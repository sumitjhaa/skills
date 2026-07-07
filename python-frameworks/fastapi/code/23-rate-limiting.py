"""Rate limiting: token bucket, sliding window, per-IP, per-user, burst handling."""
from typing import Any, Optional
from datetime import datetime, timedelta
import json
import time
import threading


# ======================== Rate Limiters ========================

class TokenBucket:
    """Token bucket algorithm: refills tokens over time."""
    def __init__(self, rate: float, burst: int):
        self.rate = rate  # tokens per second
        self.burst = burst  # max tokens
        self.tokens = burst
        self.last_refill = time.time()
        self._lock = threading.Lock()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> bool:
        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def remaining(self) -> float:
        with self._lock:
            self._refill()
            return self.tokens


class SlidingWindow:
    """Sliding window counter: limits requests within a rolling time window."""
    def __init__(self, max_requests: int, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._timestamps: list[float] = []
        self._lock = threading.Lock()

    def allow(self) -> bool:
        now = time.time()
        with self._lock:
            cutoff = now - self.window_seconds
            self._timestamps = [ts for ts in self._timestamps if ts > cutoff]
            if len(self._timestamps) < self.max_requests:
                self._timestamps.append(now)
                return True
            return False

    def remaining(self) -> int:
        now = time.time()
        with self._lock:
            cutoff = now - self.window_seconds
            self._timestamps = [ts for ts in self._timestamps if ts > cutoff]
            return max(0, self.max_requests - len(self._timestamps))

    def reset_in(self) -> float:
        now = time.time()
        with self._lock:
            if not self._timestamps:
                return 0.0
            oldest = self._timestamps[0]
            return max(0.0, self.window_seconds - (now - oldest))


class RateLimiter:
    """Multi-key rate limiter: separate limits per IP, user, endpoint."""
    def __init__(self, default_rate: float = 10, default_burst: int = 20):
        self.default_rate = default_rate
        self.default_burst = default_burst
        self._buckets: dict[str, TokenBucket] = {}
        self._windows: dict[str, SlidingWindow] = {}
        self._lock = threading.Lock()

    def _get_or_create_bucket(self, key: str) -> TokenBucket:
        with self._lock:
            if key not in self._buckets:
                self._buckets[key] = TokenBucket(self.default_rate, self.default_burst)
            return self._buckets[key]

    def _get_or_create_window(self, key: str) -> SlidingWindow:
        with self._lock:
            if key not in self._windows:
                self._windows[key] = SlidingWindow(self.default_burst, 60)
            return self._windows[key]

    def check_bucket(self, key: str, tokens: int = 1) -> dict:
        bucket = self._get_or_create_bucket(key)
        allowed = bucket.consume(tokens)
        return {
            "allowed": allowed,
            "remaining": bucket.remaining(),
            "limit": self.default_burst,
        }

    def check_window(self, key: str) -> dict:
        window = self._get_or_create_window(key)
        allowed = window.allow()
        return {
            "allowed": allowed,
            "remaining": window.remaining(),
            "limit": window.max_requests,
            "reset_in": round(window.reset_in(), 1),
        }

    def check(self, key: str, strategy: str = "bucket") -> dict:
        if strategy == "bucket":
            return self.check_bucket(key)
        return self.check_window(key)

    def stats(self) -> dict:
        return {
            "buckets": len(self._buckets),
            "windows": len(self._windows),
            "default_rate": self.default_rate,
            "default_burst": self.default_burst,
        }


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.rate_limiter = RateLimiter(default_rate=5, default_burst=10)

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Rate Limited Endpoints ========================

def rate_limit_key(client_ip: str = "127.0.0.1", user_id: str = "", endpoint: str = "") -> str:
    """Generate a rate limit key."""
    if user_id:
        return f"user:{user_id}:{endpoint}"
    return f"ip:{client_ip}:{endpoint}"


@app.post("/api/items")
def create_item(name: str, price: float, client_ip: str = "127.0.0.1", user_id: str = ""):
    key = rate_limit_key(client_ip=client_ip, user_id=user_id, endpoint="create_item")
    result = app.rate_limiter.check(key, strategy="bucket")

    if not result["allowed"]:
        return {"error": "rate_limited", "retry_after": 1, "limit": result["limit"]}, 429

    item = {"id": 1, "name": name, "price": price}
    return {"item": item, "rate_limit": result}


@app.get("/api/items")
def list_items(client_ip: str = "127.0.0.1", user_id: str = ""):
    key = rate_limit_key(client_ip=client_ip, user_id=user_id, endpoint="list_items")
    result = app.rate_limiter.check(key, strategy="bucket")

    if not result["allowed"]:
        return {"error": "rate_limited", "retry_after": 1, "limit": result["limit"]}, 429

    return {"items": [{"id": 1, "name": "Item 1"}], "rate_limit": result}


@app.get("/api/public")
def public_endpoint(client_ip: str = "127.0.0.1"):
    """Public endpoint with stricter rate limit."""
    key = rate_limit_key(client_ip=client_ip, endpoint="public")
    result = app.rate_limiter.check(key, strategy="window")

    if not result["allowed"]:
        return {"error": "rate_limited", "retry_after": result["reset_in"], "limit": result["limit"]}, 429

    return {"message": "Public data", "rate_limit": result}


@app.get("/api/rate-limit-status")
def rate_limit_status():
    """Check current rate limit status."""
    return app.rate_limiter.stats()


# ======================== Demo ========================
print("=== Rate Limiting Demo ===\n")

print("1. Initial rate limiter stats:")
print(f"   {json.dumps(app.rate_limiter.stats(), indent=2)}\n")

print("2. Making requests (rate limit: 10 req/burst, 5 tokens/sec refill):\n")
client_ip = "192.168.1.100"

for i in range(15):
    result = app("POST", "/api/items", name=f"Item {i}", price=10.0 + i, client_ip=client_ip)
    status = "✅" if "item" in result["data"] else "❌"
    rl = result["data"].get("rate_limit", result["data"])
    remaining = rl.get("remaining", 0)
    print(f"   Request {i+1:2d}: {status} remaining={remaining:.1f}")
    if "error" in result["data"]:
        print(f"             → {result['data']['error']}")
        break
    time.sleep(0.05)

# Wait for refill
print(f"\n3. Waiting 1 second for token refill...")
time.sleep(1.0)

print(f"\n4. After refill:")
result = app("POST", "/api/items", name="Refilled Item", price=99.99, client_ip=client_ip)
rl = result["data"].get("rate_limit", {})
print(f"   remaining={rl.get('remaining', 0):.1f} (should be ~5)\n")

# Different clients have separate limits
print("5. Different client (separate bucket):")
result2 = app("POST", "/api/items", name="Bob's Item", price=50.0, client_ip="192.168.1.200")
rl2 = result2["data"].get("rate_limit", {})
print(f"   Bob: remaining={rl2.get('remaining', 0):.1f} (full bucket)\n")

# Window-based limiting
print("6. Window-based rate limit (10 req/min on /api/public):")
for i in range(12):
    result = app("GET", "/api/public", client_ip=client_ip)
    status = "✅" if "message" in result["data"] else "❌"
    rl = result["data"].get("rate_limit", result["data"])
    remaining = rl.get("remaining", 0)
    print(f"   Request {i+1:2d}: {status} remaining={remaining} reset_in={rl.get('reset_in', 0)}s")

print(f"\n7. Final rate limiter stats:")
print(f"   {json.dumps(app.rate_limiter.stats(), indent=2)}")
