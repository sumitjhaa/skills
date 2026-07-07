"""Role-Based Access Control: roles, permissions, decorators, resource ownership."""
from typing import Any, Optional
import json
import hmac
import hashlib
import base64
import time


# ======================== JWT ========================

JWT_SECRET = "rbac-secret"

def b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

def b64d(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)

def create_jwt(payload: dict) -> str:
    h = b64e(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
    p = payload.copy()
    p["iat"] = int(time.time())
    p["exp"] = int(time.time()) + 3600
    p = b64e(json.dumps(p).encode())
    s = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
    return f"{h}.{p}.{b64e(s)}"

def verify_jwt(token: str) -> Optional[dict]:
    try:
        h, p, s = token.split(".")
        expected = hmac.new(JWT_SECRET.encode(), f"{h}.{p}".encode(), hashlib.sha256).digest()
        if not hmac.compare_digest(expected, b64d(s)):
            return None
        payload = json.loads(b64d(p))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


# ======================== RBAC System ========================

class RBAC:
    """Role-Based Access Control system."""
    def __init__(self):
        # role -> set of permissions
        self._role_permissions: dict[str, set[str]] = {
            "reader": {"read:post", "read:profile"},
            "writer": {"read:post", "write:post", "read:profile", "write:profile"},
            "editor": {"read:post", "write:post", "edit:post", "delete:post", "read:profile", "write:profile"},
            "admin": {"read:post", "write:post", "edit:post", "delete:post", "read:profile", "write:profile", "admin:users", "admin:settings"},
        }

    def has_permission(self, role: str, permission: str) -> bool:
        return permission in self._role_permissions.get(role, set())

    def check(self, role: str, permission: str) -> bool:
        if not self.has_permission(role, permission):
            return False
        return True

    def get_permissions(self, role: str) -> set[str]:
        return self._role_permissions.get(role, set()).copy()

    def add_role(self, name: str, permissions: list[str]):
        self._role_permissions[name] = set(permissions)


rbac = RBAC()


# ======================== User Store ========================

class UserDB:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self._next_id = 1
        self.posts: dict[int, list[dict]] = {}

    def create(self, username: str, role: str = "reader") -> dict:
        u = {"id": self._next_id, "username": username, "role": role}
        self.users[self._next_id] = u
        self.posts[self._next_id] = []
        self._next_id += 1
        return u

    def get_by_id(self, uid: int) -> Optional[dict]:
        return self.users.get(uid)

    def create_post(self, user_id: int, title: str, content: str) -> dict:
        post = {"id": len(self.posts.get(user_id, [])) + 1, "title": title, "content": content, "user_id": user_id}
        self.posts.setdefault(user_id, []).append(post)
        return post

    def get_posts(self, user_id: int) -> list[dict]:
        return self.posts.get(user_id, [])

    def get_all_posts(self) -> list[dict]:
        all_posts = []
        for uid, posts in self.posts.items():
            for p in posts:
                all_posts.append({**p, "author": self.users.get(uid, {}).get("username")})
        return all_posts

    def get_post_by_id(self, post_id: int) -> Optional[dict]:
        for uid, posts in self.posts.items():
            for p in posts:
                if p["id"] == post_id:
                    return {**p, "author": self.users.get(uid, {}).get("username")}
        return None


db = UserDB()


# ======================== Permission Checker ========================

class PermissionChecker:
    def __init__(self, permission: str, require_ownership: bool = False):
        self.permission = permission
        self.require_ownership = require_ownership

    def __call__(self, authorization: str = "", resource_user_id: int | None = None) -> dict | None:
        if not authorization.startswith("Bearer "):
            return {"error": "not_authenticated"}
        token = authorization[7:]
        payload = verify_jwt(token)
        if payload is None:
            return {"error": "invalid_token"}
        user = db.get_by_id(payload["sub"])
        if user is None:
            return {"error": "user_not_found"}
        if not rbac.check(user["role"], self.permission):
            return {"error": "forbidden", "detail": f"Requires permission: {self.permission}"}
        if self.require_ownership and resource_user_id is not None and user["id"] != resource_user_id:
            if not rbac.check(user["role"], "admin:users"):
                return {"error": "forbidden", "detail": "You can only access your own resources"}
        return user


class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def delete(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "DELETE", "handler": func})
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

@app.get("/posts")
def list_posts(authorization: str = ""):
    checker = PermissionChecker("read:post")
    result = checker(authorization=authorization)
    if isinstance(result, dict) and "error" in result:
        return result
    return {"posts": db.get_all_posts()}


@app.post("/posts")
def create_post(title: str, content: str, authorization: str = ""):
    checker = PermissionChecker("write:post")
    result = checker(authorization=authorization)
    if isinstance(result, dict) and "error" in result:
        return result
    post = db.create_post(result["id"], title, content)
    return {"post": post}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, authorization: str = ""):
    post = db.get_post_by_id(post_id)
    if post is None:
        return {"error": "not_found"}
    checker = PermissionChecker("delete:post", require_ownership=True)
    result = checker(authorization=authorization, resource_user_id=post.get("user_id"))
    if isinstance(result, dict) and "error" in result:
        return result
    return {"success": True, "deleted": post_id}


@app.get("/admin/users")
def admin_list_users(authorization: str = ""):
    checker = PermissionChecker("admin:users")
    result = checker(authorization=authorization)
    if isinstance(result, dict) and "error" in result:
        return result
    return {"users": [{"id": u["id"], "username": u["username"], "role": u["role"]} for u in db.users.values()]}


# ======================== Demo ========================
print("=== RBAC Demo ===\n")

# Create users with different roles
alice = db.create("alice", "admin")
bob = db.create("bob", "writer")
charlie = db.create("charlie", "reader")
editor = db.create("eve", "editor")

# Create tokens
tokens = {
    "alice": create_jwt({"sub": 1, "role": "admin"}),
    "bob": create_jwt({"sub": 2, "role": "writer"}),
    "charlie": create_jwt({"sub": 3, "role": "reader"}),
    "eve": create_jwt({"sub": 4, "role": "editor"}),
}

# Alice creates posts
db.create_post(1, "Admin Post", "Posted by admin")
db.create_post(1, "Announcement", "System announcement")

# Bob creates posts
db.create_post(2, "Bob's Article", "Written by Bob")
db.create_post(2, "Tutorial", "How to code")

print("1. Permissions per role:")
for role in ["reader", "writer", "editor", "admin"]:
    perms = rbac.get_permissions(role)
    print(f"   {role:8s}: {', '.join(sorted(perms))}")

print("\n2. Charlie (reader) lists posts:")
result = app("GET", "/posts", authorization=f"Bearer {tokens['charlie']}")
print(f"   {'✅' if 'posts' in result['data'] else '❌'} {len(result['data'].get('posts', []))} posts\n")

print("3. Charlie tries to create a post (no write permission):")
result = app("POST", "/posts", title="Charlie's Post", content="Test", authorization=f"Bearer {tokens['charlie']}")
print(f"   {result['data']}\n")

print("4. Bob creates a post:")
result = app("POST", "/posts", title="Bob's New Post", content="Content here", authorization=f"Bearer {tokens['bob']}")
print(f"   {result['data']}\n")

print("5. Charlie tries to delete Bob's post (no delete permission):")
result = app("DELETE", "/posts/3", authorization=f"Bearer {tokens['charlie']}")
print(f"   {result['data']}\n")

print("6. Bob tries to delete Alice's post (ownership check):")
result = app("DELETE", "/posts/1", authorization=f"Bearer {tokens['bob']}")
print(f"   {result['data']}\n")

print("7. Eve (editor) deletes a post (has delete permission):")
result = app("DELETE", "/posts/3", authorization=f"Bearer {tokens['eve']}")
print(f"   {result['data']}\n")

print("8. Alice (admin) lists all users:")
result = app("GET", "/admin/users", authorization=f"Bearer {tokens['alice']}")
print(f"   {result['data']}\n")

print("9. Bob tries admin endpoint (no admin permission):")
result = app("GET", "/admin/users", authorization=f"Bearer {tokens['bob']}")
print(f"   {result['data']}")

print("\n10. Unauthenticated request:")
result = app("GET", "/posts")
print(f"   {result['data']}")
