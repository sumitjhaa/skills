# 📘 Django Phase 04 — Lesson 07: Pagination, Filtering & Ordering

> 🎯 **Goal**: Paginate large result sets, filter by fields, and order results in DRF.

## 📖 Concepts

### Pagination
Split large querysets into pages. Two main styles:

| Paginator | Query Params | Response |
|-----------|-------------|----------|
| `PageNumberPagination` | `?page=2&page_size=10` | `count`, `next`, `previous`, `results` |
| `LimitOffsetPagination` | `?limit=10&offset=20` | `count`, `limit`, `offset`, `results` |
| `CursorPagination` | `?cursor=xyz` | Opaque cursor (for real-time data) |

### Global Pagination
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
```

### Per-View Pagination
```python
class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination  # overrides global
```

### Filtering with django-filter
```python
# settings.py
INSTALLED_APPS = ['django_filters']
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# views.py
class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['author', 'is_published']
```

### Searching
```python
from rest_framework.filters import SearchFilter

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']
    # ?search=django → matches title or content containing "django"
```

### Ordering
```python
from rest_framework.filters import OrderingFilter

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'likes', 'title']
    ordering = ['-created_at']  # default
    # ?ordering=-likes → sort by likes descending
```

### ADHD-Friendly Summary
```
PageNumberPagination → ?page=2&page_size=10
DjangoFilterBackend  → ?author=alice&is_published=true
SearchFilter         → ?search=django  (icontains)
OrderingFilter       → ?ordering=-likes
Mix all backends together
```

## 🛠️ Code

```python
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer

class PostPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'likes']
    ordering = ['-created_at']

# GET /posts/?page=2&search=django&ordering=-likes&author=alice
```

## 🧪 Practice

1. Set up `PageNumberPagination` with page_size=3 on a BookList view
2. Add `DjangoFilterBackend` with `filterset_fields = ['author', 'genre']`
3. Add `SearchFilter` with `search_fields = ['title', 'description']`
4. Add `OrderingFilter` with `ordering_fields = ['price', 'published_date']`
5. Combine all three and test: `?search=python&ordering=-price&page=2`

## 🧠 Key Takeaways

- `PAGE_SIZE` in settings sets the global default
- Override `pagination_class` per view for custom sizes
- Filter backends stack — combine DjangoFilter, SearchFilter, OrderingFilter
- `search_fields` uses `icontains` by default
- Prepend `-` in ordering for descending
