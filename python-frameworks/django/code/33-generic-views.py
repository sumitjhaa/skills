"""Generic views: ListCreateAPIView, RetrieveUpdateDestroyAPIView."""
from typing import Any, Optional
from functools import wraps
import json


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", data=None, query_params=None, user=None):
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.user = user or AnonymousUser()


class Response:
    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self):
        return json.dumps(self.data, indent=2)


class AnonymousUser:
    is_authenticated = False
    username = "Anonymous"


class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True


# ======================== Mixins ========================

class CreateModelMixin:
    """POST: create a new instance."""
    def create(self, request, *args, **kwargs):
        data = request.data
        errors = self.validate(data)
        if errors:
            return Response({"errors": errors}, status=400)
        instance = self.perform_create(data)
        return Response(instance, status=201)

    def perform_create(self, data):
        return self.create_object(data)

    def validate(self, data):
        return {}


class ListModelMixin:
    """GET: list instances."""
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate(queryset, request)
        return Response({"count": len(queryset), "results": page})


class RetrieveModelMixin:
    """GET: retrieve single instance."""
    def retrieve(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        return Response(obj)


class UpdateModelMixin:
    """PUT: update instance."""
    def update(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        data = request.data
        errors = self.validate(data)
        if errors:
            return Response({"errors": errors}, status=400)
        obj.update(data)
        return Response(obj)


class DestroyModelMixin:
    """DELETE: delete instance."""
    def destroy(self, request, pk, *args, **kwargs):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        self.perform_destroy(pk)
        return Response({"message": "Deleted"}, status=204)


# ======================== Generic Views ========================

class GenericAPIView:
    """Base with queryset, serializer, pagination."""
    queryset = []
    serializer_class = None

    def get_queryset(self):
        return list(self.queryset)

    def get_object(self, pk):
        return next((item for item in self.queryset if item["id"] == pk), None)

    def paginate(self, queryset, request):
        page_size = int(request.query_params.get("page_size", 10))
        page = int(request.query_params.get("page", 1))
        start = (page - 1) * page_size
        return queryset[start:start + page_size]

    def create_object(self, data):
        raise NotImplementedError

    def validate(self, data):
        return {}


class ListCreateAPIView(CreateModelMixin, ListModelMixin, GenericAPIView):
    """GET / → list; POST / → create."""
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return self.list(request, *args, **kwargs)
        if request.method == "POST":
            return self.create(request, *args, **kwargs)
        return Response({"error": "Method not allowed"}, status=405)


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """GET/PUT/DELETE /:id/"""
    def dispatch(self, request, pk, *args, **kwargs):
        if request.method == "GET":
            return self.retrieve(request, pk, *args, **kwargs)
        if request.method == "PUT":
            return self.update(request, pk, *args, **kwargs)
        if request.method == "DELETE":
            return self.destroy(request, pk, *args, **kwargs)
        return Response({"error": "Method not allowed"}, status=405)


# ======================== Data ========================
POST_DATA = [
    {"id": 1, "title": "Hello Django", "content": "First post", "author": "alice", "likes": 12},
    {"id": 2, "title": "DRF Guide", "content": "REST framework", "author": "alice", "likes": 8},
    {"id": 3, "title": "Python Tips", "content": "Tips and tricks", "author": "bob", "likes": 5},
]
NEXT_ID = 4


# ======================== Concrete Views ========================

class PostList(ListCreateAPIView):
    queryset = POST_DATA

    def create_object(self, data):
        global NEXT_ID
        obj = {
            "id": NEXT_ID,
            "title": data.get("title", "Untitled"),
            "content": data.get("content", ""),
            "author": data.get("author", "anonymous"),
            "likes": 0,
        }
        NEXT_ID += 1
        self.queryset.append(obj)
        return obj

    def validate(self, data):
        errors = {}
        if not data.get("title"):
            errors["title"] = "This field is required."
        if len(data.get("title", "")) < 3:
            errors["title"] = "Must be at least 3 characters."
        return errors


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = POST_DATA


user = User("alice")

# Demo
print("=== Generic Views Demo ===\n")

list_view = PostList()
detail_view = PostDetail()

# GET list
resp = list_view.dispatch(Request("GET", user=user))
print(f"GET /posts/ → {resp.status}")
data = json.loads(resp.render())
print(f"  Count: {data['count']}")
print(f"  Results: {len(data['results'])} posts")

# POST create (valid)
resp = list_view.dispatch(Request("POST", data={"title": "New Post", "content": "Content", "author": "alice"}, user=user))
print(f"\nPOST /posts/ (valid) → {resp.status}")
print(f"  Created: {json.loads(resp.render())['title']}")

# POST create (invalid)
resp = list_view.dispatch(Request("POST", data={"title": "AB", "content": ""}, user=user))
print(f"\nPOST /posts/ (invalid) → {resp.status}")
print(f"  Errors: {json.loads(resp.render())['errors']}")

# GET detail
resp = detail_view.dispatch(Request("GET", user=user), pk=1)
print(f"\nGET /posts/1/ → {resp.status}")
print(f"  Post: {json.loads(resp.render())['title']}")

# PUT update
resp = detail_view.dispatch(Request("PUT", data={"title": "Updated!", "likes": 99}, user=user), pk=1)
print(f"\nPUT /posts/1/ → {resp.status}")
print(f"  Updated: {json.loads(resp.render())['title']}, likes={json.loads(resp.render())['likes']}")

# DELETE
resp = detail_view.dispatch(Request("DELETE", user=user), pk=3)
print(f"\nDELETE /posts/3/ → {resp.status}")

# GET 404
resp = detail_view.dispatch(Request("GET", user=user), pk=999)
print(f"\nGET /posts/999/ → {resp.status}")
print(f"  {json.loads(resp.render())['error']}")
