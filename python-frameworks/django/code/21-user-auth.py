"""User model & authentication: authenticate(), login(), logout(), request.user."""
from typing import Optional
import hashlib
import secrets


# ======================== Simulated User Model ========================
USERS: dict[int, dict] = {}
SESSION_STORE: dict[str, int] = {}  # session_id → user_id
PK = 1


class User:
    def __init__(self, username: str, email: str, password: str):
        global PK
        self.id = PK
        self.username = username
        self.email = email
        self.password_hash = self._hash(password)
        self.is_authenticated = False
        self.is_active = True
        USERS[PK] = self
        PK += 1

    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _check_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<User: {self.username} (id={self.id})>"


# Pre-create users
alice = User("alice", "alice@example.com", "secret123")
bob = User("bob", "bob@example.com", "password456")


# ======================== Auth Functions ========================

class AnonymousUser:
    is_authenticated = False
    is_active = False
    username = "Anonymous"
    id = None


def authenticate(username: str = None, email: str = None, password: str = None) -> Optional[User]:
    """Check credentials, return User or None."""
    for user in USERS.values():
        if username and user.username != username:
            continue
        if email and user.email != email:
            continue
        if user._check_password(password):
            return user
    return None


def login(request: dict, user: User) -> str:
    """Create a session. Returns session_id."""
    session_id = secrets.token_hex(16)
    SESSION_STORE[session_id] = user.id
    user.is_authenticated = True
    request["session_id"] = session_id
    request["user"] = user
    return session_id


def logout(request: dict):
    """Destroy session."""
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        user_id = SESSION_STORE.pop(sid)
        user = USERS.get(user_id)
        if user:
            user.is_authenticated = False
    request["user"] = AnonymousUser()
    request["session_id"] = None


def get_user(request: dict) -> User:
    """Resolve user from session."""
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        user = USERS.get(SESSION_STORE[sid])
        if user and user.is_active:
            return user
    return AnonymousUser()


def login_required(view_func):
    """Decorator: redirect to login if not authenticated."""
    def wrapper(request: dict, *args, **kwargs):
        user = get_user(request)
        if not user.is_authenticated:
            return {"status": 302, "location": "/login/", "error": "Login required"}
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ======================== Views ========================

def login_view(request: dict) -> dict:
    """Handle login form submission."""
    username = request.get("post", {}).get("username", "")
    password = request.get("post", {}).get("password", "")
    user = authenticate(username=username, password=password)
    if user:
        session_id = login(request, user)
        return {
            "status": 200,
            "message": f"Welcome, {user.username}!",
            "session_id": session_id,
        }
    return {"status": 401, "error": "Invalid credentials"}


def logout_view(request: dict) -> dict:
    logout(request)
    return {"status": 200, "message": "Logged out"}


def profile_view(request: dict) -> dict:
    user = get_user(request)
    if not user.is_authenticated:
        return {"status": 401, "error": "Login required"}
    return {
        "status": 200,
        "user": user.username,
        "email": user.email,
        "id": user.id,
    }


@login_required
def dashboard_view(request: dict) -> dict:
    user = get_user(request)
    return {
        "status": 200,
        "message": f"Welcome to your dashboard, {user.username}!",
    }


# ======================== Demo ========================
print("=== Authentication Demo ===")

# Anonymous access
anon_req: dict = {}
print(f"\nAnonymous dashboard: {dashboard_view(anon_req)}")

# Login
login_req: dict = {"post": {"username": "alice", "password": "secret123"}}
login_result = login_view(login_req)
print(f"\nLogin: {login_result}")

# Authenticated access
print(f"\nAuthenticated dashboard: {dashboard_view(login_req)}")

# Profile
print(f"\nProfile: {profile_view(login_req)}")

# Logout
print(f"\nLogout: {logout_view(login_req)}")

# After logout
print(f"\nAfter logout dashboard: {dashboard_view(login_req)}")

# Bad login
bad_req: dict = {"post": {"username": "alice", "password": "wrong"}}
print(f"\nBad login: {login_view(bad_req)}")
