"""Blueprints: modular apps, route prefixes, subdomains, organization."""
from typing import Any, Optional
import json
import re


# ======================== Blueprint Simulation ========================

class Blueprint:
    """Simulates Flask's Blueprint."""
    def __init__(self, name: str, import_name: str, url_prefix: str = ""):
        self.name = name
        self.import_name = import_name
        self.url_prefix = url_prefix
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def decorator(func):
            full_path = self.url_prefix + path
            self.routes.append({"path": full_path, "methods": methods, "handler": func, "bp": self.name})
            return func
        return decorator


class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def register_blueprint(self, bp: Blueprint):
        self.routes.extend(bp.routes)

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def decorator(func):
            self.routes.append({"path": path, "methods": methods, "handler": func, "bp": "__main__"})
            return func
        return decorator

    @staticmethod
    def _match_route(route_pattern: str, actual_path: str) -> dict | None:
        param_names = []
        def replacer(m):
            full = m.group(0)
            if ':' in full:
                typ, name = full.strip('<>').split(':')
            else:
                typ, name = 'str', full.strip('<>')
            param_names.append((name, typ))
            if typ == 'int': return r'(\d+)'
            if typ == 'float': return r'([0-9.]+)'
            if typ == 'path': return r'(.+)'
            return r'([^/]+)'
        regex = '^' + re.sub(r'<[^>]+>', replacer, route_pattern) + '$'
        m = re.match(regex, actual_path)
        if not m: return None
        return {name: int(val) if typ == 'int' else float(val) if typ == 'float' else val
                for (name, typ), val in zip(param_names, m.groups())}

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if method in route["methods"] and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result, "blueprint": route["bp"]}
            params = self._match_route(route["path"], path)
            if method in route["methods"] and params is not None:
                result = route["handler"](**params, **kwargs)
                return {"status": 200, "data": result, "blueprint": route["bp"]}
        return {"status": 404, "data": {"error": "Not Found"}, "blueprint": None}


app = Flask()


# ======================== Blueprints ========================

# Auth Blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login(**kwargs):
    if kwargs:
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")
        if username == "admin" and password == "secret":
            return {"message": "Login successful", "token": "fake-jwt-token"}
        return {"error": "Invalid credentials"}
    return {"message": "Login page", "form": {"username": "", "password": ""}}


@auth_bp.route("/logout")
def logout():
    return {"message": "Logged out"}


@auth_bp.route("/register", methods=["GET", "POST"])
def register(**kwargs):
    if kwargs:
        return {"message": "Registration successful", "user": kwargs.get("username")}
    return {"message": "Registration page"}


@auth_bp.route("/profile")
def profile():
    return {"message": "User profile (protected)"}


# API Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@api_bp.route("/items")
def list_items():
    return {"items": [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]}


@api_bp.route("/items/<int:item_id>")
def get_item(item_id: int, **kwargs):
    return {"id": item_id, "name": f"Item {item_id}", "price": 9.99}


@api_bp.route("/items", methods=["POST"])
def create_item(**kwargs):
    return {"id": 3, "name": kwargs.get("name", "New Item"), "price": float(kwargs.get("price", 0))}


# Admin Blueprint
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def admin_dashboard():
    return {"message": "Admin Dashboard", "stats": {"users": 42, "posts": 128}}


@admin_bp.route("/users")
def admin_users():
    return {"users": [{"id": 1, "username": "alice"}, {"id": 2, "username": "bob"}]}


@admin_bp.route("/settings")
def admin_settings():
    return {"settings": {"site_name": "Flask App", "maintenance": False}}


# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp)


# ======================== Main Routes ========================

@app.route("/")
def home():
    return {
        "message": "Flask Blueprints Demo",
        "blueprints": {
            "auth": "/auth/* (login, logout, register, profile)",
            "api": "/api/v1/* (items CRUD)",
            "admin": "/admin/* (dashboard, users, settings)",
        },
    }


@app.route("/routes")
def list_routes():
    return {"routes": [{"path": r["path"], "methods": r["methods"], "blueprint": r["bp"]} for r in app.routes]}


# ======================== Demo ========================
print("=== Blueprints & Modular Apps Demo ===\n")

print("1. All registered routes:")
for r in app.routes:
    methods = ",".join(r["methods"])
    print(f"   [{r['bp']:8s}] {methods:10s} {r['path']}")

print("\n2. Home:")
r = app("GET", "/")
print(f"   {json.dumps(r['data'], indent=2)}\n")

print("3. Auth routes:")
for path in ["/auth/login", "/auth/logout", "/auth/register", "/auth/profile"]:
    r = app("GET", path)
    print(f"   {r['data']['message']} (via {r['blueprint']} blueprint)")

print("\n4. API routes:")
r = app("GET", "/api/v1/items")
print(f"   List items: {len(r['data']['items'])} items")
r = app("GET", "/api/v1/items/5")
print(f"   Get item 5: {r['data']['name']}")
r = app("POST", "/api/v1/items", name="Laptop", price="999.99")
print(f"   Create: {r['data']['name']} (${r['data']['price']})")

print("\n5. Admin routes:")
r = app("GET", "/admin/")
print(f"   Dashboard: {r['data']['stats']}")
r = app("GET", "/admin/users")
print(f"   Users: {len(r['data']['users'])}")

print("\n6. Auth login (POST):")
r = app("POST", "/auth/login", username="admin", password="secret")
print(f"   {r['data']['message']}")
r = app("POST", "/auth/login", username="admin", password="wrong")
print(f"   Bad login: {r['data']['error']}")
