"""User authentication: Flask-Login, password hashing, login/logout, current_user."""
from typing import Any, Optional
from datetime import datetime
import json
import hashlib
import uuid


# ======================== Password Hashing ========================

def hash_password(password: str) -> str:
    salt = uuid.uuid4().hex[:16]
    return f"{salt}${hashlib.sha256(f'{salt}:{password}'.encode()).hexdigest()}"

def verify_password(password: str, hashed: str) -> bool:
    if "$" not in hashed:
        return False
    salt, h = hashed.split("$", 1)
    return h == hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()


# ======================== User Mixin ========================

class UserMixin:
    """Simulates Flask-Login's UserMixin."""
    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)


class LoginManager:
    """Simulates Flask-Login's LoginManager."""
    def __init__(self):
        self._user_callback = None
        self._unauthorized_callback = None

    def user_loader(self, func):
        self._user_callback = func
        return func

    def unauthorized_handler(self, func):
        self._unauthorized_callback = func
        return func

    def load_user(self, user_id: str) -> Optional[UserMixin]:
        if self._user_callback:
            return self._user_callback(user_id)
        return None

    def unauthorized(self):
        if self._unauthorized_callback:
            return self._unauthorized_callback()
        return {"error": "Unauthorized"}

login_manager = LoginManager()


def login_required(func):
    """Simulates Flask-Login's @login_required decorator."""
    def wrapper(*args, **kwargs):
        if "current_user" not in kwargs or kwargs["current_user"].is_anonymous:
            return login_manager.unauthorized()
        return func(*args, **kwargs)
    return wrapper


# ======================== User Store ========================

class UserStore:
    def __init__(self):
        self.users: dict[int, UserMixin] = {}
        self._next = 1

    def create(self, username: str, email: str, password: str) -> UserMixin:
        user = type("User", (UserMixin,), {})()
        user.id = self._next
        user.username = username
        user.email = email
        user.password_hash = hash_password(password)
        self.users[self._next] = user
        self._next += 1
        return user

    def get_by_id(self, uid: int) -> Optional[UserMixin]:
        return self.users.get(uid)

    def get_by_username(self, username: str) -> Optional[UserMixin]:
        for u in self.users.values():
            if u.username == username:
                return u
        return None

    def authenticate(self, username: str, password: str) -> Optional[UserMixin]:
        user = self.get_by_username(username)
        if user and verify_password(password, user.password_hash):
            return user
        return None

store = UserStore()


@login_manager.user_loader
def load_user(user_id: str):
    return store.get_by_id(int(user_id))


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path: str, methods: list[str] | None = None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    def __call__(self, method: str, path: str, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Auth Routes ========================

@app.route("/register", methods=["POST"])
def register(**kw):
    username = kw.get("username", "")
    if store.get_by_username(username):
        return {"error": "Username taken"}
    user = store.create(username, kw.get("email", ""), kw.get("password", ""))
    return {"id": user.id, "username": user.username, "email": user.email}

@app.route("/login", methods=["POST"])
def login(**kw):
    user = store.authenticate(kw.get("username", ""), kw.get("password", ""))
    if not user:
        return {"error": "Invalid credentials"}
    return {"message": "Login successful", "user_id": user.id, "username": user.username}

@app.route("/profile")
@login_required
def profile(current_user = None, **kw):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}

@app.route("/admin")
@login_required
def admin_panel(current_user = None, **kw):
    return {"message": f"Admin panel for {current_user.username}", "users": [{"id": u.id, "username": u.username} for u in store.users.values()]}


# ======================== Demo ========================
print("=== User Auth Demo ===\n")

print("1. Register users:")
for name, email, pw in [("alice", "alice@test.com", "secret123"), ("bob", "bob@test.com", "pass456")]:
    r = app("POST", "/register", username=name, email=email, password=pw)
    print(f"   Registered: {r['data']['username']} (id={r['data']['id']})")

print("\n2. Login:")
r = app("POST", "/login", username="alice", password="secret123")
print(f"   {r['data']['message']}")

print("\n3. Bad login:")
r = app("POST", "/login", username="alice", password="wrong")
print(f"   {r['data']['error']}")

print("\n4. Profile (via login_required):")
# Simulate passing current_user to the handler
alice = store.get_by_username("alice")
r = app("GET", "/profile", current_user=alice)
print(f"   {json.dumps(r['data'])}")

print("\n5. Profile without auth:")
anon = type("AnonUser", (object,), {"is_anonymous": True, "get_id": lambda: "0"})()
r = app("GET", "/profile", current_user=anon)
print(f"   {r['data']}")

print("\n6. Admin panel (authenticated):")
r = app("GET", "/admin", current_user=alice)
print(f"   {r['data']['message']}")
for u in r["data"]["users"]:
    print(f"   - {u['username']} (id={u['id']})")

print("\n7. Password security:")
print(f"   alice's hash: {alice.password_hash[:20]}...")
print(f"   verify('secret123'): {verify_password('secret123', alice.password_hash)}")
print(f"   verify('wrong'):     {verify_password('wrong', alice.password_hash)}")
