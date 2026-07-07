"""Email authentication — login with email instead of username."""
from typing import Optional
import hashlib
import secrets


# ======================== Email-Only User Model ========================
USERS: dict[str, dict] = {}  # email → User
SESSION_STORE: dict[str, str] = {}  # session_id → email
PK = 1


class EmailUser:
    def __init__(self, email: str, display_name: str, password: str):
        global PK
        self.id = PK
        self.email = email
        self.display_name = display_name
        self.password_hash = self._hash(password)
        self.is_authenticated = False
        self.is_active = True
        self.date_joined = "2024-07-07"
        USERS[email] = self
        PK += 1

    def _hash(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


# ======================== Email Auth Backend ========================

class EmailAuthBackend:
    """
    Custom auth backend: authenticate by email + password.
    In Django, you'd add this to AUTHENTICATION_BACKENDS:
        AUTHENTICATION_BACKENDS = [
            'path.to.EmailAuthBackend',
            'django.contrib.auth.backends.ModelBackend',
        ]
    """

    def authenticate(self, request=None, email=None, password=None, **kwargs) -> Optional[EmailUser]:
        user = USERS.get(email)
        if user and user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id: int) -> Optional[EmailUser]:
        for user in USERS.values():
            if user.id == user_id:
                return user
        return None


# ======================== Registration Form ========================

class EmailSignupForm:
    errors: dict[str, list[str]] = {}

    def __init__(self, data: dict):
        self.data = data

    def is_valid(self) -> bool:
        self.errors = {}
        email = self.data.get("email", "").strip()
        name = self.data.get("display_name", "").strip()
        password = self.data.get("password", "")
        confirm = self.data.get("confirm_password", "")

        if "@" not in email or "." not in email:
            self.errors.setdefault("email", []).append("Invalid email address")
        if email in USERS:
            self.errors.setdefault("email", []).append("Email already registered")
        if len(name) < 1:
            self.errors.setdefault("display_name", []).append("Required")
        if len(password) < 6:
            self.errors.setdefault("password", []).append("Must be at least 6 characters")
        if password != confirm:
            self.errors.setdefault("confirm_password", []).append("Passwords don't match")

        return not bool(self.errors)

    def save(self) -> EmailUser:
        return EmailUser(
            email=self.data["email"],
            display_name=self.data["display_name"],
            password=self.data["password"],
        )


# ======================== Auth Helpers ========================

class AnonymousUser:
    is_authenticated = False
    is_active = False
    email = ""


def login(request: dict, user: EmailUser):
    sid = secrets.token_hex(16)
    SESSION_STORE[sid] = user.email
    user.is_authenticated = True
    request["session_id"] = sid
    request["user"] = user


def logout(request: dict):
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        email = SESSION_STORE.pop(sid)
        user = USERS.get(email)
        if user:
            user.is_authenticated = False
    request["user"] = AnonymousUser()
    request["session_id"] = None


def get_user(request: dict) -> EmailUser:
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        email = SESSION_STORE.get(sid)
        user = USERS.get(email)
        if user and user.is_active:
            return user
    return AnonymousUser()


# ======================== Views ========================

def signup_view(request: dict) -> dict:
    form = EmailSignupForm(request.get("post", {}))
    if form.is_valid():
        user = form.save()
        login(request, user)
        return {"status": 201, "message": f"Welcome, {user.display_name}!", "email": user.email}
    return {"status": 400, "errors": form.errors}


def login_view(request: dict) -> dict:
    email = request.get("post", {}).get("email", "")
    password = request.get("post", {}).get("password", "")
    backend = EmailAuthBackend()
    user = backend.authenticate(email=email, password=password)
    if user:
        login(request, user)
        return {"status": 200, "message": f"Welcome back, {user.display_name}!"}
    return {"status": 401, "error": "Invalid email or password"}


def logout_view(request: dict) -> dict:
    logout(request)
    return {"status": 200, "message": "Logged out"}


def profile_view(request: dict) -> dict:
    user = get_user(request)
    if not user.is_authenticated:
        return {"status": 401, "error": "Login required"}
    return {
        "status": 200,
        "email": user.email,
        "display_name": user.display_name,
    }


# ======================== Demo ========================
print("=== Email Authentication Demo ===")

# Signup with email
req1: dict = {"post": {"email": "alice@example.com",
                        "display_name": "Alice",
                        "password": "secret123",
                        "confirm_password": "secret123"}}
print(f"Signup: {signup_view(req1)}")

# Duplicate email
print(f"Duplicate: {signup_view(req1)}")

# Login
login_req: dict = {"post": {"email": "alice@example.com", "password": "secret123"}}
print(f"Login: {login_view(login_req)}")

# Bad password
bad_login: dict = {"post": {"email": "alice@example.com", "password": "wrong"}}
print(f"Bad login: {login_view(bad_login)}")

# Profile
print(f"Profile: {profile_view(req1)}")

# Login nonexistent email
nope: dict = {"post": {"email": "nobody@example.com", "password": "x"}}
print(f"Nonexistent: {login_view(nope)}")
