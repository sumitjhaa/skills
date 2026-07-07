"""Integration: Full Auth API — combines DB, JWT, RBAC, file uploads, testing."""
from typing import Any, Optional
from datetime import datetime
import json
import hmac
import hashlib
import base64
import time


# ======================== JWT ========================

JWT_SECRET = "integration-secret"

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


# ======================== Database ========================

class Database:
    def __init__(self):
        self.users: dict[int, dict] = {}
        self.posts: dict[int, dict] = {}
        self.comments: dict[int, dict] = {}
        self.files: dict[str, dict] = {}
        self._next = {"users": 1, "posts": 1, "comments": 1}

    def create_user(self, username: str, email: str, password: str, role: str = "user") -> dict:
        uid = self._next["users"]
        self._next["users"] += 1
        user = {"id": uid, "username": username, "email": email, "password": password, "role": role, "active": True}
        self.users[uid] = user
        return user

    def get_user_by_username(self, username: str) -> Optional[dict]:
        for u in self.users.values():
            if u["username"] == username:
                return u
        return None

    def get_user_by_id(self, uid: int) -> Optional[dict]:
        return self.users.get(uid)

    def create_post(self, title: str, content: str, user_id: int) -> dict:
        pid = self._next["posts"]
        self._next["posts"] += 1
        post = {"id": pid, "title": title, "content": content, "user_id": user_id, "created_at": datetime.now().isoformat()}
        self.posts[pid] = post
        return post

    def get_post(self, pid: int) -> Optional[dict]:
        return self.posts.get(pid)

    def get_posts(self) -> list[dict]:
        return list(self.posts.values())

    def get_user_posts(self, user_id: int) -> list[dict]:
        return [p for p in self.posts.values() if p["user_id"] == user_id]

    def delete_post(self, pid: int) -> bool:
        if pid in self.posts:
            del self.posts[pid]
            return True
        return False

    def create_comment(self, post_id: int, user_id: int, content: str) -> dict:
        cid = self._next["comments"]
        self._next["comments"] += 1
        comment = {"id": cid, "post_id": post_id, "user_id": user_id, "content": content, "created_at": datetime.now().isoformat()}
        self.comments[cid] = comment
        return comment

    def get_post_comments(self, post_id: int) -> list[dict]:
        return [c for c in self.comments.values() if c["post_id"] == post_id]

    def save_file(self, filename: str, content: str, user_id: int) -> dict:
        file_id = filename or f"file_{int(time.time())}"
        file_info = {"filename": filename, "size": len(content), "user_id": user_id, "uploaded_at": datetime.now().isoformat()}
        self.files[file_id] = file_info
        return file_info


# ======================== RBAC ========================

class RBAC:
    def __init__(self):
        self._perms = {
            "user": {"read:post", "write:post", "delete:own_post", "read:comment", "write:comment", "upload:file"},
            "moderator": {"read:post", "write:post", "delete:post", "read:comment", "write:comment", "delete:comment", "upload:file"},
            "admin": {"read:post", "write:post", "delete:post", "read:comment", "write:comment", "delete:comment", "upload:file", "admin:users"},
        }

    def check(self, role: str, permission: str) -> bool:
        return permission in self._perms.get(role, set())


rbac = RBAC()
db = Database()


# ======================== FastAPI App ========================

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

    def put(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "PUT", "handler": func})
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


# ======================== Auth Helpers ========================

def get_current_user(authorization: str = "") -> Optional[dict]:
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    payload = verify_jwt(token)
    if payload is None:
        return None
    return db.get_user_by_id(payload["sub"])


def require_auth(authorization: str = "") -> Optional[dict]:
    user = get_current_user(authorization=authorization)
    if user is None:
        return {"error": "not_authenticated", "detail": "Valid token required"}
    return user


def require_permission(permission: str):
    def check(authorization: str = "") -> Optional[dict]:
        user = require_auth(authorization=authorization)
        if isinstance(user, dict) and "error" in user:
            return user
        if not rbac.check(user["role"], permission):
            return {"error": "forbidden", "detail": f"Requires: {permission}"}
        return user
    return check


# ======================== Auth Endpoints ========================

@app.post("/auth/register")
def register(username: str, email: str, password: str):
    if db.get_user_by_username(username):
        return {"error": "Username taken"}
    user = db.create_user(username, email, password)
    token = create_jwt({"sub": user["id"], "role": user["role"]})
    return {"access_token": token, "user_id": user["id"], "username": user["username"]}


@app.post("/auth/login")
def login(username: str, password: str):
    user = db.get_user_by_username(username)
    if not user or user["password"] != password:
        return {"error": "Invalid credentials"}
    token = create_jwt({"sub": user["id"], "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me")
def me(authorization: str = ""):
    user = require_auth(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    return {"id": user["id"], "username": user["username"], "email": user["email"], "role": user["role"]}


# ======================== Post Endpoints ========================

@app.post("/posts")
def create_post(title: str, content: str, authorization: str = ""):
    user = require_permission("write:post")(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    post = db.create_post(title, content, user["id"])
    return post


@app.get("/posts")
def list_posts():
    posts = db.get_posts()
    enriched = []
    for p in posts:
        user = db.get_user_by_id(p["user_id"])
        enriched.append({**p, "author": user["username"] if user else "unknown"})
    return {"posts": enriched}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    post = db.get_post(post_id)
    if not post:
        return {"error": "not_found"}
    user = db.get_user_by_id(post["user_id"])
    comments = db.get_post_comments(post_id)
    return {**post, "author": user["username"] if user else "unknown", "comments": comments}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, authorization: str = ""):
    user = require_permission("delete:post")(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    post = db.get_post(post_id)
    if not post:
        return {"error": "not_found"}
    if post["user_id"] != user["id"] and not rbac.check(user["role"], "admin:users"):
        return {"error": "forbidden", "detail": "Not your post"}
    db.delete_post(post_id)
    return {"success": True, "deleted": post_id}


# ======================== Comment Endpoints ========================

@app.post("/posts/{post_id}/comments")
def create_comment(post_id: int, content: str, authorization: str = ""):
    user = require_permission("write:comment")(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    if not db.get_post(post_id):
        return {"error": "post_not_found"}
    comment = db.create_comment(post_id, user["id"], content)
    return comment


# ======================== Upload Endpoint ========================

@app.post("/upload")
def upload_file(filename: str, content: str, authorization: str = ""):
    user = require_permission("upload:file")(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    file_info = db.save_file(filename, content, user["id"])
    return file_info


# ======================== Admin Endpoints ========================

@app.get("/admin/users")
def admin_list_users(authorization: str = ""):
    user = require_permission("admin:users")(authorization=authorization)
    if isinstance(user, dict) and "error" in user:
        return user
    return {"users": [{"id": u["id"], "username": u["username"], "role": u["role"]} for u in db.users.values()]}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "users": len(db.users),
        "posts": len(db.posts),
        "comments": len(db.comments),
        "files": len(db.files),
    }


# ======================== Demo ========================
print("=" * 60)
print("  INTEGRATION: FULL AUTH API")
print("=" * 60)

# 1. Register users
print("\n1. Register users:")
alice_reg = app("POST", "/auth/register", username="alice", email="alice@example.com", password="pass123")
alice_token = alice_reg["data"]["access_token"]
print(f"   Alice registered: id={alice_reg['data']['user_id']}")

bob_reg = app("POST", "/auth/register", username="bob", email="bob@example.com", password="pass456")
bob_token = bob_reg["data"]["access_token"]
print(f"   Bob registered: id={bob_reg['data']['user_id']}")

admin_reg = app("POST", "/auth/register", username="admin", email="admin@example.com", password="admin123")
# Promote admin
admin = db.get_user_by_username("admin")
admin["role"] = "admin"
admin_token = create_jwt({"sub": admin["id"], "role": "admin"})
print(f"   Admin registered + promoted: id={admin['id']}")

# 2. Login
print("\n2. Login:")
login_result = app("POST", "/auth/login", username="alice", password="pass123")
print(f"   Alice login: {'✅' if 'access_token' in login_result['data'] else '❌'}")

login_bad = app("POST", "/auth/login", username="alice", password="wrong")
print(f"   Bad login: {login_bad['data']['error']}")

# 3. Auth/me
print("\n3. Get current user:")
alice_me = app("GET", "/auth/me", authorization=f"Bearer {alice_token}")
print(f"   Alice: {alice_me['data']['username']} ({alice_me['data']['role']})")

# 4. Create posts
print("\n4. Create posts:")
p1 = app("POST", "/posts", title="Alice's First Post", content="Hello from Alice!", authorization=f"Bearer {alice_token}")
print(f"   Post created: id={p1['data']['id']} by Alice")

p2 = app("POST", "/posts", title="Bob's Post", content="Bob was here", authorization=f"Bearer {bob_token}")
print(f"   Post created: id={p2['data']['id']} by Bob")

p3 = app("POST", "/posts", title="Admin News", content="System update", authorization=f"Bearer {admin_token}")
print(f"   Post created: id={p3['data']['id']} by Admin")

# 5. List posts
print("\n5. All posts:")
posts = app("GET", "/posts")
for p in posts["data"]["posts"]:
    print(f"   [{p['id']}] {p['title']} — by {p['author']}")

# 6. Comments
print("\n6. Add comments:")
c1 = app("POST", "/posts/1/comments", content="Great post!", authorization=f"Bearer {bob_token}")
print(f"   Bob commented on post 1: {c1['data']['content']}")

c2 = app("POST", "/posts/1/comments", content="Thanks Bob!", authorization=f"Bearer {alice_token}")
print(f"   Alice replied: {c2['data']['content']}")

# 7. Get post with comments
print("\n7. Post 1 with comments:")
post_detail = app("GET", "/posts/1")
print(f"   Title: {post_detail['data']['title']}")
print(f"   Author: {post_detail['data']['author']}")
for c in post_detail["data"]["comments"]:
    commenter = db.get_user_by_id(c["user_id"])
    print(f"   💬 {commenter['username']}: {c['content']}")

# 8. File upload
print("\n8. File upload:")
f1 = app("POST", "/upload", filename="report.txt", content="Annual report data", authorization=f"Bearer {alice_token}")
print(f"   Alice uploaded: {f1['data']['filename']} ({f1['data']['size']} bytes)")

# 9. RBAC enforcement
print("\n9. Permission checks:")
bob_delete_alice = app("DELETE", "/posts/1", authorization=f"Bearer {bob_token}")
print(f"   Bob deletes Alice's post: {bob_delete_alice['data']['error']}")

alice_delete_own = app("DELETE", "/posts/1", authorization=f"Bearer {alice_token}")
print(f"   Alice deletes own post: {'✅' if alice_delete_own['data'].get('success') else '❌'}")

admin_list = app("GET", "/admin/users", authorization=f"Bearer {admin_token}")
print(f"   Admin lists users: {len(admin_list['data']['users'])} users")

bob_admin = app("GET", "/admin/users", authorization=f"Bearer {bob_token}")
print(f"   Bob lists users: {bob_admin['data']['error']}")

# 10. Health
print("\n10. Health check:")
health = app("GET", "/health")
print(f"    {json.dumps(health['data'], indent=2)}")

print("\n" + "=" * 60)
print("  ✅ AUTH API INTEGRATION COMPLETE")
print("=" * 60)
