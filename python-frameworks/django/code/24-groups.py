"""Groups & custom permissions: group-based access control."""
from typing import Optional
from functools import wraps


# ======================== Group & Permission System ========================
GROUPS: dict[str, dict] = {}  # group_name → {"permissions": set(), "users": set()}


class Group:
    def __init__(self, name: str):
        self.name = name
        self.permissions: set[str] = set()
        GROUPS[name] = self

    def add_permission(self, perm: str):
        self.permissions.add(perm)

    def remove_permission(self, perm: str):
        self.permissions.discard(perm)

    @property
    def user_set(self) -> list:
        return [u for u in USERS.values() if self.name in u.groups]

    def __repr__(self) -> str:
        return f"<Group: {self.name} ({len(self.permissions)} perms)>"


# ======================== User ========================
USERS: dict[int, dict] = {}


class User:
    def __init__(self, username: str):
        self.id = len(USERS) + 1
        self.username = username
        self.is_authenticated = False
        self.is_active = True
        self.is_superuser = False
        self.groups: list[str] = []
        USERS[self.id] = self

    def add_to_group(self, group_name: str):
        if group_name not in self.groups:
            self.groups.append(group_name)

    def remove_from_group(self, group_name: str):
        if group_name in self.groups:
            self.groups.remove(group_name)

    def get_group_permissions(self) -> set[str]:
        """Collect permissions from all groups."""
        perms = set()
        for gname in self.groups:
            group = GROUPS.get(gname)
            if group:
                perms.update(group.permissions)
        return perms

    def has_perm(self, perm: str) -> bool:
        if self.is_superuser:
            return True
        return perm in self.get_group_permissions()

    def has_perms(self, *perms: str) -> bool:
        return all(self.has_perm(p) for p in perms)


class AnonymousUser:
    is_authenticated = False
    is_active = False
    username = "Anonymous"
    id = None
    is_superuser = False

    def has_perm(self, perm: str) -> bool:
        return False


# ======================== Custom Permissions (on Model) ========================

# Simulates: class Post(models.Model):
#     class Meta:
#         permissions = [
#             ("can_publish", "Can publish posts"),
#             ("can_feature", "Can feature posts"),
#             ("can_archive", "Can archive posts"),
#         ]

CUSTOM_PERMISSIONS = {
    "blog.can_publish": "Can publish posts",
    "blog.can_feature": "Can feature posts",
    "blog.can_archive": "Can archive posts",
    "blog.can_moderate": "Can moderate comments",
}


# ======================== Decorators ========================

def group_required(*group_names: str):
    """Require user to be in at least one of the listed groups."""
    def decorator(func):
        @wraps(func)
        def wrapper(request: dict, *args, **kwargs):
            user = request.get("user", AnonymousUser())
            if not user.is_authenticated:
                return {"status": 302, "location": "/login/"}
            if not any(g in user.groups for g in group_names):
                return {"status": 403, "error": f"Must be in one of: {group_names}"}
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def permission_required(perm: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request: dict, *args, **kwargs):
            user = request.get("user", AnonymousUser())
            if not user.has_perm(perm):
                return {"status": 403, "error": f"Missing: {perm}"}
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


# ======================== Views ========================

def publish_post_view(request: dict) -> dict:
    return {"status": 200, "message": "Post published"}


def feature_post_view(request: dict) -> dict:
    return {"status": 200, "message": "Post featured"}


def moderate_comments_view(request: dict) -> dict:
    return {"status": 200, "message": "Comments moderated"}


@group_required("editors", "admins")
def editor_dashboard_view(request: dict) -> dict:
    return {"status": 200, "message": "Editor dashboard"}


# ======================== Demo ========================
print("=== Groups & Custom Permissions Demo ===")

# Create groups
editors = Group("editors")
admins = Group("admins")
moderators = Group("moderators")

# Add permissions to groups
editors.add_permission("blog.can_publish")
editors.add_permission("blog.can_feature")
admins.add_permission("blog.can_publish")
admins.add_permission("blog.can_feature")
admins.add_permission("blog.can_archive")
admins.add_permission("blog.can_moderate")
moderators.add_permission("blog.can_moderate")

# Create users and assign groups
alice = User("alice")
alice.is_authenticated = True
alice.add_to_group("editors")

bob = User("bob")
bob.is_authenticated = True
bob.add_to_group("moderators")

charlie = User("charlie")
charlie.is_authenticated = True
charlie.add_to_group("admins")

dave = User("dave")  # no group
dave.is_authenticated = True

print("\n--- Group Permissions ---")
for gname, group in GROUPS.items():
    print(f"  {gname}: {group.permissions}")

print("\n--- User Group Memberships ---")
for u in USERS.values():
    print(f"  {u.username}: groups={u.groups}")

print("\n--- Permission Checks ---")
tests = [
    ("alice", "blog.can_publish"),
    ("alice", "blog.can_moderate"),
    ("bob", "blog.can_moderate"),
    ("bob", "blog.can_publish"),
    ("charlie", "blog.can_archive"),
    ("dave", "blog.can_publish"),
]
for name, perm in tests:
    user = next(u for u in USERS.values() if u.username == name)
    print(f"  {name:8s} has {perm:20s}: {user.has_perm(perm)}")

print("\n--- View Access ---")
req = {"user": alice}
print(f"  alice → editor_dashboard: {editor_dashboard_view(req)}")

req = {"user": bob}
print(f"  bob   → editor_dashboard: {editor_dashboard_view(req)}")

req = {"user": dave}
print(f"  dave  → editor_dashboard: {editor_dashboard_view(req)}")
