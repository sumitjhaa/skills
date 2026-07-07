"""Routers: automatic URL routing from ViewSets."""
from typing import Any, Optional
import json


# ======================== Core (condensed) ========================
class Request:
    def __init__(self, method="GET", data=None, user=None):
        self.method = method
        self.data = data or {}
        self.user = user or type("Anon", (), {"is_authenticated": False, "username": "Anonymous"})()


class Response:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    def render(self):
        return json.dumps(self.data, indent=2)


class User:
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True


# ======================== Router ========================

class Router:
    """DRF's SimpleRouter — auto-generate URL patterns from ViewSets."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix
        self.registry: list[tuple[str, Any, str]] = []  # (prefix, viewset, basename)

    def register(self, prefix: str, viewset: Any, basename: str = None):
        """Register a ViewSet with a URL prefix."""
        self.registry.append((prefix, viewset, basename or prefix))

    @property
    def urls(self) -> list[dict]:
        """Generate URL patterns. Returns list of route configs."""
        patterns = []
        for prefix, viewset, basename in self.registry:
            pk_pattern = f"{'/' if prefix else ''}{prefix}/{{pk}}/"
            list_pattern = f"{'/' if prefix else ''}{prefix}/"

            patterns.append({
                "pattern": list_pattern,
                "view": viewset.as_view({
                    "GET": "list",
                    "POST": "create",
                }),
                "name": f"{basename}-list",
            })
            patterns.append({
                "pattern": pk_pattern,
                "view": viewset.as_view({
                    "GET": "retrieve",
                    "PUT": "update",
                    "PATCH": "partial_update",
                    "DELETE": "destroy",
                }),
                "name": f"{basename}-detail",
            })
        return patterns

    def resolve(self, path: str, method: str) -> Optional[dict]:
        """Match a path + method to a route. Returns response or None."""
        for route in self.urls:
            pattern = route["pattern"]
            # Simple matching: check prefix
            if method == "GET" and pattern.endswith("/") and not "{pk}" in pattern:
                if path == pattern:
                    return route
            elif method == "GET" and "{pk}" in pattern:
                prefix_part = pattern.replace("{pk}", "")
                pk = path.replace(prefix_part, "")
                if pk.isdigit():
                    return {**route, "pk": int(pk)}
            elif method == "POST" and not "{pk}" in pattern:
                if path == pattern:
                    return route
            elif method in ("PUT", "PATCH", "DELETE") and "{pk}" in pattern:
                prefix_part = pattern.replace("{pk}", "")
                pk = path.replace(prefix_part, "")
                if pk.isdigit():
                    return {**route, "pk": int(pk)}
        return None


# ======================== ViewSet ========================

class ModelViewSet:
    queryset = []
    action = None

    @classmethod
    def as_view(cls, actions: dict):
        def view(request, *args, **kwargs):
            instance = cls()
            method = request.method
            action_name = actions.get(method)
            if not action_name:
                return Response({"error": "Method not allowed"}, status=405)
            instance.action = action_name
            handler = getattr(instance, action_name)
            return handler(request, *args, **kwargs)
        return view

    def list(self, request):
        return Response({"count": len(self.queryset), "results": self.queryset})

    def create(self, request):
        data = request.data
        obj = {
            "id": len(self.queryset) + 1,
            "title": data.get("title", "Untitled"),
            "content": data.get("content", ""),
        }
        self.queryset.append(obj)
        return Response(obj, status=201)

    def retrieve(self, request, pk=None):
        obj = next((item for item in self.queryset if item["id"] == pk), None)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        return Response(obj)

    def update(self, request, pk=None):
        obj = next((item for item in self.queryset if item["id"] == pk), None)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        obj.update(request.data)
        return Response(obj)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    def destroy(self, request, pk=None):
        self.queryset[:] = [item for item in self.queryset if item["id"] != pk]
        return Response({"message": "Deleted"}, status=204)


# ======================== Concrete ========================

class PostViewSet(ModelViewSet):
    queryset = [
        {"id": 1, "title": "Hello", "content": "First"},
        {"id": 2, "title": "Routers", "content": "Auto URL generation"},
    ]


class CommentViewSet(ModelViewSet):
    queryset = [
        {"id": 1, "text": "Great!", "post_id": 1},
        {"id": 2, "text": "Nice!", "post_id": 1},
    ]


# ======================== Demo ========================
print("=== Routers Demo ===\n")

router = Router()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

print("Generated URL patterns:")
for route in router.urls:
    print(f"  {route['pattern']:30s} → {route['name']}")

print("\n--- Simulating Requests ---")
user = User("alice")

test_paths = [
    ("GET", "/posts/"),
    ("GET", "/posts/1/"),
    ("POST", "/posts/"),
    ("PUT", "/posts/1/"),
    ("DELETE", "/posts/2/"),
    ("GET", "/comments/"),
    ("GET", "/comments/1/"),
]

for method, path in test_paths:
    route = router.resolve(path, method)
    if route:
        view = route["view"]
        pk = route.get("pk")
        if pk is not None:
            data = {"title": "Updated"} if method == "PUT" else {}
            resp = view(Request(method, data=data, user=user), pk=pk)
        elif method == "POST":
            resp = view(Request(method, data={"title": "New Post", "content": "Content"}, user=user))
        else:
            resp = view(Request(method, user=user))
        result = json.loads(resp.render())
        summary = result.get("title") or result.get("text") or result.get("message") or result.get("error") or f"{resp.status}"
        print(f"  {method:6s} {path:20s} → {resp.status}: {summary}")
    else:
        print(f"  {method:6s} {path:20s} → No route matched")
