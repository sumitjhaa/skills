"""Integration: Full REST API for the Auth Blog — all DRF concepts combined."""
from typing import Any, Optional
from functools import wraps
import json
import time
from collections import defaultdict


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", data=None, query_params=None, user=None, META=None):
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.user = user or AnonymousUser()
        self.META = META or {}
        self.action = None


class Response:
    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self):
        return json.dumps(self.data, indent=2)


class AnonymousUser:
    is_authenticated = False
    is_active = False
    is_staff = False
    is_superuser = False
    username = "Anonymous"
    id = None
    def has_perm(self, perm): return False


class User:
    def __init__(self, username, is_staff=False, is_superuser=False):
        self.id = hash(username) % 10000
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = is_staff
        self.is_superuser = is_superuser
    def has_perm(self, perm): return self.is_superuser


# ======================== Permissions ========================
class BasePermission:
    def has_permission(self, request, view): return True
    def has_object_permission(self, request, view, obj): return True


class AllowAny(BasePermission):
    def has_permission(self, request, view): return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated


class IsAdminUser(BasePermission):
    def has_permission(self, request, view): return request.user.is_authenticated and request.user.is_staff


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.get("author_id") == request.user.id


# ======================== Throttling ========================
class RateThrottle:
    cache = defaultdict(list)
    def __init__(self, rate=10, window=60, scope="default"):
        self.rate = rate
        self.window = window
        self.scope = scope

    def allow_request(self, request, view):
        key = f"{self.scope}:{request.user.username if request.user.is_authenticated else 'anon'}"
        now = time.time()
        history = self.cache[key]
        self.cache[key] = [t for t in history if now - t < self.window]
        if len(self.cache[key]) >= self.rate:
            self._wait = self.window - (now - self.cache[key][0])
            return False
        self.cache[key].append(now)
        self._wait = None
        return True

    def wait(self): return self._wait


# ======================== Pagination ========================
class Paginator:
    def paginate(self, queryset, request):
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 5))
        total = len(queryset)
        start = (page - 1) * page_size
        end = start + page_size
        return {
            "count": total,
            "page": page,
            "page_size": page_size,
            "total_pages": max(1, -(-total // page_size)),
            "results": queryset[start:end],
        }


# ======================== Data Store ========================
POSTS: list[dict] = []
COMMENTS: list[dict] = []
PK = {"post": 1, "comment": 1}


def seed():
    global POSTS, COMMENTS, PK
    POSTS = [
        {"id": 1, "title": "Hello Django", "content": "First post content", "author_id": 1, "author_name": "alice", "is_published": True, "likes": 12, "created": "2024-01-15"},
        {"id": 2, "title": "DRF Guide", "content": "REST framework guide", "author_id": 1, "author_name": "alice", "is_published": True, "likes": 8, "created": "2024-03-20"},
        {"id": 3, "title": "Python Tips", "content": "Python tips and tricks", "author_id": 2, "author_name": "bob", "is_published": True, "likes": 5, "created": "2024-02-01"},
        {"id": 4, "title": "Draft: Advanced", "content": "Not yet published", "author_id": 2, "author_name": "bob", "is_published": False, "likes": 3, "created": "2024-04-10"},
    ]
    COMMENTS = [
        {"id": 1, "text": "Great post!", "post_id": 1, "author_id": 2, "author_name": "bob"},
        {"id": 2, "text": "Thanks!", "post_id": 1, "author_id": 1, "author_name": "alice"},
        {"id": 3, "text": "Very helpful", "post_id": 2, "author_id": 2, "author_name": "bob"},
    ]
    PK = {"post": 5, "comment": 4}


# ======================== Serializers ========================
class PostSerializer:
    def to_representation(self, post):
        comments = [c for c in COMMENTS if c["post_id"] == post["id"]]
        return {
            **post,
            "comments": comments,
            "comment_count": len(comments),
            "url": f"/api/v1/posts/{post['id']}/",
        }

    def to_internal_value(self, data):
        validated = {}
        if "title" in data:
            if len(data["title"]) < 3:
                raise ValueError("Title must be at least 3 chars")
            validated["title"] = data["title"]
        if "content" in data:
            validated["content"] = data["content"]
        return validated


# ======================== API Views ========================
class APIView:
    permission_classes = [AllowAny]
    throttle_classes = []
    serializer_class = PostSerializer

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        # Permissions
        for pc in self.permission_classes:
            if not pc().has_permission(request, self):
                return Response({"detail": "Permission denied"}, status=403)
        # Throttling
        for tc in self.throttle_classes:
            if not tc().allow_request(request, self):
                wait = tc().wait()
                return Response({"detail": "Throttled", "retry_after": round(wait, 1) if wait else 60}, status=429)
        # Method handler
        handler = getattr(self, request.method.lower(), None)
        if not handler:
            return Response({"error": "Method not allowed"}, status=405)
        return handler(request, *args, **kwargs)

    def check_object_perms(self, request, obj):
        for pc in self.permission_classes:
            if not pc().has_object_permission(request, self, obj):
                return False
        return True


# ======================== Post Views ========================
class PostList(APIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer

    def get(self, request):
        queryset = [p for p in POSTS if p["is_published"] or request.user.is_authenticated]
        paginator = Paginator()
        page = paginator.paginate(queryset, request)
        ser = PostSerializer()
        page["results"] = [ser.to_representation(p) for p in page["results"]]
        return Response(page)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=401)
        data = request.data
        ser = PostSerializer()
        try:
            validated = ser.to_internal_value(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        global PK
        post = {
            "id": PK["post"],
            "title": validated.get("title", "Untitled"),
            "content": validated.get("content", ""),
            "author_id": request.user.id,
            "author_name": request.user.username,
            "is_published": False,
            "likes": 0,
            "created": "2024-07-07",
        }
        PK["post"] += 1
        POSTS.append(post)
        return Response(PostSerializer().to_representation(post), status=201)


class PostDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PostSerializer

    def get_object(self, pk):
        return next((p for p in POSTS if p["id"] == pk), None)

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        if not self.check_object_perms(request, obj):
            return Response({"detail": "Not found"}, status=404)
        return Response(PostSerializer().to_representation(obj))

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        if not self.check_object_perms(request, obj):
            return Response({"detail": "You do not own this post"}, status=403)
        ser = PostSerializer()
        try:
            validated = ser.to_internal_value(request.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        obj.update(validated)
        return Response(PostSerializer().to_representation(obj))

    def delete(self, request, pk):
        global POSTS
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        if not self.check_object_perms(request, obj):
            return Response({"detail": "You do not own this post"}, status=403)
        POSTS = [p for p in POSTS if p["id"] != pk]
        return Response({"message": "Deleted"}, status=204)


class PostPublish(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        post = next((p for p in POSTS if p["id"] == pk), None)
        if not post:
            return Response({"error": "Not found"}, status=404)
        post["is_published"] = True
        return Response({"message": "Published", "post_id": pk})


class CommentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        comments = [c for c in COMMENTS if c["post_id"] == post_id]
        return Response({"count": len(comments), "results": comments})

    def post(self, request, post_id):
        if not request.data.get("text"):
            return Response({"error": "Text required"}, status=400)
        global PK
        comment = {
            "id": PK["comment"],
            "text": request.data["text"],
            "post_id": post_id,
            "author_id": request.user.id,
            "author_name": request.user.username,
        }
        PK["comment"] += 1
        COMMENTS.append(comment)
        return Response(comment, status=201)


class MyPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_posts = [p for p in POSTS if p["author_id"] == request.user.id]
        ser = PostSerializer()
        return Response({"count": len(user_posts), "results": [ser.to_representation(p) for p in user_posts]})


# ======================== Router ========================
class Router:
    def __init__(self):
        self.routes = []

    def register(self, method, pattern, view, name=None):
        self.routes.append({"method": method, "pattern": pattern, "view": view, "name": name})

    def resolve(self, request, path):
        for route in self.routes:
            method_match = route["method"] == request.method
            if not method_match:
                continue
            pattern = route["pattern"]
            if "{pk}" in pattern:
                prefix = pattern.replace("{pk}", "")
                if path.startswith(prefix):
                    pk_str = path[len(prefix):].strip("/")
                    if pk_str.isdigit():
                        return route["view"], {"pk": int(pk_str)}, route["name"]
            elif "{post_id}" in pattern:
                prefix = pattern.replace("{post_id}", "")
                if path.startswith(prefix):
                    pid_str = path[len(prefix):].strip("/")
                    if pid_str.isdigit():
                        return route["view"], {"post_id": int(pid_str)}, route["name"]
            elif path == pattern:
                return route["view"], {}, route["name"]
        return None, None, None


# ======================== Demo ========================
print("=" * 60)
print("🌐 REST API — FULL INTEGRATION DEMO")
print("=" * 60)

seed()
alice = User("alice", is_staff=True, is_superuser=True)
bob = User("bob")
anon = AnonymousUser()

# Setup Router
router = Router()
router.register("GET", "/api/v1/posts/", PostList(), "post-list")
router.register("POST", "/api/v1/posts/", PostList(), "post-create")
router.register("GET", "/api/v1/posts/{pk}/", PostDetail(), "post-detail")
router.register("PUT", "/api/v1/posts/{pk}/", PostDetail(), "post-update")
router.register("DELETE", "/api/v1/posts/{pk}/", PostDetail(), "post-delete")
router.register("POST", "/api/v1/posts/{pk}/publish/", PostPublish(), "post-publish")
router.register("GET", "/api/v1/posts/{post_id}/comments/", CommentList(), "comment-list")
router.register("POST", "/api/v1/posts/{post_id}/comments/", CommentList(), "comment-create")
router.register("GET", "/api/v1/my-posts/", MyPosts(), "my-posts")

print("\n--- Registered Routes ---")
for r in router.routes:
    print(f"  {r['method']:6s} {r['pattern']:40s} → {r['name']}")

def call(method, path, user=anon, data=None, params=None):
    req = Request(method, data=data or {}, query_params=params or {}, user=user)
    view, kwargs, name = router.resolve(req, path)
    if view:
        req.action = name.split("-")[0] if name else "unknown"
        return view.dispatch(req, **(kwargs or {}))
    return Response({"error": "Not found"}, status=404)

print("\n--- 1. GET /posts/ (anon — only published) ---")
resp = call("GET", "/api/v1/posts/")
data = json.loads(resp.render())
print(f"  Status: {resp.status}, Posts: {data['count']}")
for p in data["results"]:
    print(f"    #{p['id']} {p['title']} (published={p['is_published']})")

print("\n--- 2. POST /posts/ (anon — should fail) ---")
resp = call("POST", "/api/v1/posts/", user=anon, data={"title": "Hacked"})
print(f"  Status: {resp.status}: {json.loads(resp.render())['detail']}")

print("\n--- 3. POST /posts/ (alice — create) ---")
resp = call("POST", "/api/v1/posts/", user=alice, data={"title": "New REST Post", "content": "Created via API"})
print(f"  Status: {resp.status}: created id={json.loads(resp.render())['id']}")

print("\n--- 4. PUT /posts/1/ (bob — not owner) ---")
resp = call("PUT", "/api/v1/posts/1/", user=bob, data={"title": "Hacked!"})
print(f"  Status: {resp.status}: {json.loads(resp.render()).get('detail', '?')}")

print("\n--- 5. PUT /posts/1/ (alice — owner) ---")
resp = call("PUT", "/api/v1/posts/1/", user=alice, data={"title": "Updated Title"})
print(f"  Status: {resp.status}: new title='{json.loads(resp.render())['title']}'")

print("\n--- 6. POST /posts/1/publish/ (bob — not admin) ---")
resp = call("POST", "/api/v1/posts/1/publish/", user=bob)
print(f"  Status: {resp.status}: {json.loads(resp.render()).get('detail', '?')}")

print("\n--- 7. POST /posts/1/publish/ (alice — admin) ---")
resp = call("POST", "/api/v1/posts/1/publish/", user=alice)
print(f"  Status: {resp.status}: {json.loads(resp.render())['message']}")

print("\n--- 8. GET /posts/1/comments/ ---")
resp = call("GET", "/api/v1/posts/1/comments/", user=alice)
data = json.loads(resp.render())
print(f"  Status: {resp.status}, Comments: {data['count']}")
for c in data["results"]:
    print(f"    #{c['id']} '{c['text']}' by {c['author_name']}")

print("\n--- 9. POST /posts/1/comments/ ---")
resp = call("POST", "/api/v1/posts/1/comments/", user=bob, data={"text": "API comment!"})
print(f"  Status: {resp.status}: comment id={json.loads(resp.render())['id']}")

print("\n--- 10. GET /my-posts/ (alice) ---")
resp = call("GET", "/api/v1/my-posts/", user=alice)
data = json.loads(resp.render())
print(f"  Status: {resp.status}, Alice's posts: {data['count']}")

print("\n--- 11. DELETE /posts/4/ (bob — owner) ---")
resp = call("DELETE", "/api/v1/posts/4/", user=bob)
print(f"  Status: {resp.status}")

print("\n--- 12. GET /posts/ (anon — after publish) ---")
resp = call("GET", "/api/v1/posts/")
data = json.loads(resp.render())
print(f"  Status: {resp.status}, Published posts: {data['count']}")

print("\n✅ REST API Demo Complete")
