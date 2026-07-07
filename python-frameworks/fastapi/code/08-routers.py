"""Routers/APIRouter: modular route organization and mounting."""
from typing import Any, Callable
import json


# ======================== APIRouter ========================

class APIRouter:
    """Simulates FastAPI's APIRouter for modular routes."""
    def __init__(self, prefix: str = "", tags: list[str] = None):
        self.prefix = prefix
        self.tags = tags or []
        self.routes: list[dict] = []

    def _add_route(self, path: str, method: str, handler: Callable):
        full_path = self.prefix + path
        self.routes.append({"path": full_path, "method": method, "handler": handler})

    def get(self, path: str):
        def decorator(func):
            self._add_route(path, "GET", func)
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            self._add_route(path, "POST", func)
            return func
        return decorator

    def put(self, path: str):
        def decorator(func):
            self._add_route(path, "PUT", func)
            return func
        return decorator

    def delete(self, path: str):
        def decorator(func):
            self._add_route(path, "DELETE", func)
            return func
        return decorator


# ======================== Main App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def include_router(self, router: APIRouter):
        """Mount a router's routes onto the main app."""
        self.routes.extend(router.routes)

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


# ======================== Modular Routers ========================

items_router = APIRouter(prefix="/items", tags=["items"])

@items_router.get("/")
def list_items():
    return [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]


@items_router.get("/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}", "price": 99.99}


@items_router.post("/")
def create_item(name: str, price: float):
    return {"id": 3, "name": name, "price": price}


@items_router.delete("/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}


# Users router
users_router = APIRouter(prefix="/users", tags=["users"])

@users_router.get("/")
def list_users():
    return [{"id": 1, "username": "alice"}, {"id": 2, "username": "bob"}]


@users_router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "username": f"user_{user_id}", "email": f"user{user_id}@example.com"}


@users_router.get("/{user_id}/posts")
def get_user_posts(user_id: int):
    return {"user_id": user_id, "posts": [{"id": 1, "title": "Post 1"}, {"id": 2, "title": "Post 2"}]}


# Admin router (no prefix, but specific tag)
admin_router = APIRouter(prefix="/admin", tags=["admin"])

@admin_router.get("/dashboard")
def admin_dashboard():
    return {
        "stats": {
            "users": 150,
            "posts": 320,
            "comments": 1200,
        }
    }


# ======================== Main App Setup ========================

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


# Include routers
app.include_router(items_router)
app.include_router(users_router)
app.include_router(admin_router)


# ======================== Demo ========================
print("=== Routers Demo ===\n")

print(f"Registered routes ({len(app.routes)}):")
endpoint_tags = {
    "/items/": "items",
    "/items/{item_id}": "items",
    "/users/": "users",
    "/users/{user_id}": "users",
    "/users/{user_id}/posts": "users",
    "/admin/dashboard": "admin",
}

for route in app.routes:
    tag = endpoint_tags.get(route["path"], "general")
    print(f"  [{tag:7s}] {route['method']:6s} {route['path']}")

print("\nSimulating requests:")
tests = [
    ("GET", "/"),
    ("GET", "/items/"),
    ("GET", "/items/5"),
    ("POST", "/items/"),
    ("DELETE", "/items/3"),
    ("GET", "/users/"),
    ("GET", "/users/1"),
    ("GET", "/users/2/posts"),
    ("GET", "/admin/dashboard"),
    ("GET", "/nonexistent"),
]

for method, path in tests:
    result = app(method, path)
    status = result["status"]
    icon = "✅" if status == 200 else "❌"
    print(f"  {icon} {method:6s} {path:25s} → {status}")
