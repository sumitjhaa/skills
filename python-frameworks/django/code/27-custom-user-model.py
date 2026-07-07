"""Custom user models: AbstractUser vs AbstractBaseUser."""
from typing import Optional
import hashlib
import secrets


# ======================== 1. AbstractUser (extend built-in) ========================
class AbstractUser:
    """Simulates Django's AbstractUser — full User with extra fields."""

    id: int = 0
    username: str = ""
    email: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    date_joined: str = ""
    last_login: str = ""

    # Extra fields added by extending AbstractUser
    bio: str = ""
    avatar: str = ""
    phone: str = ""
    location: str = ""

    def __repr__(self) -> str:
        return f"<User: {self.username}>"


class CustomUser(AbstractUser):
    """Extending AbstractUser — everything built-in + custom fields."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


# ======================== 2. AbstractBaseUser (from scratch) ========================

class AbstractBaseUser:
    """
    Simulates Django's AbstractBaseUser — minimal user.
    You define: USERNAME_FIELD, REQUIRED_FIELDS, and all auth methods.
    """

    id: int = 0
    password_hash: str = ""
    last_login: str = ""
    is_active: bool = True

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"  # login with email instead of username
    REQUIRED_FIELDS: list[str] = []

    def set_password(self, raw: str):
        self.password_hash = hashlib.sha256(raw.encode()).hexdigest()

    def check_password(self, raw: str) -> bool:
        return self.password_hash == hashlib.sha256(raw.encode()).hexdigest()

    @property
    def is_authenticated(self) -> bool:
        return True  # AbstractBaseUser instances are always authenticated

    @property
    def is_anonymous(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"<AbstractBaseUser: {getattr(self, self.USERNAME_FIELD, '?')}>"


class EmailUser(AbstractBaseUser):
    """
    Custom user model that uses email as the unique identifier.
    No username field.
    """

    id: int = 0
    email: str = ""
    username: str = ""  # optional, not used for login
    display_name: str = ""
    bio: str = ""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["display_name"]

    def __init__(self, email: str, display_name: str = "", password: str = ""):
        self.id = secrets.randbelow(10000) + 100
        self.email = email
        self.display_name = display_name or email.split("@")[0]
        self.username = self.display_name
        if password:
            self.set_password(password)

    def __str__(self) -> str:
        return self.email


# ======================== Custom Backend for Email Auth ========================

class EmailAuthBackend:
    """Authenticate by email instead of username."""

    USERS: dict[str, "EmailUser"] = {}

    @classmethod
    def register(cls, user: "EmailUser"):
        cls.USERS[user.email] = user

    def authenticate(self, email: str = None, password: str = None) -> Optional["EmailUser"]:
        user = self.USERS.get(email)
        if user and user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id: int) -> Optional["EmailUser"]:
        for u in self.USERS.values():
            if u.id == user_id:
                return u
        return None


# ======================== Demo ========================
print("=== Custom User Model Demo ===")
print("\n--- 1. AbstractUser (extending built-in) ---")
cu = CustomUser(
    username="alice",
    email="alice@example.com",
    bio="Python developer",
    phone="+1-555-0100",
    location="NYC",
)
print(f"  User: {cu.username}")
print(f"  Email: {cu.email}")
print(f"  Extra fields: bio='{cu.bio}', phone='{cu.phone}', location='{cu.location}'")
print(f"  Has built-in: is_active={cu.is_active}, is_staff={cu.is_staff}")

print("\n--- 2. AbstractBaseUser (from scratch) ---")
auth = EmailAuthBackend()

eu = EmailUser("charlie@custom.com", "Charlie", "mypassword123")
auth.register(eu)

eu2 = EmailUser("diana@custom.com", "Diana", "pass456")
auth.register(eu2)

print(f"  Login fields: USERNAME_FIELD='{EmailUser.USERNAME_FIELD}'")
print(f"  No username field required for auth")

# Test email authentication
user = auth.authenticate(email="charlie@custom.com", password="mypassword123")
print(f"  Auth by email: {user} → {user.display_name if user else 'FAIL'}")

bad = auth.authenticate(email="charlie@custom.com", password="wrong")
print(f"  Wrong password: {bad}")

print("\n--- Comparison ---")
print("  AbstractUser:     Full User model, add extra fields, keep built-in auth")
print("  AbstractBaseUser: Minimal user, full control, define everything yourself")
print("  Use AbstractUser  → 90% of projects (simpler)")
print("  Use AbstractBaseUser → custom auth requirements (email-only, phone, etc.)")
