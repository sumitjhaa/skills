"""Integration: Auth Blog — login-required views, per-user content, permissions."""
from typing import Optional
from functools import wraps
import hashlib
import secrets


# ======================== Auth System ========================
USERS: dict[int, dict] = {}
SESSION_STORE: dict[str, int] = {}
PERMISSIONS: dict[int, set[str]] = {}  # user_id → permissions
GROUPS: dict[str, set[int]] = {}  # group_name → user_ids
PK = 1


class AnonymousUser:
    is_authenticated = False
    is_active = False
    username = "Anonymous"
    id = None

    def has_perm(self, perm: str) -> bool:
        return False


_anon = AnonymousUser()


def _hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


class User:
    def __init__(self, username: str, email: str, password: str):
        global PK
        self.id = PK
        self.username = username
        self.email = email
        self.password_hash = _hash(password)
        self.is_authenticated = False
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
        USERS[PK] = self
        PK += 1

    def check_password(self, password: str) -> bool:
        return self.password_hash == _hash(password)

    def has_perm(self, perm: str) -> bool:
        if self.is_superuser:
            return True
        return perm in PERMISSIONS.get(self.id, set())


def authenticate(username: str, password: str) -> Optional[User]:
    for u in USERS.values():
        if u.username == username and u.check_password(password):
            return u
    return None


def login(request: dict, user: User):
    sid = secrets.token_hex(16)
    SESSION_STORE[sid] = user.id
    user.is_authenticated = True
    request["session_id"] = sid
    request["user"] = user


def logout(request: dict):
    sid = request.get("session_id")
    if sid in SESSION_STORE:
        uid = SESSION_STORE.pop(sid)
        u = USERS.get(uid)
        if u:
            u.is_authenticated = False
    request["user"] = AnonymousUser()


def get_user(request: dict) -> User:
    sid = request.get("session_id")
    if sid and sid in SESSION_STORE:
        u = USERS.get(SESSION_STORE[sid])
        if u and u.is_active:
            return u
    return AnonymousUser()


def login_required(func):
    @wraps(func)
    def wrapper(request: dict, *args, **kwargs):
        user = get_user(request)
        if not user.is_authenticated:
            return {"status": 302, "location": "/login/", "error": "Login required"}
        return func(request, *args, **kwargs)
    return wrapper


def permission_required(perm: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request: dict, *args, **kwargs):
            user = get_user(request)
            if not user.has_perm(perm):
                return {"status": 403, "error": f"Permission denied: {perm}"}
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


# ======================== Blog Data ========================
POSTS: list[dict] = []
COMMENTS: list[dict] = []
POST_PK = 1
COMMENT_PK = 1


class Post:
    def __init__(self, title: str, content: str, author_id: int, is_published: bool = False):
        global POST_PK
        self.id = POST_PK
        self.title = title
        self.content = content
        self.author_id = author_id
        self.is_published = is_published
        self.created_at = "2024-07-07"
        POSTS.append(self)
        POST_PK += 1

    def can_edit(self, user: User) -> bool:
        return user.id == self.author_id or user.has_perm("blog.change_post")

    def can_delete(self, user: User) -> bool:
        return user.id == self.author_id or user.has_perm("blog.delete_post")

    def to_dict(self) -> dict:
        author = USERS.get(self.author_id)
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content[:50] + "...",
            "author": author.username if author else "?",
            "is_published": self.is_published,
        }


class Comment:
    def __init__(self, text: str, post_id: int, author_id: int):
        global COMMENT_PK
        self.id = COMMENT_PK
        self.text = text
        self.post_id = post_id
        self.author_id = author_id
        COMMENTS.append(self)
        COMMENT_PK += 1

    def to_dict(self) -> dict:
        author = USERS.get(self.author_id)
        return {
            "id": self.id,
            "text": self.text,
            "author": author.username if author else "?",
        }


# ======================== Views ========================

# --- Auth Views ---
def login_view(request: dict) -> dict:
    username = request.get("post", {}).get("username", "")
    password = request.get("post", {}).get("password", "")
    user = authenticate(username, password)
    if user:
        login(request, user)
        return {"status": 200, "message": f"Welcome, {user.username}!"}
    return {"status": 401, "error": "Invalid credentials"}


def signup_view(request: dict) -> dict:
    data = request.get("post", {})
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")

    if len(username) < 3:
        return {"status": 400, "error": "Username too short"}
    if any(u.username == username for u in USERS.values()):
        return {"status": 400, "error": "Username taken"}
    if len(password) < 6:
        return {"status": 400, "error": "Password too short"}

    user = User(username, email, password)
    login(request, user)
    return {"status": 201, "message": f"Welcome, {user.username}!"}


def logout_view(request: dict) -> dict:
    logout(request)
    return {"status": 200, "message": "Logged out"}


# --- Blog Views ---
def post_list_view(request: dict) -> dict:
    posts = [p.to_dict() for p in POSTS if p.is_published or
             (get_user(request).is_authenticated and p.author_id == get_user(request).id)]
    return {"status": 200, "posts": posts}


def my_posts_view(request: dict) -> dict:
    user = get_user(request)
    if not user.is_authenticated:
        return {"status": 401, "error": "Login required"}
    posts = [p.to_dict() for p in POSTS if p.author_id == user.id]
    return {"status": 200, "posts": posts}


@login_required
def create_post_view(request: dict) -> dict:
    user = get_user(request)
    data = request.get("post", {})
    title = data.get("title", "Untitled")
    content = data.get("content", "")
    post = Post(title, content, user.id)
    return {"status": 201, "post": post.to_dict()}


@login_required
def edit_post_view(request: dict, post_id: int) -> dict:
    user = get_user(request)
    post = next((p for p in POSTS if p.id == post_id), None)
    if not post:
        return {"status": 404, "error": "Post not found"}
    if not post.can_edit(user):
        return {"status": 403, "error": "You don't own this post"}
    data = request.get("post", {})
    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    return {"status": 200, "post": post.to_dict()}


@permission_required("blog.publish_post")
def publish_post_view(request: dict, post_id: int) -> dict:
    post = next((p for p in POSTS if p.id == post_id), None)
    if not post:
        return {"status": 404, "error": "Post not found"}
    post.is_published = True
    return {"status": 200, "message": f"Published: {post.title}"}


@login_required
def add_comment_view(request: dict, post_id: int) -> dict:
    user = get_user(request)
    text = request.get("post", {}).get("text", "")
    if not text:
        return {"status": 400, "error": "Comment text required"}
    comment = Comment(text, post_id, user.id)
    return {"status": 201, "comment": comment.to_dict()}


# ======================== Demo ========================
print("=" * 60)
print("📝 AUTH BLOG — INTEGRATION DEMO")
print("=" * 60)

# Setup users
alice = User("alice", "alice@example.com", "pass123")
bob = User("bob", "bob@example.com", "pass456")
charlie = User("charlie", "charlie@example.com", "pass789")

# Add permissions/groups
PERMISSIONS[alice.id] = {"blog.publish_post"}
PERMISSIONS[bob.id] = {"blog.publish_post"}

# Login as alice
req_alice: dict = {"post": {"username": "alice", "password": "pass123"}}
print(f"\n🔐 Login: {login_view(req_alice)['message']}")

# Create posts
print(f"\n📝 Create post: {create_post_view({**req_alice, 'post': {'title': 'My First Post', 'content': 'Hello world!'}})['status']}")
print(f"📝 Create post: {create_post_view({**req_alice, 'post': {'title': 'Django Auth', 'content': 'Auth is fun!'}})['status']}")

# Login as bob
req_bob: dict = {"post": {"username": "bob", "password": "pass456"}}
print(f"\n🔐 Login: {login_view(req_bob)['message']}")
print(f"📝 Create post: {create_post_view({**req_bob, 'post': {'title': 'Bob\'s Article', 'content': 'Bob was here'}})['status']}")

# List posts
print(f"\n📋 All visible posts:")
for p in post_list_view(req_alice)["posts"]:
    print(f"   #{p['id']} '{p['title']}' by {p['author']} (published={p['is_published']})")

# Publish (requires permission)
post1_id = POSTS[0].id
print(f"\n✅ Publish post #{post1_id}: {publish_post_view({**req_alice, 'post': {}}, post1_id)}")

# Alice's posts only
print(f"\n👤 My posts:")
for p in my_posts_view(req_alice)["posts"]:
    print(f"   #{p['id']} '{p['title']}'")

# Charlie tries to edit Alice's post
req_charlie: dict = {"post": {"username": "charlie", "password": "pass789"}}
login_view(req_charlie)
print(f"\n🚫 Charlie edits Alice's post: {edit_post_view({**req_charlie, 'post': {'title': 'Hacked!'}}, post1_id)['error']}")

# Add comments
print(f"\n💬 Comment on post #{post1_id}: {add_comment_view({**req_bob, 'post': {'text': 'Great post!'}}, post1_id)}")
print(f"💬 Comment on post #{post1_id}: {add_comment_view({**req_charlie, 'post': {'text': 'Nice work!'}}, post1_id)}")

# Charlie tries to publish (no permission)
print(f"\n🚫 Charlie publishes: {publish_post_view({**req_charlie, 'post': {}}, post1_id)['error']}")

# Anonymous access
anon_req: dict = {}
print(f"\n👤 Anonymous posts: {len(post_list_view(anon_req)['posts'])} visible (only published)")
