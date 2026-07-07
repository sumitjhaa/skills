"""OAuth2 password flow: /token endpoint, password hashing, scopes."""
from typing import Any, Optional
from datetime import datetime
import json
import hmac
import hashlib
import base64
import time


# ======================== Password Hashing ========================

def hash_password(password: str) -> str:
    """Simple password hashing (simulating bcrypt)."""
    salt = "fastapi_salt"
    return hashlib.sha256(f"{password}:{salt}".encode()).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


# ======================== JWT (same as lesson 14) ========================

JWT_SECRET = "oauth2-secret-key"
JWT_ALGORITHM = "HS256"


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def create_jwt(payload: dict, expires_minutes: int = 30) -> str:
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    payload = payload.copy()
    payload["iat"] = int(time.time())
    payload["exp"] = int(time.time()) + expires_minutes * 60
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())
    message = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(JWT_SECRET.encode(), message, hashlib.sha256).digest()
    return f"{header_b64}.{payload_b64}.{base64url_encode(signature)}"


def verify_jwt(token: str) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, signature_b64 = parts
        message = f"{header_b64}.{payload_b64}".encode()
        expected = hmac.new(JWT_SECRET.encode(), message, hashlib.sha256).digest()
        actual = base64url_decode(signature_b64)
        if not hmac.compare_digest(expected, actual):
            return None
        payload = json.loads(base64url_decode(payload_b64))
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

    def create(self, username: str, password: str, scopes: str = "read") -> dict:
        user = {
            "id": self._next_id,
            "username": username,
            "password": hash_password(password),
            "scopes": scopes,
            "disabled": False,
        }
        self.users[self._next_id] = user
        self._next_id += 1
        return user

    def get_by_username(self, username: str) -> Optional[dict]:
        for u in self.users.values():
            if u["username"] == username:
                return u
        return None

    def get_by_id(self, uid: int) -> Optional[dict]:
        return self.users.get(uid)


db = UserDB()


# ======================== OAuth2 /token endpoint ========================

class TokenEndpoint:
    """Simulates the OAuth2 /token endpoint with grant_type=password."""
    def __call__(self, grant_type: str = "password", username: str = "", password: str = "", scope: str = ""):
        if grant_type != "password":
            return {"error": "unsupported_grant_type", "error_description": "Only password grant is supported"}

        user = db.get_by_username(username)
        if not user or not verify_password(password, user["password"]):
            return {"error": "invalid_grant", "error_description": "Invalid username or password"}

        if user.get("disabled"):
            return {"error": "access_denied", "error_description": "User account is disabled"}

        access_token = create_jwt({
            "sub": user["id"],
            "username": user["username"],
            "scopes": scope or user["scopes"],
        })
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "scope": scope or user["scopes"],
        }


token_endpoint = TokenEndpoint()


# ======================== Scoped Endpoints ========================

def require_scopes(required_scopes: list[str]):
    """Decorator-like scope checker."""
    def check(authorization: str = "") -> dict | None:
        if not authorization.startswith("Bearer "):
            return {"error": "not_authenticated", "detail": "Missing token"}
        token = authorization[7:]
        payload = verify_jwt(token)
        if payload is None:
            return {"error": "invalid_token", "detail": "Invalid or expired"}
        user_scopes = payload.get("scopes", "").split()
        for required in required_scopes:
            if required not in user_scopes:
                return {"error": "insufficient_scope", "detail": f"Requires scope: {required}"}
        return payload
    return check


class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

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

@app.post("/token")
def login_for_token(grant_type: str = "password", username: str = "", password: str = "", scope: str = ""):
    return token_endpoint(grant_type=grant_type, username=username, password=password, scope=scope)


@app.get("/users/me")
def read_current_user(authorization: str = ""):
    payload = require_scopes(["read"])(authorization=authorization)
    if isinstance(payload, dict) and "error" in payload:
        return payload
    user = db.get_by_id(payload["sub"])
    return {"id": user["id"], "username": user["username"], "scopes": user["scopes"]}


@app.get("/users/me/items")
def read_own_items(authorization: str = ""):
    payload = require_scopes(["read", "write"])(authorization=authorization)
    if isinstance(payload, dict) and "error" in payload:
        return payload
    return {"items": [{"id": 1, "name": "Item 1", "owner": payload["username"]}]}


@app.post("/admin/users")
def admin_create_user(authorization: str = ""):
    payload = require_scopes(["admin"])(authorization=authorization)
    if isinstance(payload, dict) and "error" in payload:
        return payload
    return {"success": True, "action": "admin:create_user", "by": payload["username"]}


# ======================== Demo ========================
print("=== OAuth2 Password Flow Demo ===\n")

# Create users with different scopes
db.create("alice", "password1", scopes="read")
db.create("bob", "password2", scopes="read write")
db.create("admin_user", "admin_pass", scopes="read write admin")

# Login as alice (read only)
print("1. Alice logs in (scope: read):")
alice_token_data = app("POST", "/token", grant_type="password", username="alice", password="password1", scope="read")
alice_token = alice_token_data["data"]["access_token"]
print(f"   Token: {alice_token[:50]}...\n")

# Login as bob (read + write)
print("2. Bob logs in (scope: read write):")
bob_token_data = app("POST", "/token", grant_type="password", username="bob", password="password2", scope="read write")
bob_token = bob_token_data["data"]["access_token"]
print(f"   Token: {bob_token[:50]}...\n")

# Login as admin
print("3. Admin logs in (scope: admin):")
admin_token_data = app("POST", "/token", grant_type="password", username="admin_user", password="admin_pass", scope="admin")
admin_token = admin_token_data["data"]["access_token"]
print(f"   Token: {admin_token[:50]}...\n")

# Test scope enforcement
print("4. Alice reads own profile (scope: read needed):")
alice_me = app("GET", "/users/me", authorization=f"Bearer {alice_token}")
print(f"   {alice_me['data']}\n")

print("5. Alice tries to write (needs write scope):")
alice_items = app("GET", "/users/me/items", authorization=f"Bearer {alice_token}")
print(f"   {alice_items['data']}\n")

print("6. Bob writes (has read+write):")
bob_items = app("GET", "/users/me/items", authorization=f"Bearer {bob_token}")
print(f"   {bob_items['data']}\n")

print("7. Alice tries admin action:")
alice_admin = app("POST", "/admin/users", authorization=f"Bearer {alice_token}")
print(f"   {alice_admin['data']}\n")

print("8. Admin does admin action:")
admin_action = app("POST", "/admin/users", authorization=f"Bearer {admin_token}")
print(f"   {admin_action['data']}\n")

print("9. Wrong credentials:")
bad_login = app("POST", "/token", grant_type="password", username="alice", password="wrong")
print(f"   {bad_login['data']}")
