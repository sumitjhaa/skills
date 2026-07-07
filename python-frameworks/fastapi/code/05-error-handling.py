"""Error handling: HTTPException, validation errors, custom handlers."""
from typing import Any, Optional, Callable
import json
import traceback


# ======================== HTTP Exception ========================

class HTTPException(Exception):
    """Simulates FastAPI's HTTPException."""
    def __init__(self, status_code: int, detail: str = "", headers: dict = None):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers or {}

    def response(self) -> dict:
        return {
            "status_code": self.status_code,
            "data": {"detail": self.detail},
            "headers": self.headers,
        }


# ======================== Validation Error ========================

class ValidationError(Exception):
    """Simulates Pydantic/FastAPI validation errors."""
    def __init__(self, errors: list[dict]):
        self.errors = errors

    def response(self) -> dict:
        return {
            "status_code": 422,
            "data": {"detail": self.errors},
        }


# ======================== Exception Handler ========================

class ExceptionHandler:
    """Simulates FastAPI's exception handlers."""
    def __init__(self):
        self._handlers: dict[type, Callable] = {}

    def register(self, exc_class: type, handler: Callable):
        self._handlers[exc_class] = handler

    def handle(self, exc: Exception) -> dict:
        for exc_class, handler in self._handlers.items():
            if isinstance(exc, exc_class):
                return handler(exc)
        # Default: 500
        return {
            "status_code": 500,
            "data": {"detail": "Internal server error"},
        }


# ======================== Custom Exceptions ========================

class NotFoundError(HTTPException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(status_code=404, detail=f"{resource} not found")


class UnauthorizedError(HTTPException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(status_code=401, detail=message)


class ForbiddenError(HTTPException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(status_code=403, detail=message)


class RateLimitError(HTTPException):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            detail="Too many requests",
            headers={"Retry-After": str(retry_after)},
        )


# ======================== Data Store ========================

POSTS = [
    {"id": 1, "title": "Hello FastAPI", "content": "Getting started", "author": "alice"},
    {"id": 2, "title": "Error Handling", "content": "How to handle errors", "author": "bob"},
]


# ======================== API with Error Handling ========================

class FastAPI:
    def __init__(self):
        self.routes = []
        self.exception_handler = ExceptionHandler()
        self._setup_default_handlers()

    def _setup_default_handlers(self):
        self.exception_handler.register(HTTPException, lambda e: e.response())
        self.exception_handler.register(ValidationError, lambda e: e.response())
        self.exception_handler.register(NotFoundError, lambda e: e.response())

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                try:
                    result = route["handler"](**kwargs)
                    return {"status": 200, "data": result}
                except Exception as e:
                    return self.exception_handler.handle(e)
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if not post:
        raise NotFoundError(f"Post {post_id}")
    return post


@app.post("/posts")
def create_post(title: str = "", content: str = ""):
    errors = []
    if not title:
        errors.append({"loc": ["body", "title"], "msg": "field required", "type": "value_error.missing"})
    if len(title) < 3:
        errors.append({"loc": ["body", "title"], "msg": "ensure this value has at least 3 characters", "type": "value_error"})
    if errors:
        raise ValidationError(errors)
    post = {"id": len(POSTS) + 1, "title": title, "content": content}
    POSTS.append(post)
    return post


@app.get("/secret")
def get_secret():
    raise ForbiddenError("Admin access required")


# ======================== Demo ========================
print("=== Error Handling Demo ===\n")

tests = [
    ("GET", "/posts/1"),
    ("GET", "/posts/999"),
    ("POST", "/posts"),
    ("GET", "/secret"),
    ("GET", "/nonexistent"),
]

for method, path in tests:
    result = app(method, path)
    status = result["status"]
    icon = "✅" if status == 200 else "❌" if status == 404 else "⚠️"
    print(f"  {icon} {method:6s} {path:20s} → {status}: {json.dumps(result['data'])}")
