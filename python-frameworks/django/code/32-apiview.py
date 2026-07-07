"""APIView & function-based API views: request handling, status codes, Response."""
from typing import Any, Optional
from functools import wraps
import json


# ======================== Core DRF Simulation ========================

class Request:
    """Simulates DRF's Request object."""
    def __init__(self, method: str = "GET", data: dict = None, query_params: dict = None, user=None):
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.user = user or AnonymousUser()
        self.META = {"REMOTE_ADDR": "127.0.0.1"}


class Response:
    """Simulates DRF's Response object."""
    def __init__(self, data: Any, status: int = 200, headers: dict = None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self) -> str:
        return json.dumps(self.data, indent=2)


class AnonymousUser:
    is_authenticated = False
    username = "Anonymous"


class User:
    def __init__(self, username: str):
        self.username = username
        self.is_authenticated = True


# ======================== APIView Base ========================

class APIView:
    """Base class for DRF API views."""
    def dispatch(self, request: Request, *args, **kwargs) -> Response:
        handler = getattr(self, request.method.lower(), None)
        if handler is None:
            return Response({"error": "Method not allowed"}, status=405)
        return handler(request, *args, **kwargs)

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            instance = cls()
            return instance.dispatch(request, *args, **kwargs)
        return view


# ======================== Data ========================
POSTS = [
    {"id": 1, "title": "Hello Django", "content": "First post", "author": "alice", "likes": 12},
    {"id": 2, "title": "DRF Basics", "content": "REST framework", "author": "alice", "likes": 8},
    {"id": 3, "title": "Python Tips", "content": "Tips and tricks", "author": "bob", "likes": 5},
]
NEXT_ID = 4


# ======================== Views ========================

class PostListAPIView(APIView):
    """GET /posts/ — list all; POST /posts/ — create new."""

    def get(self, request: Request) -> Response:
        return Response({"count": len(POSTS), "results": POSTS, "status": "ok"})

    def post(self, request: Request) -> Response:
        global NEXT_ID
        data = request.data
        if not data.get("title"):
            return Response({"error": "Title is required"}, status=400)
        post = {
            "id": NEXT_ID,
            "title": data["title"],
            "content": data.get("content", ""),
            "author": request.user.username,
            "likes": 0,
        }
        NEXT_ID += 1
        POSTS.append(post)
        return Response(post, status=201)


class PostDetailAPIView(APIView):
    """GET/PUT/DELETE /posts/:id/"""

    def get_object(self, pk: int) -> Optional[dict]:
        return next((p for p in POSTS if p["id"] == pk), None)

    def get(self, request: Request, pk: int) -> Response:
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Not found"}, status=404)
        return Response(post)

    def put(self, request: Request, pk: int) -> Response:
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Not found"}, status=404)
        data = request.data
        post.update({k: v for k, v in data.items() if k in ("title", "content", "likes")})
        return Response(post)

    def delete(self, request: Request, pk: int) -> Response:
        global POSTS
        post = self.get_object(pk)
        if not post:
            return Response({"error": "Not found"}, status=404)
        POSTS = [p for p in POSTS if p["id"] != pk]
        return Response({"message": "Deleted"}, status=204)


# ======================== Status Code Constants ========================
class status:
    HTTP_200_OK = 200
    HTTP_201_CREATED = 201
    HTTP_204_NO_CONTENT = 204
    HTTP_400_BAD_REQUEST = 400
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403
    HTTP_404_NOT_FOUND = 404
    HTTP_405_METHOD_NOT_ALLOWED = 405


# ======================== Demo ========================
print("=== APIView Demo ===\n")

user = User("alice")
req = Request

# GET list
view = PostListAPIView.as_view()
resp = view(Request("GET", user=user))
print(f"GET /posts/ → {resp.status}")
print(resp.render()[:200])
print()

# POST create
resp = view(Request("POST", data={"title": "New Post", "content": "Fresh content"}, user=user))
print(f"POST /posts/ → {resp.status}")
print(resp.render())
print(f"  Total posts now: {len(POSTS)}")

# POST bad request
resp = view(Request("POST", data={"content": "No title"}, user=user))
print(f"\nPOST /posts/ (no title) → {resp.status}")
print(resp.render())

# GET detail
detail_view = PostDetailAPIView.as_view()
resp = detail_view(Request("GET", user=user), pk=1)
print(f"\nGET /posts/1/ → {resp.status}")
print(resp.render())

# PUT update
resp = detail_view(Request("PUT", data={"title": "Updated Title", "likes": 99}, user=user), pk=1)
print(f"\nPUT /posts/1/ → {resp.status}")
print(resp.render())

# GET 404
resp = detail_view(Request("GET", user=user), pk=999)
print(f"\nGET /posts/999/ → {resp.status}")
print(resp.render())

# DELETE
resp = detail_view(Request("DELETE", user=user), pk=3)
print(f"\nDELETE /posts/3/ → {resp.status}")
print(f"  Total posts now: {len(POSTS)}")

# Method not allowed
class ReadOnlyView(APIView):
    def get(self, request):
        return Response({"message": "read-only"})

ro_view = ReadOnlyView.as_view()
resp = ro_view(Request("POST", data={}, user=user))
print(f"\nPOST to read-only → {resp.status}")
print(resp.render())
