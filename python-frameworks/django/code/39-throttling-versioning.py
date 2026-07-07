"""Throttling & versioning in DRF."""
from typing import Any, Optional
import json
import time
from collections import defaultdict


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", data=None, user=None, META=None):
        self.method = method
        self.data = data or {}
        self.user = user or type("Anon", (), {"is_authenticated": False})()
        self.META = META or {}


class Response:
    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self):
        return json.dumps(self.data, indent=2)


class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True


# ======================== Throttling ========================

class BaseThrottle:
    """Base throttle class."""
    def allow_request(self, request, view) -> bool:
        return True

    def wait(self) -> Optional[float]:
        return None


class AnonRateThrottle(BaseThrottle):
    """Anonymous user: 5 requests per minute."""
    rate = "5/min"
    scope = "anon"
    cache = defaultdict(list)

    def allow_request(self, request, view) -> bool:
        if request.user.is_authenticated:
            return True
        key = self.get_cache_key(request, view)
        now = time.time()
        history = self.cache[key]
        self.cache[key] = [t for t in history if now - t < 60]
        if len(self.cache[key]) >= 5:
            self._wait = 60 - (now - self.cache[key][0])
            return False
        self.cache[key].append(now)
        self._wait = None
        return True

    def wait(self) -> Optional[float]:
        return self._wait

    def get_cache_key(self, request, view) -> str:
        return f"anon:{request.META.get('REMOTE_ADDR', '0.0.0.0')}"


class UserRateThrottle(BaseThrottle):
    """Authenticated user: 10 requests per minute."""
    rate = "10/min"
    scope = "user"
    cache = defaultdict(list)

    def allow_request(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return True
        key = self.get_cache_key(request, view)
        now = time.time()
        history = self.cache[key]
        self.cache[key] = [t for t in history if now - t < 60]
        if len(self.cache[key]) >= 10:
            self._wait = 60 - (now - self.cache[key][0])
            return False
        self.cache[key].append(now)
        self._wait = None
        return True

    def wait(self) -> Optional[float]:
        return self._wait

    def get_cache_key(self, request, view) -> str:
        return f"user:{request.user.username}"


class ScopedRateThrottle(BaseThrottle):
    """Per-scope throttle (e.g., 'uploads' scope: 3/min)."""
    scope_rates = {"uploads": (3, 60)}

    def __init__(self, scope: str = None):
        self.scope = scope
        self.cache = defaultdict(list)

    def allow_request(self, request, view) -> bool:
        if not self.scope or self.scope not in self.scope_rates:
            return True
        max_reqs, window = self.scope_rates[self.scope]
        key = f"scope:{self.scope}:{request.user.username if request.user.is_authenticated else 'anon'}"
        now = time.time()
        history = self.cache[key]
        self.cache[key] = [t for t in history if now - t < window]
        if len(self.cache[key]) >= max_reqs:
            self._wait = window - (now - self.cache[key][0])
            return False
        self.cache[key].append(now)
        self._wait = None
        return True

    def wait(self) -> Optional[float]:
        return self._wait


# ======================== Throttled View ========================

class ThrottledAPIView:
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    data = {"message": "OK"}

    def dispatch(self, request):
        for throttle_cls in self.throttle_classes:
            throttle = throttle_cls()
            if not throttle.allow_request(request, self):
                wait_time = throttle.wait()
                return Response(
                    {"detail": "Request was throttled.",
                     "retry_after": round(wait_time, 1) if wait_time else 60},
                    status=429,
                    headers={"Retry-After": str(round(wait_time or 60))},
                )
        return self.get(request)

    def get(self, request):
        return Response(self.data)

    @classmethod
    def as_view(cls):
        def view(request):
            instance = cls()
            return instance.dispatch(request)
        return view


# ======================== Versioning ========================

class URLPathVersioning:
    """Version via URL path: /api/v1/posts/"""
    default_version = "v1"
    allowed_versions = ["v1", "v2"]
    version_param = "version"

    def determine_version(self, request, view, **kwargs) -> str:
        return kwargs.get(self.version_param, self.default_version)


class AcceptHeaderVersioning:
    """Version via Accept header: Accept: application/json; version=v2"""
    default_version = "v1"
    allowed_versions = ["v1", "v2"]

    def determine_version(self, request, view, **kwargs) -> str:
        accept = request.META.get("HTTP_ACCEPT", "")
        for part in accept.split(";"):
            part = part.strip()
            if part.startswith("version="):
                version = part.split("=")[1].strip()
                if version in self.allowed_versions:
                    return version
        return self.default_version


# ======================== Versioned Views ========================

class PostListV1:
    """v1: flat list."""
    data = [
        {"id": 1, "title": "Hello", "author": "alice"},
        {"id": 2, "title": "DRF", "author": "bob"},
    ]

    def get(self, request):
        return Response({"version": "v1", "results": self.data})


class PostListV2:
    """v2: nested author."""
    data = [
        {"id": 1, "title": "Hello", "author": {"name": "alice", "email": "alice@example.com"}},
        {"id": 2, "title": "DRF", "author": {"name": "bob", "email": "bob@example.com"}},
    ]

    def get(self, request):
        return Response({"version": "v2", "results": self.data})


# ======================== Demo ========================
print("=== Throttling & Versioning Demo ===\n")

anon = type("Anon", (), {"is_authenticated": False, "username": "Anonymous"})()
user = User("alice")

# --- Throttling ---
print("--- Throttling ---")
view = ThrottledAPIView.as_view()

for i in range(7):
    req = Request("GET", user=anon, META={"REMOTE_ADDR": "192.168.1.1"})
    resp = view(req)
    data = json.loads(resp.render())
    status_note = "✅" if resp.status == 200 else "⏳"
    detail = data.get("detail", data.get("message", ""))
    print(f"  Anon req {i+1}: {resp.status} {status_note} — {detail}")

# User throttle (within limit)
print("\n  Auth user (within limit):")
for i in range(12):
    req = Request("GET", user=user)
    resp = view(req)
    if resp.status != 200:
        data = json.loads(resp.render())
        print(f"  Auth req {i+1}: {resp.status} — {data['detail']} (retry: {data['retry_after']}s)")
        break
print(f"  Auth user made it through")

# Scoped throttle (uploads)
upload_throttle = ScopedRateThrottle(scope="uploads")
print(f"\n  Upload scope (3/min):")
for i in range(5):
    req = Request("GET", user=user)
    allowed = upload_throttle.allow_request(req, None)
    wait_time = upload_throttle.wait()
    print(f"  Upload req {i+1}: {'✅ allowed' if allowed else f'⏳ throttled (wait {wait_time:.1f}s)'}")

# --- Versioning ---
print("\n--- Versioning ---")
url_versioner = URLPathVersioning()

v1 = url_versioner.determine_version(None, None, version="v1")
print(f"  URL versioning: /api/{v1}/posts/ → {v1}")

v2 = url_versioner.determine_version(None, None, version="v2")
print(f"  URL versioning: /api/{v2}/posts/ → {v2}")

# Versioned responses
print("\n  Versioned responses:")
v1_view = PostListV1()
v2_view = PostListV2()
print(f"  V1: {json.dumps(v1_view.get(Request()).data, indent=2)}")
print(f"  V2: {json.dumps(v2_view.get(Request()).data, indent=2)}")

# Accept header versioning
accept_ver = AcceptHeaderVersioning()
req_v1 = Request(META={"HTTP_ACCEPT": "application/json; version=v1"})
print(f"\n  Accept header: version={accept_ver.determine_version(req_v1, None)}")

req_v2 = Request(META={"HTTP_ACCEPT": "application/json; version=v2"})
print(f"  Accept header: version={accept_ver.determine_version(req_v2, None)}")
