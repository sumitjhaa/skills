# 📘 Django Phase 04 — Lesson 04: ViewSets

> 🎯 **Goal**: Use `ViewSet` and `ModelViewSet` to combine list + detail actions into one class.

## 📖 Concepts

### ViewSet
A `ViewSet` groups all CRUD actions in one class:

| Action | Method | URL |
|--------|--------|-----|
| `list` | GET | `/posts/` |
| `create` | POST | `/posts/` |
| `retrieve` | GET | `/posts/:id/` |
| `update` | PUT | `/posts/:id/` |
| `partial_update` | PATCH | `/posts/:id/` |
| `destroy` | DELETE | `/posts/:id/` |

### ModelViewSet
`ModelViewSet` = `GenericViewSet` + all mixins. Full CRUD in 3 lines:

```python
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

### Custom Actions
Add extra routes with the `@action` decorator:

```python
from rest_framework.decorators import action

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        return Response({'status': 'published'})

    @action(detail=False, methods=['get'])
    def recent(self, request):
        posts = Post.objects.all()[:5]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
```

### ViewSet Types

| ViewSet | Default Actions |
|---------|----------------|
| `ViewSet` | None (you define) |
| `GenericViewSet` | None + generic behavior |
| `ModelViewSet` | All CRUD |
| `ReadOnlyModelViewSet` | `list` + `retrieve` only |

### ADHD-Friendly Summary
```
ModelViewSet → list, create, retrieve, update, partial_update, destroy
@action(detail=True) → /posts/:id/publish/
@action(detail=False) → /posts/recent/
One class replaces 2+ APIViews
```

## 🛠️ Code

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        return Response({'status': 'published'})

    @action(detail=False)
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

## 🧪 Practice

1. Create a `BookViewSet(ModelViewSet)` with `queryset` and `serializer_class`
2. Add a `@action(detail=True)` called `checkout` that sets `is_checked_out=True`
3. Add a `@action(detail=False)` called `available` that filters `is_checked_out=False`
4. Override `perform_create` to set `added_by=self.request.user`
5. Create a `ReadOnlyModelViewSet` for categories

## 🧠 Key Takeaways

- `ModelViewSet` = one class for full CRUD
- `@action(detail=True)` for per-instance custom actions
- `@action(detail=False)` for collection-level custom actions
- ViewSets need a Router to generate URLs
- `perform_create()` is the hook for extra save logic
