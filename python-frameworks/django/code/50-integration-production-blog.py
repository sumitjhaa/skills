"""Integration: Production-ready blog — combines all Phase 05 concepts."""
from typing import Any, Optional, Callable
from functools import wraps
import time
import random
import json
from collections import defaultdict


# ======================== Core ========================
class HttpRequest:
    def __init__(self, method="GET", path="/", user=None, META=None, data=None):
        self.method = method
        self.path = path
        self.user = user or AnonymousUser()
        self.META = META or {}
        self.data = data or {}
        self.session = {"cart": [], "visited": []}


class HttpResponse:
    def __init__(self, content="", status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}


class AnonymousUser:
    is_authenticated = False
    username = "Anonymous"
    is_staff = False


class User:
    def __init__(self, username, is_staff=False):
        self.username = username
        self.is_authenticated = True
        self.is_staff = is_staff


# ======================== Cache ========================
CACHE: dict[str, tuple[Any, float]] = {}

def cached(timeout: int = 60):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = f"{fn.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            if key in CACHE:
                val, exp = CACHE[key]
                if time.time() < exp:
                    return val
            result = fn(*args, **kwargs)
            CACHE[key] = (result, time.time() + timeout)
            return result
        return wrapper
    return decorator


# ======================== Signals ========================
class Signal:
    def __init__(self):
        self._receivers = []
    def connect(self, fn):
        self._receivers.append(fn)
    def send(self, **kwargs):
        for r in self._receivers:
            r(**kwargs)

post_created = Signal()
comment_added = Signal()
post_viewed_event = Signal()


# ======================== Middleware ========================
class MiddlewareChain:
    def __init__(self):
        self._middlewares = []

    def add(self, mw_cls):
        self._middlewares.append(mw_cls)
        return self

    def process(self, request, view_func):
        # Process request
        for mw in self._middlewares:
            response = mw().process_request(request)
            if response:
                return response
        # View
        response = view_func(request)
        # Process response
        for mw in reversed(self._middlewares):
            response = mw().process_response(request, response)
        return response


class TimingMiddleware:
    def process_request(self, request):
        request._start = time.time()
    def process_response(self, request, response):
        dur = time.time() - request._start
        response.headers["X-Duration"] = f"{dur:.3f}"
        return response


class AuthMiddleware:
    def process_request(self, request):
        if request.path.startswith("/admin/") and not request.user.is_staff:
            return HttpResponse("Unauthorized", status=401)
        return None


# ======================== Data Store ========================
POSTS: list[dict] = []
COMMENTS: list[dict] = []
AUDIT_LOG: list[str] = []
PK = {"post": 1, "comment": 1}  # fmt: skip

def seed():
    global POSTS, COMMENTS, PK
    POSTS = [
        {"id": 1, "title": "Hello Django", "content": "First post", "author": "alice", "slug": "hello-django", "is_published": True, "views": 120, "created": "2024-01-15"},
        {"id": 2, "title": "DRF Guide", "content": "REST framework", "author": "alice", "slug": "drf-guide", "is_published": True, "views": 85, "created": "2024-03-20"},
        {"id": 3, "title": "Python Tips", "content": "Tips & tricks", "author": "bob", "slug": "python-tips", "is_published": True, "views": 200, "created": "2024-02-01"},
        {"id": 4, "title": "Draft: Advanced", "content": "Draft content", "author": "bob", "slug": "draft-advanced", "is_published": False, "views": 0, "created": "2024-04-10"},
    ]
    COMMENTS = [
        {"id": 1, "post_id": 1, "text": "Great post!", "author": "bob", "created": "2024-01-16"},
        {"id": 2, "post_id": 1, "text": "Thanks!", "author": "alice", "created": "2024-01-16"},
        {"id": 3, "post_id": 2, "text": "Very helpful", "author": "bob", "created": "2024-03-21"},
    ]
    PK = {"post": 5, "comment": 4}


# ======================== Signal Handlers ========================
@post_created.connect
def on_post_created(**kwargs):
    post = kwargs.get("post", {})
    AUDIT_LOG.append(f"Post created: #{post.get('id')} '{post.get('title')}'")
    CACHE.pop("post:list", None)  # Bust cache

@comment_added.connect
def on_comment_added(**kwargs):
    comment = kwargs.get("comment", {})
    AUDIT_LOG.append(f"Comment #{comment.get('id')} on post #{comment.get('post_id')}")

@post_viewed_event.connect
def on_post_viewed(**kwargs):
    post_id = kwargs.get("post_id")
    for p in POSTS:
        if p["id"] == post_id:
            p["views"] = p.get("views", 0) + 1
            break


# ======================== Services ========================

@cached(timeout=30)
def get_published_posts() -> list[dict]:
    """Cached query for published posts."""
    time.sleep(0.05)  # Simulate DB query
    return [p for p in POSTS if p["is_published"]]


def get_post_by_slug(slug: str) -> dict | None:
    return next((p for p in POSTS if p["slug"] == slug), None)


def create_post(title: str, content: str, author: str) -> dict:
    global PK
    slug = title.lower().replace(" ", "-")
    post = {
        "id": PK["post"],
        "title": title,
        "content": content,
        "author": author,
        "slug": slug,
        "is_published": False,
        "views": 0,
        "created": "2024-07-07",
    }
    POSTS.append(post)
    PK["post"] += 1
    post_created.send(post=post)
    return post


def add_comment(post_id: int, text: str, author: str) -> dict | None:
    if not get_post_by_slug(None) and not any(p["id"] == post_id for p in POSTS):
        return None
    global PK
    comment = {
        "id": PK["comment"],
        "post_id": post_id,
        "text": text,
        "author": author,
        "created": "2024-07-07",
    }
    COMMENTS.append(comment)
    PK["comment"] += 1
    comment_added.send(comment=comment)
    return comment


# ======================== Management Command ========================
def cleanup_old_drafts(days: int = 30, dry_run: bool = False) -> str:
    """Simulated management command to cleanup old drafts."""
    to_delete = [p for p in POSTS if not p["is_published"]]
    if dry_run:
        return f"[DRY RUN] Would delete {len(to_delete)} draft posts"
    for p in to_delete:
        POSTS.remove(p)
        AUDIT_LOG.append(f"Cleaned up draft #{p['id']}")
    return f"Deleted {len(to_delete)} draft posts"


# ======================== Views ========================
def post_list_view(request):
    posts = get_published_posts()  # cached
    return HttpResponse(json.dumps({
        "count": len(posts),
        "results": [
            {
                "id": p["id"],
                "title": p["title"],
                "slug": p["slug"],
                "author": p["author"],
                "views": p["views"],
            }
            for p in posts
        ],
    }))


def post_detail_view(request, slug):
    post = get_post_by_slug(slug)
    if not post:
        return HttpResponse(json.dumps({"error": "Not found"}), status=404)
    post_viewed_event.send(post_id=post["id"])
    comments = [c for c in COMMENTS if c["post_id"] == post["id"]]
    return HttpResponse(json.dumps({
        "post": post,
        "comments": comments,
        "comment_count": len(comments),
    }))


def create_post_view(request):
    if not request.user.is_authenticated:
        return HttpResponse(json.dumps({"error": "Login required"}), status=401)
    if not request.data.get("title") or not request.data.get("content"):
        return HttpResponse(json.dumps({"error": "Title and content required"}), status=400)
    post = create_post(request.data["title"], request.data["content"], request.user.username)
    return HttpResponse(json.dumps(post), status=201)


def dashboard_view(request):
    """Admin dashboard with stats."""
    if not request.user.is_staff:
        return HttpResponse("Admin only", status=403)
    total = len(POSTS)
    published = len([p for p in POSTS if p["is_published"]])
    total_comments = len(COMMENTS)
    total_views = sum(p.get("views", 0) for p in POSTS)
    return HttpResponse(json.dumps({
        "total_posts": total,
        "published_posts": published,
        "drafts": total - published,
        "total_comments": total_comments,
        "total_views": total_views,
    }))


# ======================== Demo ========================
print("=" * 60)
print("🏭 PRODUCTION BLOG — FULL INTEGRATION DEMO")
print("=" * 60)

seed()

alice = User("alice", is_staff=True)
bob = User("bob")
anon = AnonymousUser()

# Setup middleware
middleware = MiddlewareChain()
middleware.add(TimingMiddleware).add(AuthMiddleware)

def run(method, path, user=anon, view_func=None, data=None):
    req = HttpRequest(method, path, user=user, data=data or {})
    return middleware.process(req, view_func)

# --- 1. Cached post list ---
print("\n1. GET /posts/ (cached):")
t0 = time.time()
resp = run("GET", "/posts/", anon, post_list_view)
t1 = time.time()
data = json.loads(resp.content)
print(f"   {data['count']} posts in {(t1-t0)*1000:.0f}ms (cold)")

t2 = time.time()
resp = run("GET", "/posts/", anon, post_list_view)
t3 = time.time()
print(f"   {data['count']} posts in {(t3-t2)*1000:.0f}ms (cached!)")

# --- 2. Post detail with signals ---
print("\n2. GET /posts/hello-django/ (triggers view counter signal):")
resp = run("GET", "/posts/hello-django/", alice, lambda r: post_detail_view(r, "hello-django"))
data = json.loads(resp.content)
print(f"   Title: {data['post']['title']}, Views: {data['post']['views']}, Comments: {data['comment_count']}")

# View again — counter increments
resp = run("GET", "/posts/hello-django/", bob, lambda r: post_detail_view(r, "hello-django"))
data = json.loads(resp.content)
print(f"   After second view: Views={data['post']['views']}")

# --- 3. Create post with signal + cache bust ---
print("\n3. POST /posts/create/ (signal busts cache):")
resp = run("POST", "/posts/create/", alice, create_post_view, data={"title": "New Production Post", "content": "Created with signals"})
data = json.loads(resp.content)
print(f"   Created: #{data['id']} '{data['title']}'")

t4 = time.time()
resp = run("GET", "/posts/", anon, post_list_view)
t5 = time.time()
data = json.loads(resp.content)
print(f"   Post list again: {data['count']} posts in {(t5-t4)*1000:.0f}ms (fresh)")

# --- 4. Middleware timing ---
print("\n4. Timing middleware (X-Duration header):")
resp = run("GET", "/posts/", anon, post_list_view)
print(f"   X-Duration: {resp.headers.get('X-Duration')}s")

# --- 5. Admin-only path ---
print("\n5. Admin dashboard (bob — not staff):")
resp = run("GET", "/admin/", bob, dashboard_view)
print(f"   Status: {resp.status} — {resp.content}")

print("\n6. Admin dashboard (alice — staff):")
resp = run("GET", "/admin/", alice, dashboard_view)
print(f"   Status: {resp.status}")
data = json.loads(resp.content)
print(f"   Stats: {data['total_posts']} posts, {data['drafts']} drafts, {data['total_views']} views")

# --- 6. Management command ---
print("\n7. Management command cleanup:")
result = cleanup_old_drafts(dry_run=True)
print(f"   {result}")
result = cleanup_old_drafts(days=1)
print(f"   {result}")

# --- 7. Audit log ---
print(f"\n8. Audit log ({len(AUDIT_LOG)} entries):")
for entry in AUDIT_LOG[-5:]:
    print(f"   📝 {entry}")

# --- Cache stats ---
print(f"\n9. Cache entries: {len(CACHE)}")
for k, (v, exp) in CACHE.items():
    ttl = round(exp - time.time(), 1)
    print(f"   {k}: ttl={ttl}s")

print("\n✅ Production Blog Integration Complete")
