# 📘 Django Phase 04 — Lesson 03: Generic Views

> 🎯 **Goal**: Use DRF's generic views (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) to reduce boilerplate.

## 📖 Concepts

### Mixin Chain
DRF generic views are built from reusable mixins:

| Mixin | Method | Action |
|-------|--------|--------|
| `ListModelMixin` | GET | List queryset |
| `CreateModelMixin` | POST | Create instance |
| `RetrieveModelMixin` | GET (detail) | Single instance |
| `UpdateModelMixin` | PUT | Full update |
| `DestroyModelMixin` | DELETE | Delete instance |

### Concrete Generic Views

| View | GET | POST | PUT | DELETE |
|------|-----|------|-----|--------|
| `ListAPIView` | ✅ list | — | — | — |
| `CreateAPIView` | — | ✅ create | — | — |
| `ListCreateAPIView` | ✅ list | ✅ create | — | — |
| `RetrieveAPIView` | ✅ detail | — | — | — |
| `UpdateAPIView` | — | — | ✅ update | — |
| `DestroyAPIView` | — | — | — | ✅ destroy |
| `RetrieveUpdateDestroyAPIView` | ✅ detail | — | ✅ update | ✅ destroy |
| `RetrieveDestroyAPIView` | ✅ detail | — | — | ✅ destroy |

### Minimum Setup
```python
class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

### Override Behavior
```python
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

### ADHD-Friendly Summary
```
ListCreateAPIView   → GET list + POST create
RetrieveUpdateDestroyAPIView → GET/PUT/DELETE detail
Set queryset + serializer_class → done
Override perform_create for author
```

## 🛠️ Code

```python
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Post
from .serializers import PostSerializer

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Even shorter with router-friendly setup:
# URLs
urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
```

## 🧪 Practice

1. Create `BookList(ListCreateAPIView)` and `BookDetail(RetrieveUpdateDestroyAPIView)`
2. Override `get_queryset` to filter by `?author=` query param
3. Override `perform_create` to auto-set author
4. Add pagination by setting `pagination_class`
5. Add search by setting `filter_backends` and `search_fields`

## 🧠 Key Takeaways

- Generic views save 80% boilerplate vs raw `APIView`
- Set `queryset` and `serializer_class` — that's the minimum
- Override `get_queryset()` for per-user filtering
- Override `perform_create()` for auto-author or custom logic
- Combine with mixins for custom combos
