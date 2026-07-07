"""ViewSets & ModelViewSet: list, create, retrieve, update, destroy in one class."""
from typing import Any, Optional
import json


# ======================== Core ========================
class Request:
    def __init__(self, method="GET", data=None, query_params=None, user=None, action=None):
        self.method = method
        self.data = data or {}
        self.query_params = query_params or {}
        self.user = user or AnonymousUser()
        self.action = action


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


# ======================== ViewSet ========================

class ViewSet:
    """Combines list, create, retrieve, update, partial_update, destroy."""

    action_map = {
        "GET": {"list": "list", "detail": "retrieve"},
        "POST": {"list": "create"},
        "PUT": {"detail": "update"},
        "PATCH": {"detail": "partial_update"},
        "DELETE": {"detail": "destroy"},
    }

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        is_detail = pk is not None
        method_actions = self.action_map.get(request.method, {})
        action_name = method_actions.get("detail" if is_detail else "list")

        if not action_name:
            return Response({"error": "Method not allowed"}, status=405)

        handler = getattr(self, action_name, None)
        if not handler:
            return Response({"error": "Action not implemented"}, status=405)

        request.action = action_name
        if is_detail:
            return handler(request, pk=pk, *args, **kwargs)
        return handler(request, *args, **kwargs)

    @classmethod
    def as_view(cls, actions: dict = None):
        """Map methods to actions. If actions provided, override defaults."""
        def view(request, *args, **kwargs):
            instance = cls()
            if actions:
                method = request.method
                action_name = actions.get(method)
                if not action_name:
                    return Response({"error": "Method not allowed"}, status=405)
                handler = getattr(instance, action_name, None)
                if not handler:
                    return Response({"error": "Action not implemented"}, status=405)
                request.action = action_name
                return handler(request, *args, **kwargs)
            return instance.dispatch(request, *args, **kwargs)
        return view


# ======================== ModelViewSet ========================

class ModelViewSet(ViewSet):
    """Full CRUD ViewSet with queryset."""
    queryset = []

    def list(self, request):
        return Response({"count": len(self.queryset), "results": self.queryset})

    def create(self, request):
        data = request.data
        errors = self.validate(data)
        if errors:
            return Response({"errors": errors}, status=400)
        obj = self.perform_create(data)
        return Response(obj, status=201)

    def retrieve(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        return Response(obj)

    def update(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        obj.update(request.data)
        return Response(obj)

    def partial_update(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        for k, v in request.data.items():
            obj[k] = v
        return Response(obj)

    def destroy(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        self.queryset[:] = [item for item in self.queryset if item["id"] != pk]
        return Response({"message": "Deleted"}, status=204)

    def get_object(self, pk):
        return next((item for item in self.queryset if item["id"] == pk), None)

    def perform_create(self, data):
        obj = {
            "id": max((item["id"] for item in self.queryset), default=0) + 1,
            "title": data.get("title", "Untitled"),
            "content": data.get("content", ""),
            "author": data.get("author", "anonymous"),
        }
        self.queryset.append(obj)
        return obj

    def validate(self, data):
        errors = {}
        if not data.get("title"):
            errors["title"] = "Required."
        return errors


# ======================== Data ========================
POST_DATA = [
    {"id": 1, "title": "Hello Django", "content": "First", "author": "alice"},
    {"id": 2, "title": "DRF ViewSets", "content": "ViewSets rock", "author": "alice"},
    {"id": 3, "title": "Python Tips", "content": "Tips", "author": "bob"},
]


# ======================== Concrete ========================

class PostViewSet(ModelViewSet):
    queryset = POST_DATA


user = User("alice")


# ======================== Demo ========================
print("=== ViewSet & ModelViewSet Demo ===\n")

viewsets = PostViewSet()

# via as_view with action map
post_list = PostViewSet.as_view({"GET": "list", "POST": "create"})
post_detail = PostViewSet.as_view({"GET": "retrieve", "PUT": "update", "DELETE": "destroy"})
post_patch = PostViewSet.as_view({"PATCH": "partial_update"})

# GET list
resp = post_list(Request("GET", user=user))
print(f"GET /posts/ → {resp.status}: {json.loads(resp.render())['count']} posts")

# POST create
resp = post_list(Request("POST", data={"title": "ViewSet Post", "content": "Created via ViewSet", "author": "alice"}, user=user))
print(f"POST /posts/ → {resp.status}: created id={json.loads(resp.render())['id']}")

# GET detail
resp = post_detail(Request("GET", user=user), pk=1)
print(f"GET /posts/1/ → {resp.status}: {json.loads(resp.render())['title']}")

# PUT update
resp = post_detail(Request("PUT", data={"title": "Updated ViewSet", "likes": 50}, user=user), pk=1)
print(f"PUT /posts/1/ → {resp.status}: {json.loads(resp.render())['title']}")

# PATCH
resp = post_patch(Request("PATCH", data={"likes": 100}, user=user), pk=2)
print(f"PATCH /posts/2/ → {resp.status}: likes={json.loads(resp.render())['likes']}")

# DELETE
resp = post_detail(Request("DELETE", user=user), pk=3)
print(f"DELETE /posts/3/ → {resp.status}")
print(f"  Remaining: {len(POST_DATA)} posts")

# 404
resp = post_detail(Request("GET", user=user), pk=999)
print(f"\nGET /posts/999/ → {resp.status}: {json.loads(resp.render())['error']}")

# Router-like auto-generated URLs
print("\n--- Router would generate ---")
for prefix, actions in [("posts", {"GET": "list", "POST": "create"})]:
    for method, action in actions.items():
        print(f"  {method:6s} /{prefix}/        → {action}")
for prefix, actions in [("posts", {"GET": "retrieve", "PUT": "update", "PATCH": "partial_update", "DELETE": "destroy"})]:
    for method, action in actions.items():
        print(f"  {method:6s} /{prefix}/:id/   → {action}")
