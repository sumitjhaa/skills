"""Flash messages & sessions: temporary messages, session storage, cookie-based."""
from typing import Any, Optional
from datetime import datetime
import json
import uuid
import time


# ======================== Session & Flash System ========================

class Session:
    """Simulates Flask's session (cookie-based dict)."""
    def __init__(self):
        self._data: dict[str, Any] = {}
        self._modified = False
        self.session_id = str(uuid.uuid4())

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._modified = True

    def __delitem__(self, key):
        del self._data[key]
        self._modified = True

    def __contains__(self, key):
        return key in self._data

    def get(self, key, default=None):
        return self._data.get(key, default)

    def pop(self, key, default=None):
        self._modified = True
        return self._data.pop(key, default)

    def clear(self):
        self._data.clear()
        self._modified = True

    @property
    def modified(self) -> bool:
        return self._modified

    def to_dict(self) -> dict:
        return dict(self._data)


class Flash:
    """Simulates Flask's flash messaging system."""
    def __init__(self):
        self._messages: list[dict] = []

    def flash(self, message: str, category: str = "info"):
        self._messages.append({"message": message, "category": category, "timestamp": datetime.now().isoformat()})

    def get_messages(self) -> list[dict]:
        messages = list(self._messages)
        self._messages.clear()
        return messages

    def has_messages(self) -> bool:
        return len(self._messages) > 0

    @property
    def count(self) -> int:
        return len(self._messages)


class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.session = Session()
        self.flash = Flash()

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
                messages = self.flash.get_messages()
                if messages:
                    result["_flashes"] = messages
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()


# ======================== Routes ========================

@app.route("/")
def home():
    return {
        "message": "Flash Messages & Sessions Demo",
        "visit_count": app.session.get("visit_count", 0),
        "endpoints": ["/login", "/dashboard", "/logout", "/flash-demo", "/session-demo"],
    }


@app.route("/login", methods=["GET", "POST"])
def login(**kwargs):
    if kwargs:
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")

        if username == "admin" and password == "secret":
            app.session["user"] = username
            app.session["role"] = "admin"
            app.session["login_time"] = datetime.now().isoformat()
            app.flash.flash(f"Welcome back, {username}!", "success")
            return {"message": "Login successful", "redirect": "/dashboard"}

        app.flash.flash("Invalid credentials", "error")
        return {"message": "Login failed"}

    return {"message": "Login page", "form": {"username": "", "password": ""}}


@app.route("/dashboard")
def dashboard():
    user = app.session.get("user")
    if not user:
        app.flash.flash("Please log in first", "warning")
        return {"message": "Access denied", "redirect": "/login"}

    app.session["visit_count"] = app.session.get("visit_count", 0) + 1
    return {
        "message": f"Welcome to dashboard, {user}!",
        "user": user,
        "role": app.session.get("role"),
        "visit_count": app.session["visit_count"],
        "login_time": app.session.get("login_time"),
    }


@app.route("/logout")
def logout():
    user = app.session.get("user", "unknown")
    app.session.clear()
    app.flash.flash(f"Goodbye, {user}!", "info")
    return {"message": "Logged out", "redirect": "/"}


@app.route("/flash-demo")
def flash_demo():
    app.flash.flash("This is an info message", "info")
    app.flash.flash("This is a success message", "success")
    app.flash.flash("This is a warning message", "warning")
    app.flash.flash("This is an error message", "error")
    return {"message": "Flash messages created. They appear on the next request."}


@app.route("/session-demo")
def session_demo():
    # Counter
    count = app.session.get("counter", 0) + 1
    app.session["counter"] = count

    # Store some data
    app.session["last_visit"] = datetime.now().isoformat()
    app.session["items"] = ["apple", "banana", "cherry"]

    return {
        "session_id": app.session.session_id,
        "data": app.session.to_dict(),
        "counter": count,
    }


@app.route("/session-clear")
def session_clear():
    app.session.clear()
    app.flash.flash("Session cleared", "info")
    return {"message": "Session data cleared"}


@app.route("/cart/add")
def add_to_cart(**kwargs):
    item = kwargs.get("item", "unknown")
    cart = app.session.get("cart", [])
    cart.append(item)
    app.session["cart"] = cart
    app.flash.flash(f"Added '{item}' to cart", "success")
    return {"cart": cart, "item_count": len(cart)}


@app.route("/cart")
def view_cart():
    cart = app.session.get("cart", [])
    return {"cart": cart, "total": len(cart)}


# ======================== Demo ========================
print("=== Flash Messages & Sessions Demo ===\n")

# Visit counter
print("1. Session counter (visits):")
for i in range(3):
    r = app("GET", "/")
    print(f"   Visit {i+1}: count={r['data']['visit_count']}")

print("\n2. Login with wrong credentials:")
r = app("POST", "/login", username="admin", password="wrong")
print(f"   {r['data']['message']}")
for msg in r['data'].get('_flashes', []):
    print(f"   💬 [{msg['category']}] {msg['message']}")

print("\n3. Successful login:")
r = app("POST", "/login", username="admin", password="secret")
print(f"   {r['data']['message']}")
for msg in r['data'].get('_flashes', []):
    print(f"   💬 [{msg['category']}] {msg['message']}")

print("\n4. Dashboard (authenticated):")
r = app("GET", "/dashboard")
print(f"   User: {r['data']['user']}")
print(f"   Role: {r['data']['role']}")
print(f"   Visits: {r['data']['visit_count']}")

print("\n5. Add items to cart:")
for item in ["Laptop", "Mouse", "Keyboard"]:
    r = app("GET", "/cart/add", item=item)
    print(f"   Cart: {r['data']['cart']}")

print("\n6. View cart:")
r = app("GET", "/cart")
print(f"   Items: {r['data']['cart']}")
print(f"   Total: {r['data']['total']}")

print("\n7. Session data:")
r = app("GET", "/session-demo")
print(f"   Session ID: {r['data']['session_id'][:8]}...")
print(f"   Data: {json.dumps(r['data']['data'], indent=2)}")

print("\n8. Logout:")
r = app("GET", "/logout")
print(f"   {r['data']['message']}")
for msg in r['data'].get('_flashes', []):
    print(f"   💬 [{msg['category']}] {msg['message']}")

print("\n9. Dashboard after logout (access denied):")
r = app("GET", "/dashboard")
print(f"   {r['data']['message']}")
for msg in r['data'].get('_flashes', []):
    print(f"   💬 [{msg['category']}] {msg['message']}")
