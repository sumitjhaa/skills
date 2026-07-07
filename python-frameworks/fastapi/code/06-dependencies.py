"""Dependencies: Depends, dependency injection, shared logic."""
from typing import Any, Optional, Callable
import json


# ======================== Dependency Injection ========================

class DependsMeta:
    """Simulates FastAPI's Depends() marker."""
    def __init__(self, dependency: Callable = None, use_cache: bool = True):
        self.dependency = dependency
        self.use_cache = use_cache


def Depends(dependency: Callable = None, use_cache: bool = True) -> Any:
    """Marker function for dependencies."""
    return DependsMeta(dependency, use_cache)


# ======================== Dependency Container ========================

class DIContainer:
    """Simple dependency injection container."""
    def __init__(self):
        self._cache = {}

    def resolve(self, dependency: Callable) -> Any:
        key = id(dependency)
        if key not in self._cache:
            self._cache[key] = dependency()
        return self._cache[key]

    def resolve_deps(self, handler: Callable) -> dict:
        import inspect
        sig = inspect.signature(handler)
        kwargs = {}
        for name, param in sig.parameters.items():
            default = param.default
            if isinstance(default, DependsMeta):
                if default.dependency:
                    kwargs[name] = self.resolve(default.dependency)
                else:
                    kwargs[name] = default.dependency
            elif default is inspect.Parameter.empty:
                kwargs[name] = param.default  # Use default if possible
            else:
                kwargs[name] = default
        return kwargs


container = DIContainer()


# ======================== Dependencies ========================

def get_db():
    """Simulates DB connection dependency."""
    return {"connection": "postgres://localhost:5432/mydb", "pool_size": 10}


def get_current_user():
    """Simulates auth dependency."""
    return {"username": "alice", "role": "admin", "is_authenticated": True}


def get_settings():
    """Simulates app settings dependency."""
    return {
        "app_name": "My API",
        "version": "1.0.0",
        "debug": False,
        "items_per_page": 20,
    }


def get_pagination(page: int = 1, page_size: int = 10):
    """Dependency with default params."""
    return {"page": page, "page_size": page_size}


# ======================== Dependency Chain ========================

def get_user_service(db=Depends(get_db), current_user=Depends(get_current_user)):
    """Dependency that depends on other dependencies."""
    return {
        "db": db,
        "user": current_user,
        "service": "UserService",
    }


# ======================== API with Dependencies ========================

class FastAPI:
    def __init__(self):
        self.routes = []

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                kwargs = container.resolve_deps(route["handler"])
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


@app.get("/items")
def list_items(db=Depends(get_db), pagination=Depends(get_pagination)):
    items = [{"id": i, "name": f"Item {i}"} for i in range(1, pagination["page_size"] + 1)]
    return {
        "db": db["connection"],
        "page": pagination["page"],
        "items": items,
        "total": 100,
    }


@app.get("/users/me")
def get_me(current_user=Depends(get_current_user)):
    return {"user": current_user["username"], "role": current_user["role"]}


@app.get("/settings")
def get_app_settings(settings=Depends(get_settings)):
    return settings


@app.get("/users/service")
def user_service_info(service=Depends(get_user_service)):
    return {
        "service": service["service"],
        "user": service["user"]["username"],
        "db": service["db"]["connection"],
    }


# ======================== Demo ========================
print("=== Dependency Injection Demo ===\n")

endpoints = ["/items", "/users/me", "/settings", "/users/service"]

for path in endpoints:
    result = app("GET", path)
    print(f"  GET {path:20s} → {json.dumps(result['data'], indent=4)}")
    print()

# Show dependency tree
print("Dependency tree:")
print("  get_settings()         → no deps")
print("  get_db()              → no deps")
print("  get_pagination()      → no deps (has defaults)")
print("  get_current_user()    → no deps")
print("  get_user_service()    → depends on: get_db(), get_current_user()")
print("  list_items()          → depends on: get_db(), get_pagination()")
