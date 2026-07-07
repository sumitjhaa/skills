"""Permissions & authorization: login_required, permission_required, per-object checks."""
from typing import Optional, Callable
from functools import wraps


# ======================== Permission System ========================

# Built-in permissions: app_label.action_modelname
PERMISSIONS: dict[str, list[str]] = {}  # user_id → [perm_codename]


def grant(user_id: int, *permissions: str):
    PERMISSIONS.setdefault(user_id, set())
    for p in permissions:
        PERMISSIONS[user_id].add(p)


def revoke(user_id: int, *permissions: str):
    if user_id in PERMISSIONS:
        for p in permissions:
            PERMISSIONS[user_id].discard(p)


def has_perm(user_id: int, perm: str) -> bool:
    perms = PERMISSIONS.get(user_id, set())
    return perm in perms or f"{perm.split('.')[0]}.{perm.split('_')[0]}_*" in perms


def has_perms(user_id: int, *perms: str) -> bool:
    return all(has_perm(user_id, p) for p in perms)


# ======================== User & Auth ========================
USERS: dict[int, dict] = {}


class User:
    def __init__(self, username: str, is_staff=False, is_superuser=False):
        self.id = len(USERS) + 1
        self.username = username
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self.is_authenticated = False
        self.is_active = True
        USERS[self.id] = self

    def has_perm(self, perm: str) -> bool:
        if self.is_superuser:
            return True
        return has_perm(self.id, perm)

    def has_perms(self, *perms: str) -> bool:
        return all(self.has_perm(p) for p in perms)


class AnonymousUser:
    is_authenticated = False
    is_active = False
    username = "Anonymous"
    id = None
    is_staff = False
    is_superuser = False

    def has_perm(self, perm: str) -> bool:
        return False

    def has_perms(self, *perms: str) -> bool:
        return False


# ======================== Decorators ========================

def login_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        user = request.get("user", AnonymousUser())
        if not user.is_authenticated:
            return {"status": 302, "location": "/login/", "error": "Login required"}
        return func(request, *args, **kwargs)
    return wrapper


def permission_required(perm: str, raise_exception: bool = True) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(request: dict, *args, **kwargs):
            user = request.get("user", AnonymousUser())
            if not user.has_perm(perm):
                if raise_exception:
                    return {"status": 403, "error": f"Permission denied: {perm}"}
                return {"status": 302, "location": "/login/"}
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def staff_member_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        user = request.get("user", AnonymousUser())
        if not user.is_authenticated or not user.is_staff:
            return {"status": 403, "error": "Staff access required"}
        return func(request, *args, **kwargs)
    return wrapper


def superuser_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        user = request.get("user", AnonymousUser())
        if not user.is_superuser:
            return {"status": 403, "error": "Superuser access required"}
        return func(request, *args, **kwargs)
    return wrapper


# ======================== Object-Level Permissions ========================

class Post:
    """Simulates a model with per-object ownership."""
    _data: list[dict] = []
    _pk = 1

    def __init__(self, title: str, content: str, author_id: int):
        self.id = Post._pk
        self.title = title
        self.content = content
        self.author_id = author_id
        Post._data.append(self)
        Post._pk += 1

    def can_view(self, user: User) -> bool:
        return True  # anyone can view

    def can_edit(self, user: User) -> bool:
        return user.id == self.author_id or user.is_superuser

    def can_delete(self, user: User) -> bool:
        return user.id == self.author_id or user.has_perm("blog.delete_post")


# ======================== Views ========================

@login_required
def dashboard_view(request: dict) -> dict:
    return {"status": 200, "message": "Welcome to dashboard"}


@permission_required("blog.add_post")
def create_post_view(request: dict) -> dict:
    return {"status": 200, "message": "Post created"}


@staff_member_required
def admin_panel_view(request: dict) -> dict:
    return {"status": 200, "message": "Admin panel"}


def edit_post_view(request: dict, post_id: int) -> dict:
    user = request.get("user", AnonymousUser())
    post = next((p for p in Post._data if p.id == post_id), None)
    if not post:
        return {"status": 404, "error": "Post not found"}
    if not post.can_edit(user):
        return {"status": 403, "error": "You don't own this post"}
    return {"status": 200, "message": f"Editing post {post_id}"}


# ======================== Demo ========================
print("=== Permissions & Authorization Demo ===")

# Create users
normal = User("charlie")
normal.is_authenticated = True
staff = User("diana", is_staff=True)
staff.is_authenticated = True
admin = User("eve", is_superuser=True)
admin.is_authenticated = True
anon = AnonymousUser()

# Grant permissions
grant(normal.id, "blog.add_post")
grant(staff.id, "blog.add_post", "blog.change_post")

# Create posts
post1 = Post("Hello", "Post content", author_id=normal.id)
post2 = Post("Admin Post", "Secret", author_id=admin.id)

users = {"normal": normal, "staff": staff, "admin": admin, "anon": anon}

print("\n--- login_required ---")
for name, u in users.items():
    req = {"user": u}
    result = dashboard_view(req)
    print(f"  {name:6s}: {result['status']} — {result.get('message', result.get('error', ''))}")

print("\n--- permission_required('blog.add_post') ---")
for name, u in users.items():
    req = {"user": u}
    result = create_post_view(req)
    print(f"  {name:6s}: {result['status']} — {result.get('message', result.get('error', ''))}")

print("\n--- staff_member_required ---")
for name, u in users.items():
    req = {"user": u}
    result = admin_panel_view(req)
    print(f"  {name:6s}: {result['status']} — {result.get('message', result.get('error', ''))}")

print("\n--- Object-level: edit_post ---")
for name, u in users.items():
    req = {"user": u}
    result = edit_post_view(req, post_id=1)  # normal's post
    print(f"  {name:6s} editing post1: {result['status']} — {result.get('message', result.get('error', ''))}")

print("\n--- Superuser overrides ---")
req = {"user": admin}
print(f"  admin has_perm('blog.add_post'): {admin.has_perm('blog.add_post')}")
print(f"  admin has_perm('nonexistent'):   {admin.has_perm('nonexistent')}")
