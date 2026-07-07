"""Registration, profile model, signup form, and profile views."""
from typing import Optional
import hashlib
import secrets
import re


# ======================== Data Store ========================
USERS: dict[int, dict] = {}
PROFILES: dict[int, dict] = {}
SESSION_STORE: dict[str, int] = {}
PK = 1


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ======================== User Model ========================
class User:
    def __init__(self, username: str, email: str, password: str):
        global PK
        self.id = PK
        self.username = username
        self.email = email
        self.password_hash = _hash(password)
        self.is_authenticated = False
        self.is_active = True
        self.date_joined = "2024-07-07"
        USERS[PK] = self
        PK += 1

    def check_password(self, password: str) -> bool:
        return self.password_hash == _hash(password)


# ======================== Profile Model ========================
class Profile:
    def __init__(self, user: User, bio: str = "", avatar: str = "", location: str = "", website: str = ""):
        self.user_id = user.id
        self.bio = bio
        self.avatar = avatar
        self.location = location
        self.website = website
        PROFILES[user.id] = self

    def __repr__(self) -> str:
        return f"<Profile for user #{self.user_id}>"


# ======================== Signup Form (Validation) ========================
class SignupForm:
    """Simulates Django ModelForm + validation."""

    errors: dict[str, list[str]] = {}
    cleaned_data: dict = {}

    def __init__(self, data: dict):
        self.data = data
        self.errors = {}
        self.cleaned_data = {}

    def is_valid(self) -> bool:
        self.errors = {}
        username = self.data.get("username", "").strip()
        email = self.data.get("email", "").strip()
        password = self.data.get("password", "")
        confirm = self.data.get("confirm_password", "")

        if len(username) < 3:
            self.errors.setdefault("username", []).append("Must be at least 3 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            self.errors.setdefault("username", []).append("Only letters, numbers, underscore")
        for u in USERS.values():
            if u.username == username:
                self.errors.setdefault("username", []).append("Already taken")
                break

        if "@" not in email:
            self.errors.setdefault("email", []).append("Invalid email address")
        for u in USERS.values():
            if u.email == email:
                self.errors.setdefault("email", []).append("Already registered")
                break

        if len(password) < 6:
            self.errors.setdefault("password", []).append("Must be at least 6 characters")
        if password != confirm:
            self.errors.setdefault("confirm_password", []).append("Passwords don't match")

        if not self.errors:
            self.cleaned_data = {"username": username, "email": email, "password": password}
        return not bool(self.errors)


class ProfileForm:
    errors: dict[str, list[str]] = {}

    def __init__(self, data: dict):
        self.data = data

    def is_valid(self) -> bool:
        self.errors = {}
        return not bool(self.errors)

    def save(self, profile: Profile) -> Profile:
        profile.bio = self.data.get("bio", profile.bio)
        profile.location = self.data.get("location", profile.location)
        profile.website = self.data.get("website", profile.website)
        return profile


# ======================== Auth Helpers ========================

class AnonymousUser:
    is_authenticated = False
    is_active = False
    username = "Anonymous"
    id = None


def authenticate(username: str, password: str) -> Optional[User]:
    for user in USERS.values():
        if user.username == username and user.check_password(password):
            return user
    return None


def login(request: dict, user: User):
    sid = secrets.token_hex(16)
    SESSION_STORE[sid] = user.id
    user.is_authenticated = True
    request["session_id"] = sid
    request["user"] = user


def get_user(request: dict) -> User:
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        user = USERS.get(SESSION_STORE[sid])
        if user and user.is_active:
            return user
    return AnonymousUser()


# ======================== Views ========================

def signup_view(request: dict) -> dict:
    data = request.get("post", {})
    form = SignupForm(data)
    if form.is_valid():
        cd = form.cleaned_data
        user = User(cd["username"], cd["email"], cd["password"])
        profile = Profile(user, bio=f"Hello, I'm {user.username}!")
        login(request, user)
        return {"status": 201, "message": f"Welcome, {user.username}!", "user_id": user.id}
    return {"status": 400, "errors": form.errors}


def profile_view(request: dict) -> dict:
    user = get_user(request)
    if not user.is_authenticated:
        return {"status": 401, "error": "Login required"}
    profile = PROFILES.get(user.id)
    return {
        "status": 200,
        "user": user.username,
        "email": user.email,
        "bio": profile.bio if profile else "",
        "location": profile.location if profile else "",
    }


def edit_profile_view(request: dict) -> dict:
    user = get_user(request)
    if not user.is_authenticated:
        return {"status": 401, "error": "Login required"}
    profile = PROFILES.get(user.id)
    if not profile:
        profile = Profile(user)
    form = ProfileForm(request.get("post", {}))
    if form.is_valid():
        form.save(profile)
        return {"status": 200, "message": "Profile updated"}
    return {"status": 400, "errors": form.errors}


def login_view(request: dict) -> dict:
    username = request.get("post", {}).get("username", "")
    password = request.get("post", {}).get("password", "")
    user = authenticate(username, password)
    if user:
        login(request, user)
        return {"status": 200, "message": f"Welcome back, {user.username}!"}
    return {"status": 401, "error": "Invalid credentials"}


# ======================== Demo ========================
print("=== Registration & Profile Demo ===")

# Signup
req1: dict = {"post": {"username": "charlie", "email": "charlie@example.com",
                        "password": "pass123", "confirm_password": "pass123"}}
print(f"Signup: {signup_view(req1)}")

# Duplicate signup
print(f"Duplicate signup: {signup_view(req1)}")

# Invalid signup
bad_req: dict = {"post": {"username": "ab", "email": "bad",
                           "password": "12", "confirm_password": "34"}}
print(f"Bad signup: {signup_view(bad_req)}")

# View profile
print(f"Profile: {profile_view(req1)}")

# Edit profile
edit_req: dict = {"session_id": req1["session_id"], "user": req1["user"],
                   "post": {"bio": "Python developer", "location": "NYC"}}
print(f"Edit profile: {edit_profile_view(edit_req)}")
print(f"Updated profile: {profile_view(edit_req)}")

# Login existing user
login_req: dict = {"post": {"username": "alice", "password": "secret123"}}
print(f"Login: {login_view(login_req)}")
