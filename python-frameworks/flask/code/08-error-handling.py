"""Error handling: abort(), custom error handlers, error pages."""
from typing import Any, Optional
import json
import traceback


# ======================== Error System ========================

class HTTPError(Exception):
    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message or self._default_message(status_code)
        super().__init__(self.message)

    @staticmethod
    def _default_message(code: int) -> str:
        messages = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            408: "Request Timeout",
            429: "Too Many Requests",
            500: "Internal Server Error",
            502: "Bad Gateway",
            503: "Service Unavailable",
        }
        return messages.get(code, f"Error {code}")


def abort(status_code: int, message: str = ""):
    raise HTTPError(status_code, message)


class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self._error_handlers: dict[int, Any] = {}

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def decorator(func):
            self.routes.append({"path": path, "methods": methods, "handler": func})
            return func
        return decorator

    def errorhandler(self, code: int):
        def decorator(func):
            self._error_handlers[code] = func
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        try:
            for route in self.routes:
                if method in route["methods"] and route["path"] == path:
                    result = route["handler"](**kwargs)
                    return {"status": 200, "data": result}

            raise HTTPError(404, f"'{path}' not found")

        except HTTPError as e:
            handler = self._error_handlers.get(e.status_code)
            if handler:
                return {"status": e.status_code, "data": handler(e)}
            return {"status": e.status_code, "data": self._default_error(e)}

    def _default_error(self, error: HTTPError) -> dict:
        return {
            "error": error.message,
            "status_code": error.status_code,
            "message": f"An error occurred: {error.message}",
        }


app = Flask()


# ======================== Custom Error Handlers ========================

@app.errorhandler(404)
def not_found(error: HTTPError):
    return {
        "error": "not_found",
        "message": "The requested resource was not found",
        "status_code": 404,
        "suggestions": ["Check the URL", "Go back to home"],
    }


@app.errorhandler(403)
def forbidden(error: HTTPError):
    return {
        "error": "forbidden",
        "message": "You don't have permission to access this resource",
        "status_code": 403,
        "required_role": "admin",
    }


@app.errorhandler(500)
def server_error(error: HTTPError):
    return {
        "error": "internal_error",
        "message": "Something went wrong on our end",
        "status_code": 500,
        "reference_id": "ERR-001",
    }


@app.errorhandler(429)
def rate_limited(error: HTTPError):
    return {
        "error": "rate_limited",
        "message": "Too many requests. Please slow down.",
        "status_code": 429,
        "retry_after_seconds": 60,
    }


# ======================== Routes ========================

@app.route("/")
def home():
    return {
        "message": "Error Handling Demo",
        "endpoints": {
            "success": "/success",
            "not_found": "/nonexistent",
            "forbidden": "/admin",
            "server_error": "/error",
            "validation": "/validate?name=",
            "custom": "/items/-1",
        },
    }


@app.route("/success")
def success():
    return {"message": "Everything works!", "status": "ok"}


@app.route("/admin")
def admin_panel():
    abort(403, "Admin access required")


@app.route("/error")
def trigger_error():
    try:
        1 / 0
    except ZeroDivisionError:
        abort(500, "Division by zero")


@app.route("/validate")
def validate(**kwargs):
    name = kwargs.get("name", "")
    if not name:
        abort(400, "Name parameter is required")
    age = kwargs.get("age", "")
    if age and (not age.isdigit() or int(age) < 0):
        abort(400, "Age must be a positive number")
    return {"message": f"Hello {name}!", "valid": True}


@app.route("/items/<int:item_id>")
def get_item(item_id: int, **kwargs):
    if item_id < 0:
        abort(400, "Item ID cannot be negative")
    if item_id > 100:
        abort(404, f"Item {item_id} not found")
    return {"id": item_id, "name": f"Item {item_id}"}


@app.route("/rate-limited")
def rate_limited():
    abort(429, "Slow down!")


# ======================== Demo ========================
print("=== Error Handling Demo ===\n")

tests = [
    ("GET", "/success"),
    ("GET", "/nonexistent"),
    ("GET", "/admin"),
    ("GET", "/error"),
    ("GET", "/validate"),
    ("GET", "/validate", "name=Alice&age=25"),
    ("GET", "/items/-1"),
    ("GET", "/items/200"),
    ("GET", "/rate-limited"),
]

print("Testing error handling:\n")
for test in tests:
    method, path = test[0], test[1]
    kwargs = {}
    if len(test) > 2:
        qs = test[2]
        for pair in qs.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                kwargs[k] = v

    result = app(method, path, **kwargs)
    status = result["status"]
    icon = "✅" if status == 200 else "❌" if status == 404 else "⚠️"
    print(f"  {icon} {method:6s} {path:30s} → {status}: {json.dumps(result['data'], indent=2)}")
    print()
