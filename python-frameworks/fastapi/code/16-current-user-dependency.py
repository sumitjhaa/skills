"""Current user dependency pattern: reusable auth extraction, dependency chaining."""
from typing import Any, Optional
import json
import hmac
import hashlib
import base64
import time


# ======================== JWT helpers ========================

JWT_SECRET = "dependency-secret"
JWT_ALGORITHM = "HS256"


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def create_jwt(payload: dict) -> str:
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = payload.copy()
    payload["iat"] = int(time.time())
    payload["exp"] = int(time.time()) + 3600
    h_b64 = base64url_encode(json.dumps(header).encode())
    p_b64 = base64url_encode(json.dumps(payload).encode())
    sig = hmac.new(JWT_SECRET.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()
    return f"{h_b64}.{p_b64}.{base64url_encode(sig)}"


def verify_jwt(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        h_b64, p_b64, s_b64 = parts
        expected = hmac.new(JWT_SECRET.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, base64url_decode(s_b64)):
            return None
        payload = json.loads(base64url_decode(p_b64))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


# ======================== User Store ========================

class UserDB:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self._next_id = 1

    def create(self, username: str, email: str, role: str = "user") -> dict:
        u = {"id": self._next_id, "username": username, "email": email, "role": role, "active": True}
        self.users[self._next_id] = u
        self._next_id += 1
        return u

    def get_by_id(self, uid: int) -> Optional[dict]:
        return self.users.get(uid)


db = UserDB()
db.create("alice", "alice@example.com", "admin")
db.create("bob", "bob@example.com", "user")
db.create("charlie", "charlie@example.com", "user")


# ======================== Dependency Simulation ========================

class Depends:
    """Simulates FastAPI's Depends — wraps a callable as a dependency."""
    def __init__(self, dependency):
        self.dependency = dependency


class DependsResolver:
    """Resolves dependency chains."""
    def __init__(self):
        self._cache: dict[str, Any] = {}

    def resolve(self, dep, **provided) -> Any:
        if isinstance(dep, Depends):
            return self._resolve_func(dep.dependency, **provided)
        return dep

    def _resolve_func(self, func, **provided) -> Any:
        import inspect
        sig = inspect.signature(func)
        kwargs = {}
        for name, param in sig.parameters.items():
            if name in provided:
                kwargs[name] = provided[name]
            elif isinstance(param.default, Depends):
                kwargs[name] = self._resolve_func(param.default.dependency, **provided)
        return func(**kwargs)


resolver = DependsResolver()


# ======================== Dependencies ========================

def get_authorization_header(authorization: str = "") -> str:
    """Extract Bearer token from Authorization header."""
    if not authorization.startswith("Bearer "):
        return ""
    return authorization[7:]


def get_token_payload(token: str = Depends(get_authorization_header)) -> Optional[dict]:
    """Verify JWT and return payload."""
    if not token:
        return None
    payload = verify_jwt(token)
    if payload is None:
        return None
    return payload


def get_current_user(payload: Optional[dict] = Depends(get_token_payload)) -> Optional[dict]:
    """Get current user from token payload."""
    if payload is None:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.get_by_id(user_id)


def get_current_active_user(current_user: Optional[dict] = Depends(get_current_user)) -> Optional[dict]:
    """Ensure user is active."""
    if current_user is None or not current_user.get("active"):
        return None
    return current_user


def require_role(role: str):
    """Factory that returns a dependency checking for a specific role."""
    def role_checker(current_user: dict = Depends(get_current_active_user)):
        if current_user is None:
            return None
        if current_user["role"] != role:
            return None
        return current_user
    return role_checker


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.get("/users/me")
def read_me(current_user: dict = Depends(get_current_active_user)):
    if current_user is None:
        return {"error": "Not authenticated"}
    return {"id": current_user["id"], "username": current_user["username"], "role": current_user["role"]}


@app.get("/users/me/email")
def read_email(current_user: dict = Depends(get_current_user)):
    if current_user is None:
        return {"error": "Not authenticated"}
    return {"email": current_user["email"]}


@app.get("/admin/dashboard")
def admin_dashboard(admin: dict = Depends(require_role("admin"))):
    if admin is None:
        return {"error": "Admin access required"}
    return {"dashboard": "Admin panel", "admin": admin["username"]}


@app.get("/public")
def public_endpoint():
    return {"message": "This is public", "access": "anyone"}


# ======================== Demo ========================
print("=== Current User Dependency Demo ===\n")

# Create tokens for different users
alice_token = create_jwt({"sub": 1, "username": "alice"})
bob_token = create_jwt({"sub": 2, "username": "bob"})
charlie_token = create_jwt({"sub": 3, "username": "charlie"})

print("1. Public endpoint (no auth):")
result = app("GET", "/public")
print(f"   {result['data']}\n")

print("2. Alice reads own profile (active admin):")
result = app("GET", "/users/me", authorization=f"Bearer {alice_token}")
print(f"   {result['data']}\n")

print("3. Bob reads own profile (active user):")
result = app("GET", "/users/me", authorization=f"Bearer {bob_token}")
print(f"   {result['data']}\n")

print("4. Unauthenticated access to /users/me:")
result = app("GET", "/users/me")
print(f"   {result['data']}\n")

print("5. Alice accesses admin dashboard (admin role):")
result = app("GET", "/admin/dashboard", authorization=f"Bearer {alice_token}")
print(f"   {result['data']}\n")

print("6. Bob tries admin dashboard (user role):")
result = app("GET", "/admin/dashboard", authorization=f"Bearer {bob_token}")
print(f"   {result['data']}\n")

print("7. Charlie reads own email (via get_current_user dependency):")
result = app("GET", "/users/me/email", authorization=f"Bearer {charlie_token}")
print(f"   {result['data']}\n")

# Dependency chain visualization
print("8. Dependency chain for /users/me:")
print("   get_authorization_header")
print("       ↓")
print("   get_token_payload  (Depends: get_authorization_header)")
print("       ↓")
print("   get_current_user  (Depends: get_token_payload)")
print("       ↓")
print("   get_current_active_user  (Depends: get_current_user)")
print("       ↓")
print("   ✅ Protected endpoint")
