"""Request handling: query params, form data, headers, method dispatch."""
from typing import Any, Optional
from urllib.parse import parse_qs
import json


# ======================== Request Simulation ========================

class Request:
    """Simulates Flask's request object."""
    def __init__(self, method: str = "GET", path: str = "/", **kwargs):
        self.method = method
        self.path = path
        self.args: dict[str, str] = {}
        self.form: dict[str, str] = {}
        self.headers: dict[str, str] = kwargs.get("headers", {}).copy()
        self.json: Any = kwargs.get("json")
        self._data = kwargs

        # Parse query string
        query = kwargs.get("query", "")
        if query:
            for k, v in parse_qs(query).items():
                self.args[k] = v[0]

        # Parse form data
        for k, v in kwargs.items():
            if k not in ("headers", "query", "method", "path", "json"):
                self.form[k] = str(v)
                if k not in self.args:
                    self.args[k] = str(v)

    def get_arg(self, key: str, default: Any = None) -> Any:
        return self.args.get(key, default)

    def get_form(self, key: str, default: Any = None) -> Any:
        return self.form.get(key, default)

    def get_header(self, key: str, default: Any = None) -> Any:
        return self.headers.get(key, default)

    @property
    def user_agent(self) -> str:
        return self.headers.get("User-Agent", "Unknown")


class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def decorator(func):
            self.routes.append({"path": path, "methods": methods, "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        req = Request(method=method, path=path, **kwargs)
        for route in self.routes:
            if method in route["methods"] and route["path"] == path:
                result = route["handler"](req)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()


# ======================== Routes ========================

@app.route("/", methods=["GET", "POST"])
def index(req: Request):
    return {
        "method": req.method,
        "path": req.path,
        "message": "Try /search?q=python or POST to /submit",
    }


@app.route("/search")
def search(req: Request):
    q = req.get_arg("q", "")
    limit = int(req.get_arg("limit", "10"))
    page = int(req.get_arg("page", "1"))

    results = [f"Result {i} for '{q}'" for i in range(1, min(limit + 1, 6))]
    return {
        "query": q,
        "limit": limit,
        "page": page,
        "results": results,
        "total": len(results),
    }


@app.route("/submit", methods=["POST"])
def submit(req: Request):
    name = req.get_form("name", "")
    email = req.get_form("email", "")
    age = req.get_form("age", "0")

    errors = []
    if not name:
        errors.append("Name is required")
    if "@" not in email:
        errors.append("Valid email is required")

    if errors:
        return {"status": "error", "errors": errors}

    return {
        "status": "success",
        "data": {"name": name, "email": email, "age": int(age)},
    }


@app.route("/headers")
def show_headers(req: Request):
    return {
        "user_agent": req.user_agent,
        "method": req.method,
        "content_type": req.get_header("Content-Type", "N/A"),
        "accept": req.get_header("Accept", "N/A"),
        "host": req.get_header("Host", "localhost"),
    }


@app.route("/method", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def method_handler(req: Request):
    method_handlers = {
        "GET": "Retrieved resource",
        "POST": "Created resource",
        "PUT": "Updated resource",
        "DELETE": "Deleted resource",
        "PATCH": "Partially updated resource",
    }
    return {
        "method": req.method,
        "action": method_handlers.get(req.method, "Unknown method"),
        "allowed_methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
    }


# ======================== Demo ========================
print("=== Request Handling Demo ===\n")

print("1. GET / with query params:")
r = app("GET", "/", query="test=1")
print(f"   Method: {r['data']['method']}, Path: {r['data']['path']}\n")

print("2. GET /search with query params:")
r = app("GET", "/search", q="flask", limit=3, page=1)
print(f"   Query: {r['data']['query']}")
print(f"   Results: {r['data']['results']}\n")

print("3. POST /submit with form data:")
r = app("POST", "/submit", name="Alice", email="alice@example.com", age=30)
print(f"   Status: {r['data']['status']}")
print(f"   Data: {r['data']['data']}\n")

print("4. POST /submit with validation errors:")
r = app("POST", "/submit", name="", email="invalid")
print(f"   Status: {r['data']['status']}")
print(f"   Errors: {r['data']['errors']}\n")

print("5. GET /headers:")
r = app("GET", "/headers", headers={"User-Agent": "FlaskDemo/1.0", "Accept": "application/json"})
print(f"   User-Agent: {r['data']['user_agent']}")
print(f"   Accept: {r['data']['accept']}\n")

print("6. Different HTTP methods on /method:")
for method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
    r = app(method, "/method")
    print(f"   {method:8s} → {r['data']['action']}")
