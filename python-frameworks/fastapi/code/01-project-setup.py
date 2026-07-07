"""FastAPI project setup, first endpoint, uvicorn runner."""
from typing import Any
import json


# ======================== Mini FastAPI Framework ========================

class FastAPI:
    """Simulates FastAPI's core application."""
    def __init__(self, title: str = "FastAPI"):
        self.title = title
        self.routes: list[dict] = []

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
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


# ======================== App ========================

app = FastAPI(title="My First API")


@app.get("/")
def read_root():
    return {"message": "Hello World", "docs_url": "/docs", "openapi_url": "/openapi.json"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}


@app.post("/items")
def create_item(name: str, price: float):
    return {"name": name, "price": price, "id": 42}


# ======================== Demo ========================
print("=== FastAPI Project Setup ===\n")
print(f"App: {app.title}\n")

# Simulate requests
tests = [
    ("GET", "/"),
    ("GET", "/health"),
    ("GET", "/items/5"),
    ("GET", "/nonexistent"),
    ("POST", "/items", {"name": "Laptop", "price": 999.99}),
]

for method, path, *data in tests:
    kwargs = data[0] if data else {}
    result = app(method, path, **kwargs)
    print(f"  {method:6s} {path:20s} → {result['status']}: {json.dumps(result['data'])}")

# Show registered routes
print(f"\nRegistered routes ({len(app.routes)}):")
for route in app.routes:
    print(f"  {route['method']:6s} {route['path']}")
