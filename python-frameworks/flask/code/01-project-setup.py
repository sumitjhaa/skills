"""Flask project setup, routes, running the dev server."""
from typing import Any
import json


# ======================== Mini Flask Framework ========================

class Flask:
    """Simulates Flask's core application."""
    def __init__(self, name: str = "__main__"):
        self.name = name
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def decorator(func):
            self.routes.append({"path": path, "methods": methods, "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if method in route["methods"] and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask(__name__)


# ======================== Routes ========================

@app.route("/")
def home():
    return {"message": "Hello Flask!", "docs": "Try /about, /hello/<name>"}


@app.route("/about")
def about():
    return {"app": "Flask Demo", "version": "1.0.0", "author": "FastAPI Learner"}


@app.route("/hello/<name>")
def hello(name: str):
    return {"message": f"Hello, {name}!", "name": name}


@app.route("/json")
def json_example():
    return {
        "string": "value",
        "number": 42,
        "boolean": True,
        "list": [1, 2, 3],
        "nested": {"key": "value"},
    }


# ======================== Demo ========================
print("=== Flask Project Setup ===\n")
print(f"App: {app.name}\n")

tests = [
    ("GET", "/"),
    ("GET", "/about"),
    ("GET", "/hello/Alice"),
    ("GET", "/hello/World"),
    ("GET", "/json"),
    ("GET", "/nonexistent"),
]

for method, path in tests:
    result = app(method, path)
    icon = "✅" if result["status"] == 200 else "❌"
    print(f"  {icon} {method:6s} {path:25s} → {json.dumps(result['data'])}")

print(f"\nRegistered routes ({len(app.routes)}):")
for route in app.routes:
    methods = ",".join(route["methods"])
    print(f"  {methods:10s} {route['path']}")
