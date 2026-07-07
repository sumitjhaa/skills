"""Path parameters, query parameters, parameter validation."""
from typing import Any, Optional
import json
from enum import Enum


# ======================== Parameter Handling ========================

class ParamExtractor:
    """Extract and validate path/query parameters."""
    @staticmethod
    def extract_path_params(path: str, pattern: str) -> dict:
        path_parts = path.strip("/").split("/")
        pattern_parts = pattern.strip("/").split("/")
        params = {}
        for pp, pt in zip(path_parts, pattern_parts):
            if pt.startswith("{") and pt.endswith("}"):
                name = pt[1:-1]
                params[name] = pp
        return params

    @staticmethod
    def extract_query_params(query_string: str) -> dict:
        if not query_string:
            return {}
        params = {}
        for part in query_string.split("&"):
            if "=" in part:
                k, v = part.split("=", 1)
                params[k] = v
        return params


# ======================== Type Coercion ========================

def coerce(value: str, target_type) -> Any:
    """Convert string to target type with error handling."""
    if target_type == int:
        return int(value)
    elif target_type == float:
        return float(value)
    elif target_type == bool:
        return value.lower() in ("true", "1", "yes")
    elif target_type == str:
        return value
    return value


# ======================== App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def _validate_params(self, handler, params: dict) -> tuple[bool, str, dict]:
        import inspect
        sig = inspect.signature(handler)
        validated = {}
        for name, param in sig.parameters.items():
            if name in params:
                try:
                    if param.annotation != inspect.Parameter.empty:
                        validated[name] = coerce(params[name], param.annotation)
                    else:
                        validated[name] = params[name]
                except (ValueError, TypeError):
                    return False, f"Invalid value for '{name}': expected {param.annotation.__name__}", {}
                del params[name]
            else:
                if param.default == inspect.Parameter.empty:
                    return False, f"Missing required parameter: '{name}'", {}
                validated[name] = param.default if param.default is not None else None
        return True, "", validated

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, query: str = "") -> dict:
        for route in self.routes:
            if route["method"] != method:
                continue
            path_params = ParamExtractor.extract_path_params(path, route["path"])
            if not path_params and route["path"] != path and "/" not in route["path"].strip("/"):
                continue
            if path_params or route["path"] == path:
                query_params = ParamExtractor.extract_query_params(query)
                all_params = {**query_params, **path_params}
                valid, err, validated = self._validate_params(route["handler"], all_params)
                if not valid:
                    return {"status": 422, "data": {"detail": err}}
                result = route["handler"](**validated)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}


@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}


@app.get("/search")
def search_items(q: str = "", limit: int = 10, offset: int = 0):
    return {"query": q, "limit": limit, "offset": offset, "results": [f"Result {i}" for i in range(limit)]}


@app.get("/products")
def list_products(category: str = "", min_price: float = 0.0, max_price: float = 999999.0, in_stock: bool = True):
    return {
        "category": category or "all",
        "price_range": f"${min_price}-${max_price}",
        "in_stock": in_stock,
        "count": 25,
    }


# ======================== Demo ========================
print("=== Path & Query Parameters Demo ===\n")

tests = [
    ("GET", "/items/42", ""),
    ("GET", "/items/abc", ""),
    ("GET", "/users/1/posts/5", ""),
    ("GET", "/search", "q=django&limit=5"),
    ("GET", "/search", "limit=abc"),
    ("GET", "/products", "category=electronics&min_price=100&in_stock=true"),
    ("GET", "/products", ""),
    ("GET", "/nonexistent", ""),
]

for method, path, query in tests:
    result = app(method, path, query)
    status = result["status"]
    icon = "✅" if status == 200 else "❌" if status == 404 else "⚠️"
    print(f"  {icon} {method:6s} {path:25s} {query:40s} → {status}: {json.dumps(result['data'])}")
