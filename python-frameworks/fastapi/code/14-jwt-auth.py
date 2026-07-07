"""JWT authentication: token creation, verification, expiration, protected endpoints."""
from typing import Any, Optional
from datetime import datetime, timedelta
import json
import hmac
import hashlib
import base64
import time


# ======================== JWT Implementation ========================

JWT_SECRET = "super-secret-key-change-in-production"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30


def base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def base64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def create_jwt(payload: dict, secret: str = JWT_SECRET) -> str:
    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}

    # Add standard claims
    payload = payload.copy()
    payload.setdefault("iat", int(time.time()))
    payload.setdefault("exp", int(time.time()) + JWT_EXPIRATION_MINUTES * 60)

    # Encode header and payload
    header_b64 = base64url_encode(json.dumps(header).encode())
    payload_b64 = base64url_encode(json.dumps(payload).encode())

    # Create signature
    message = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(secret.encode(), message, hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def verify_jwt(token: str, secret: str = JWT_SECRET) -> Optional[dict]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None

        header_b64, payload_b64, signature_b64 = parts

        # Verify signature
        message = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(secret.encode(), message, hashlib.sha256).digest()
        actual_sig = base64url_decode(signature_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        # Decode payload
        payload = json.loads(base64url_decode(payload_b64))

        # Check expiration
        if payload.get("exp", 0) < time.time():
            return None

        return payload
    except Exception:
        return None


def decode_jwt(token: str) -> Optional[dict]:
    """Decode without verification (for debugging)."""
    try:
        parts = token.split(".")
        payload = json.loads(base64url_decode(parts[1]))
        return payload
    except Exception:
        return None


# ======================== User Store ========================

class UserDB:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self._next_id = 1

    def create(self, username: str, password: str, role: str = "user") -> dict:
        user = {
            "id": self._next_id,
            "username": username,
            "password": password,
            "role": role,
        }
        self.users[self._next_id] = user
        self._next_id += 1
        return user

    def get_by_username(self, username: str) -> Optional[dict]:
        for user in self.users.values():
            if user["username"] == username:
                return user
        return None

    def get_by_id(self, user_id: int) -> Optional[dict]:
        return self.users.get(user_id)


db = UserDB()


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def post(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return decorator

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


app = FastAPI()


# ======================== Auth Endpoints ========================

@app.post("/auth/register")
def register(username: str, password: str):
    existing = db.get_by_username(username)
    if existing:
        return {"error": "Username already exists"}
    user = db.create(username, password)
    token = create_jwt({"sub": user["id"], "username": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer", "user_id": user["id"]}


@app.post("/auth/login")
def login(username: str, password: str):
    user = db.get_by_username(username)
    if not user or user["password"] != password:
        return {"error": "Invalid credentials"}
    token = create_jwt({"sub": user["id"], "username": user["username"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me")
def get_current_user(authorization: str = ""):
    if not authorization.startswith("Bearer "):
        return {"error": "Missing or invalid authorization header"}
    token = authorization[7:]
    payload = verify_jwt(token)
    if payload is None:
        return {"error": "Invalid or expired token"}
    user = db.get_by_id(payload["sub"])
    if not user:
        return {"error": "User not found"}
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


@app.get("/auth/verify")
def verify_token(authorization: str = ""):
    if not authorization.startswith("Bearer "):
        return {"valid": False, "error": "No token"}
    token = authorization[7:]
    payload = verify_jwt(token)
    if payload is None:
        return {"valid": False, "error": "Invalid or expired"}
    return {"valid": True, "sub": payload["sub"], "exp": payload.get("exp")}


# ======================== Demo ========================
print("=== JWT Authentication Demo ===\n")

# Register
print("1. Register new user:")
reg = app("POST", "/auth/register", username="alice", password="secret123")
print(f"   {json.dumps(reg['data'], indent=2)}\n")

# Login
print("2. Login:")
login = app("POST", "/auth/login", username="alice", password="secret123")
token = login["data"]["access_token"]
print(f"   Access token: {token[:50]}...\n")

# Decode token (inspect payload)
print("3. Decoded token payload:")
decoded = decode_jwt(token)
print(f"   {json.dumps(decoded, indent=2)}\n")

# Get current user
print("4. Get current user (valid token):")
me = app("GET", "/auth/me", authorization=f"Bearer {token}")
print(f"   {me['data']}\n")

# Invalid token
print("5. Get current user (invalid token):")
me_invalid = app("GET", "/auth/me", authorization="Bearer invalid_token_here")
print(f"   {me_invalid['data']}\n")

# Verify token
print("6. Verify valid token:")
verify = app("GET", "/auth/verify", authorization=f"Bearer {token}")
print(f"   {verify['data']}\n")

# Wrong password
print("7. Login with wrong password:")
bad_login = app("POST", "/auth/login", username="alice", password="wrong")
print(f"   {bad_login['data']}\n")

# Expired token simulation
print("8. Simulate expired token:")
expired_token = create_jwt({"sub": 1, "username": "alice", "role": "user", "exp": int(time.time()) - 3600})
verify_expired = app("GET", "/auth/verify", authorization=f"Bearer {expired_token}")
print(f"   {verify_expired['data']}")
