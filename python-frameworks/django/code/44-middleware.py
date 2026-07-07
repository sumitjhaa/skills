"""Middleware: custom middleware, process_request, process_response, process_exception."""
from typing import Any, Callable, Optional
from functools import wraps
import time


# ======================== Request/Response Simulation ========================
class HttpRequest:
    def __init__(self, method="GET", path="/", user=None, META=None):
        self.method = method
        self.path = path
        self.user = user or "Anonymous"
        self.META = META or {}
        self.session = {}


class HttpResponse:
    def __init__(self, content="", status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}

    def __repr__(self):
        return f"HttpResponse({self.status}, {self.content[:50]})"


# ======================== Middleware Framework ========================

class MiddlewareMixin:
    """Base class for middleware (simulates Django's process_view etc.)."""

    def __init__(self, get_response: Callable = None):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.process_request(request)
        if response is None:
            response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        return None

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        return response

    def process_exception(self, request: HttpRequest, exception: Exception) -> Optional[HttpResponse]:
        return None

    def process_view(self, request: HttpRequest, view_func: Callable, view_args: tuple, view_kwargs: dict) -> Optional[HttpResponse]:
        return None


# ======================== Custom Middlewares ========================

class RequestTimingMiddleware(MiddlewareMixin):
    """Logs request processing time."""

    def process_request(self, request):
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            response.headers['X-Request-Duration'] = f"{duration:.4f}"
            print(f"  [Timing] {request.method} {request.path} took {duration:.4f}s")
        return response


class BlockPrivateIPMiddleware(MiddlewareMixin):
    """Blocks requests from private IP ranges."""

    def process_request(self, request):
        remote_addr = request.META.get("REMOTE_ADDR", "0.0.0.0")
        if remote_addr.startswith(("10.", "172.16.", "192.168.")):
            return HttpResponse("Forbidden: Private IP not allowed", status=403)
        return None


class AdminOnlyMiddleware(MiddlewareMixin):
    """Restricts certain paths to admin users."""

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith("/admin/") and request.user != "admin":
            return HttpResponse("Admin access required", status=403)
        return None


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Adds security headers to every response."""

    def process_response(self, request, response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response


class ErrorHandlingMiddleware(MiddlewareMixin):
    """Catches exceptions and returns a friendly response."""

    def process_exception(self, request, exception):
        print(f"  [ErrorHandler] Caught: {type(exception).__name__}: {exception}")
        return HttpResponse(
            f"<h1>Server Error</h1><p>{exception}</p>",
            status=500,
        )


# ======================== WSGI App Simulation ========================

def dummy_view(request):
    """Simulate a view that processes the request."""
    if request.path == "/slow":
        time.sleep(0.2)
    if request.path == "/error":
        raise ValueError("Something went wrong!")
    return HttpResponse(f"Hello {request.user}, you are at {request.path}")


class WSGIHandler:
    """Simple WSGI app that runs middleware chain."""

    def __init__(self, middlewares: list[type]):
        # Build middleware chain (inner-to-outer)
        self.get_response = dummy_view
        for mw_cls in reversed(middlewares):
            self.get_response = mw_cls(self.get_response)

    def __call__(self, request):
        return self.get_response(request)


# ======================== Demo ========================
print("=== Middleware Demo ===\n")

# Set up middleware stack
middlewares = [
    SecurityHeadersMiddleware,
    RequestTimingMiddleware,
    ErrorHandlingMiddleware,
    AdminOnlyMiddleware,
    BlockPrivateIPMiddleware,
]

app = WSGIHandler(middlewares)

# --- Normal request ---
print("1. Normal GET /home/:")
req = HttpRequest("GET", "/home/", user="alice", META={"REMOTE_ADDR": "203.0.113.1"})
resp = app(req)
print(f"   Response: {resp.status}")
print(f"   Headers: {dict(resp.headers)}")

# --- Admin path (non-admin user) ---
print("\n2. GET /admin/ (non-admin):")
req = HttpRequest("GET", "/admin/", user="alice", META={"REMOTE_ADDR": "203.0.113.1"})
resp = app(req)
print(f"   Response: {resp.status} — {resp.content}")

# --- Admin path (admin user) ---
print("\n3. GET /admin/ (admin):")
req = HttpRequest("GET", "/admin/", user="admin", META={"REMOTE_ADDR": "203.0.113.1"})
resp = app(req)
print(f"   Response: {resp.status} — {resp.content}")

# --- Slow request (timing middleware) ---
print("\n4. GET /slow/ (timing):")
req = HttpRequest("GET", "/slow/", user="alice", META={"REMOTE_ADDR": "203.0.113.1"})
resp = app(req)
print(f"   Response: {resp.status}, duration={resp.headers.get('X-Request-Duration')}s")

# --- Blocked private IP ---
print("\n5. GET /home/ (private IP 192.168.1.1):")
req = HttpRequest("GET", "/home/", user="alice", META={"REMOTE_ADDR": "192.168.1.1"})
resp = app(req)
print(f"   Response: {resp.status} — {resp.content}")

# --- Exception handling ---
print("\n6. GET /error/ (exception caught by middleware):")
req = HttpRequest("GET", "/error/", user="alice", META={"REMOTE_ADDR": "203.0.113.1"})
resp = app(req)
print(f"   Response: {resp.status} — {resp.content[:40]}...")
