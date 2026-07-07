"""DRF authentication & permissions: IsAuthenticated, IsAdminUser, custom perms."""
from typing import Any, Optional
from functools import wraps
import json


# ======================== Request/Response ========================
class Request:
    def __init__(self, method="GET", data=None, user=None, auth=None):
        self.method = method
        self.data = data or {}
        self.user = user or AnonymousUser()
        self.auth = auth
        self.successful_authenticator = None


class Response:
    def __init__(self, data, status=200, headers=None):
        self.data = data
        self.status = status
        self.headers = headers or {}

    def render(self):
        return json.dumps(self.data, indent=2)


# ======================== Auth ========================
class AnonymousUser:
    is_authenticated = False
    is_active = False
    is_staff = False
    is_superuser = False
    username = "Anonymous"
    id = None

    def has_perm(self, perm: str) -> bool:
        return False


class User:
    def __init__(self, username, is_staff=False, is_superuser=False, perms=None):
        self.id = hash(username) % 10000
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = is_staff
        self.is_superuser = is_superuser
        self._perms = perms or set()

    def has_perm(self, perm: str) -> bool:
        if self.is_superuser:
            return True
        return perm in self._perms


# ======================== Permission Classes ========================

class BasePermission:
    """Base permission class. Override has_permission and has_object_permission."""
    def has_permission(self, request, view) -> bool:
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        return True


class AllowAny(BasePermission):
    def has_permission(self, request, view) -> bool:
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.is_authenticated


class IsAdminUser(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated and request.user.is_staff


class IsAuthenticatedOrReadOnly(BasePermission):
    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view) -> bool:
        if request.method in self.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class DjangoModelPermissions(BasePermission):
    """Check user.has_perm for the view's model."""
    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view) -> bool:
        if request.user.is_superuser:
            return True
        model_cls = getattr(view, "model_cls", None)
        if not model_cls:
            return True
        app_label = getattr(model_cls, "app_label", "blog")
        model_name = getattr(model_cls, "model_name", "post")
        required_perms = self.perms_map.get(request.method, [])
        for perm in required_perms:
            perm_str = perm % {"app_label": app_label, "model_name": model_name}
            if not request.user.has_perm(perm_str):
                return False
        return True


class IsOwner(BasePermission):
    """Object-level: only the owner can modify."""
    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        owner = getattr(obj, "author", None) or getattr(obj, "user", None)
        return owner == request.user.username


# ======================== Permissioned APIView ========================

class APIView:
    permission_classes = [AllowAny]
    model_cls = None

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        # Check permissions
        for perm_class in self.permission_classes:
            perm = perm_class()
            if not perm.has_permission(request, self):
                return Response({"detail": "Permission denied"}, status=403)

        handler = getattr(self, request.method.lower(), None)
        if handler is None:
            return Response({"error": "Method not allowed"}, status=405)
        return handler(request, *args, **kwargs)

    def check_object_permissions(self, request, obj):
        for perm_class in self.permission_classes:
            perm = perm_class()
            if not perm.has_object_permission(request, self, obj):
                return False
        return True

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            instance = cls()
            return instance.dispatch(request, *args, **kwargs)
        return view


# ======================== Data ========================
POSTS = [
    {"id": 1, "title": "Hello", "content": "First", "author": "alice"},
    {"id": 2, "title": "DRF Auth", "content": "Permissions", "author": "alice"},
    {"id": 3, "title": "Secrets", "content": "Admin only", "author": "admin"},
]


# ======================== Views ========================

class PublicPostList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"results": POSTS})


class AuthenticatedPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"results": POSTS, "user": request.user.username})


class AdminPostList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"results": POSTS, "admin": request.user.username})


class ReadOnlyOrAuth(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({"results": POSTS})

    def post(self, request):
        return Response({"created": True, "user": request.user.username}, status=201)


class OwnerPostDetail(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        return next((p for p in POSTS if p["id"] == pk), None)

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        if not self.check_object_permissions(request, obj):
            return Response({"detail": "You do not own this object"}, status=403)
        return Response(obj)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        if not self.check_object_permissions(request, obj):
            return Response({"detail": "You do not own this object"}, status=403)
        obj.update(request.data)
        return Response(obj)


# ======================== Demo ========================
print("=== DRF Auth & Permissions Demo ===\n")

alice = User("alice")
admin = User("admin", is_staff=True, is_superuser=True)
anon = AnonymousUser()

# AllowAny
view = PublicPostList.as_view()
resp = view(Request("GET", user=anon))
print(f"AllowAny (anon): {resp.status} — public access OK")

# IsAuthenticated
view = AuthenticatedPostList.as_view()
resp = view(Request("GET", user=anon))
print(f"IsAuthenticated (anon): {resp.status}")
resp = view(Request("GET", user=alice))
print(f"IsAuthenticated (alice): {resp.status} — {json.loads(resp.render())['user']}")

# IsAdminUser
view = AdminPostList.as_view()
resp = view(Request("GET", user=alice))
print(f"\nIsAdminUser (alice): {resp.status}")
resp = view(Request("GET", user=admin))
print(f"IsAdminUser (admin): {resp.status} — {json.loads(resp.render())['admin']}")

# IsAuthenticatedOrReadOnly
view = ReadOnlyOrAuth.as_view()
resp = view(Request("GET", user=anon))
print(f"\nReadOnlyOrAuth GET (anon): {resp.status}")
resp = view(Request("POST", data={}, user=anon))
print(f"ReadOnlyOrAuth POST (anon): {resp.status}")
resp = view(Request("POST", data={}, user=alice))
print(f"ReadOnlyOrAuth POST (alice): {resp.status}")

# IsOwner
view = OwnerPostDetail.as_view()
resp = view(Request("GET", user=alice), pk=1)
print(f"\nIsOwner GET post1 (alice): {resp.status} — {json.loads(resp.render())['title']}")
resp = view(Request("PUT", data={"title": "Hacked"}, user=bob), pk=1)
print(f"IsOwner PUT post1 (bob):   {resp.status} — {json.loads(resp.render()).get('detail', '?')}")
resp = view(Request("PUT", data={"title": "My Edit"}, user=alice), pk=1)
print(f"IsOwner PUT post1 (alice): {resp.status} — title={json.loads(resp.render())['title']}")
