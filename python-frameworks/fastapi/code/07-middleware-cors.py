"""Middleware, CORS, and request/response processing."""
from typing import Any, Callable
import json
import time


# ======================== Middleware Framework ========================

class BaseMiddleware:
    """Base middleware class."""
    def __init__(self, app: Callable):
        self.app = app

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        return self.app(scope, receive, send)


class MiddlewareStack:
    """Middleware stack processor."""
    def __init__(self, app: Callable):
        self.app = app
        self.middlewares: list[type] = []

    def add(self, middleware_cls: type):
        self.middlewares.append(middleware_cls)

    def build(self) -> Callable:
        """Wrap app with all middlewares (outermost first)."""
        wrapped = self.app
        for mw_cls in reversed(self.middlewares):
            wrapped = mw_cls(wrapped)
        return wrapped


# ======================== CORSMiddleware ========================

class CORSMiddleware(BaseMiddleware):
    """Simulates FastAPI's CORSMiddleware."""
    def __init__(self, app, allow_origins=None, allow_methods=None, allow_headers=None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_credentials = True

    def __call__(self, scope, receive, send):
        request = scope
        # Handle preflight
        if request.get("method") == "OPTIONS":
            return self._preflight_response(request)
        response = self.app(scope, receive, send)
        response["headers"] = {
            **response.get("headers", {}),
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
            "Access-Control-Allow-Headers": ", ".join(self.allow_headers),
        }
        return response

    def _preflight_response(self, request) -> dict:
        return {
            "status": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": ", ".join(self.allow_methods),
                "Access-Control-Allow-Headers": ", ".join(self.allow_headers),
                "Access-Control-Max-Age": "600",
            },
        }


# ======================== Custom Middlewares ========================

class TimingMiddleware(BaseMiddleware):
    """Logs request processing time."""
    def __call__(self, scope, receive, send):
        start = time.time()
        response = self.app(scope, receive, send)
        duration = time.time() - start
        response["headers"]["X-Process-Time"] = f"{duration:.4f}"
        print(f"  [Timing] {scope.get('method', '?')} {scope.get('path', '?')} took {duration*1000:.1f}ms")
        return response


class LoggingMiddleware(BaseMiddleware):
    """Logs all requests."""
    def __call__(self, scope, receive, send):
        print(f"  [Request] {scope.get('method', '?')} {scope.get('path', '?')}")
        response = self.app(scope, receive, send)
        print(f"  [Response] → {response.get('status', '?')}")
        return response


# ======================== App ========================

def app(scope: dict, receive=None, send=None) -> dict:
    """Simple app that returns JSON responses."""
    path = scope.get("path", "/")
    method = scope.get("method", "GET")
    data = scope.get("data", {})

    if path == "/" and method == "GET":
        return {"status": 200, "data": {"message": "Hello World"}}
    elif path == "/items" and method == "GET":
        return {"status": 200, "data": {"items": [{"id": 1, "name": "Item 1"}]}}
    elif path == "/items" and method == "POST":
        return {"status": 201, "data": {"id": 2, "name": data.get("name", "New Item")}}
    return {"status": 404, "data": {"detail": "Not Found"}}


# ======================== Demo ========================
print("=== Middleware & CORS Demo ===\n")

# Build middleware stack
stack = MiddlewareStack(app)
stack.add(LoggingMiddleware)
stack.add(TimingMiddleware)
stack.add(lambda app: CORSMiddleware(app, allow_origins=["https://frontend.com"]))

wrapped_app = stack.build()

# Simulate requests
requests = [
    {"method": "GET", "path": "/", "data": {}},
    {"method": "GET", "path": "/items", "data": {}},
    {"method": "POST", "path": "/items", "data": {"name": "New Item"}},
    {"method": "OPTIONS", "path": "/items", "data": {}},
    {"method": "GET", "path": "/nonexistent", "data": {}},
]

for req in requests:
    print(f"\n  Request: {req['method']} {req['path']}")
    response = wrapped_app(req)
    status = response.get("status", 0)
    icon = "✅" if status < 400 else "❌"
    headers = response.get("headers", {})
    cors_headers = {k: v for k, v in headers.items() if "Access-Control" in k or "X-" in k}
    print(f"  Response: {icon} {status}")
    if cors_headers:
        print(f"  Headers: {json.dumps(cors_headers)}")
    if response.get("data"):
        print(f"  Body: {json.dumps(response['data'])}")

# CORS summary
print("\nCORS Configuration:")
cors_config = [
    ("allow_origins", ["https://frontend.com"]),
    ("allow_methods", ["GET", "POST", "PUT", "DELETE", "OPTIONS"]),
    ("allow_headers", ["*"]),
    ("allow_credentials", True),
    ("max_age", 600),
]
for key, val in cors_config:
    print(f"  {key:20s}: {val}")
