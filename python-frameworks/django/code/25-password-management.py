"""Password management: change, reset, email flow."""
from typing import Optional
import hashlib
import secrets
import re


# ======================== Data Store ========================
USERS: dict[int, dict] = {}
RESET_TOKENS: dict[str, int] = {}  # token → user_id
SESSION_STORE: dict[str, int] = {}
PK = 1


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ======================== User ========================
class User:
    def __init__(self, username: str, email: str, password: str):
        global PK
        self.id = PK
        self.username = username
        self.email = email
        self.password_hash = _hash(password)
        self.is_authenticated = False
        self.is_active = True
        USERS[PK] = self
        PK += 1

    def check_password(self, password: str) -> bool:
        return self.password_hash == _hash(password)

    def set_password(self, password: str):
        self.password_hash = _hash(password)


# Pre-create
alice = User("alice", "alice@example.com", "oldpass123")
bob = User("bob", "bob@example.com", "secret456")


class AnonymousUser:
    is_authenticated = False
    is_active = False


# ======================== Password Change ========================

class PasswordChangeForm:
    """Simulates Django's PasswordChangeForm."""

    errors: dict[str, list[str]] = {}

    def __init__(self, user: User, data: dict):
        self.user = user
        self.data = data

    def is_valid(self) -> bool:
        self.errors = {}
        old = self.data.get("old_password", "")
        new = self.data.get("new_password", "")
        confirm = self.data.get("confirm_password", "")

        if not self.user.check_password(old):
            self.errors.setdefault("old_password", []).append("Wrong password")
        if len(new) < 6:
            self.errors.setdefault("new_password", []).append("Must be at least 6 characters")
        if new != confirm:
            self.errors.setdefault("confirm_password", []).append("Passwords don't match")
        if new == old:
            self.errors.setdefault("new_password", []).append("Must be different from old password")

        return not bool(self.errors)

    def save(self):
        self.user.set_password(self.data["new_password"])


# ======================== Password Reset ========================

def send_reset_email(user: User) -> str:
    """Generate and return a reset token (simulating email send)."""
    token = secrets.token_urlsafe(32)
    RESET_TOKENS[token] = user.id
    return token


def validate_reset_token(token: str) -> Optional[User]:
    """Validate token and return user, or None if invalid."""
    user_id = RESET_TOKENS.get(token)
    if user_id and user_id in USERS:
        return USERS[user_id]
    return None


def reset_password(token: str, new_password: str) -> bool:
    """Complete password reset."""
    user = validate_reset_token(token)
    if not user:
        return False
    user.set_password(new_password)
    del RESET_TOKENS[token]  # token is single-use
    return True


# ======================== Views ========================

def password_change_view(request: dict) -> dict:
    user = request.get("user")
    if not user or not user.is_authenticated:
        return {"status": 401, "error": "Login required"}

    form = PasswordChangeForm(user, request.get("post", {}))
    if form.is_valid():
        form.save()
        return {"status": 200, "message": "Password changed successfully"}
    return {"status": 400, "errors": form.errors}


def password_reset_request_view(request: dict) -> dict:
    """Step 1: Request password reset (email)."""
    email = request.get("post", {}).get("email", "")
    for user in USERS.values():
        if user.email == email:
            token = send_reset_email(user)
            return {
                "status": 200,
                "message": "Reset link sent (simulated)",
                "token": token,
            }
    return {"status": 404, "error": "Email not found"}


def password_reset_confirm_view(request: dict) -> dict:
    """Step 2: Submit new password with token."""
    token = request.get("post", {}).get("token", "")
    new_password = request.get("post", {}).get("new_password", "")
    confirm = request.get("post", {}).get("confirm_password", "")

    if len(new_password) < 6:
        return {"status": 400, "error": "Password too short"}
    if new_password != confirm:
        return {"status": 400, "error": "Passwords don't match"}
    if reset_password(token, new_password):
        return {"status": 200, "message": "Password reset successfully"}
    return {"status": 400, "error": "Invalid or expired token"}


# ======================== Demo ========================
print("=== Password Management Demo ===")

# Simulate logged-in
alice.is_authenticated = True
bob.is_authenticated = True

# --- Password Change ---
req = {"user": alice, "post": {"old_password": "oldpass123",
                                "new_password": "newpass456",
                                "confirm_password": "newpass456"}}
print(f"Password change (correct): {password_change_view(req)}")
print(f"  New password works: {alice.check_password('newpass456')}")
print(f"  Old password works: {alice.check_password('oldpass123')}")

req_bad = {"user": alice, "post": {"old_password": "wrong",
                                    "new_password": "12",
                                    "confirm_password": "34"}}
print(f"Password change (errors): {password_change_view(req_bad)}")

# --- Password Reset (email) ---
reset_req = {"post": {"email": "bob@example.com"}}
result = password_reset_request_view(reset_req)
print(f"\nReset request: {result}")
token = result.get("token", "")

# Confirm reset
confirm_req = {"post": {"token": token,
                         "new_password": "bobnew789",
                         "confirm_password": "bobnew789"}}
print(f"Reset confirm: {password_reset_confirm_view(confirm_req)}")
print(f"  Bob's new password works: {bob.check_password('bobnew789')}")

# Reuse token (should fail)
print(f"Reuse token: {password_reset_confirm_view(confirm_req)}")

# Invalid token
bad_token_req = {"post": {"token": "faketoken", "new_password": "abc123",
                           "confirm_password": "abc123"}}
print(f"Bad token: {password_reset_confirm_view(bad_token_req)}")
