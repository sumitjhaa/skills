# 📘 Django Phase 04 — Lesson 06: Authentication & Permissions

> 🎯 **Goal**: Secure API endpoints with authentication classes and permission classes.

## 📖 Concepts

### Authentication vs Permission
```
Authentication  → Who is this?  (identify user)
Permission      → Are they allowed?  (check access)
```

### Authentication Classes

| Class | How It Works |
|-------|-------------|
| `SessionAuthentication` | Django session cookie |
| `TokenAuthentication` | `Authorization: Token xyz` header |
| `JWTAuthentication` | `Authorization: Bearer xyz` (djangorestframework-simplejwt) |
| `BasicAuthentication` | HTTP Basic Auth (dev only) |

### Built-in Permission Classes

| Class | Access |
|-------|--------|
| `AllowAny` | Everyone |
| `IsAuthenticated` | Only logged-in users |
| `IsAdminUser` | Only `is_staff=True` |
| `IsAuthenticatedOrReadOnly` | Auth for write, anon for read |
| `DjangoModelPermissions` | Per-model perms from Django |
| `DjangoObjectPermissions` | Per-object perms |

### Setting Permissions
```python
# Per view
class PostList(APIView):
    permission_classes = [IsAuthenticated]

# Per viewset
class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

# Global (settings.py)
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Custom Permission
```python
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
```

### ADHD-Friendly Summary
```
Auth → identifikasi user
Perm → cek izin
permission_classes = [IsAuthenticated, IsOwner]
SAFE_METHODS = GET, HEAD, OPTIONS (read-only)
```

## 🛠️ Code

```python
# permissions.py
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# views.py
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsAuthorOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

## 🧪 Practice

1. Create a view with `IsAuthenticated` — verify anon gets 403
2. Create an `IsAdminOrReadOnly` permission class
3. Apply `IsAuthenticatedOrReadOnly` to a ViewSet
4. Create object-level `IsOwner` permission
5. Set global `DEFAULT_PERMISSION_CLASSES` to `IsAuthenticated`

## 🧠 Key Takeaways

- Auth classes identify; permission classes authorize
- `has_permission()` = view-level (runs first)
- `has_object_permission()` = object-level (runs on `get_object()`)
- `SAFE_METHODS` = read-only (GET, HEAD, OPTIONS)
- Stack multiple permissions — all must pass
