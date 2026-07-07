# 📘 Django Phase 04 — Lesson 10: Integration — Full REST API

> 🎯 **Goal**: Build a complete REST API for the Auth Blog — combining serializers, views, permissions, pagination, and versioning.

## 📖 Concepts

### What We're Building
A REST API for the blog with:
- Public read access to published posts
- Authenticated post creation
- Owner-only edit/delete
- Admin-only publish action
- Comments per post
- Pagination, filtering, search
- Rate limiting

### Architecture
```
API Layer                Auth Layer           Data Layer
├── PostList             ├── IsAuthenticated  ├── Post model
├── PostDetail           ├── IsOwner          ├── Comment model
├── PostPublish          ├── IsAdminUser      └── User model
├── CommentList          └── TokenAuth
├── MyPosts
└── Router
```

### API Endpoints

| Method | Endpoint | Auth | Permission |
|--------|----------|------|------------|
| GET | `/api/v1/posts/` | No | AllowAny (published only) |
| POST | `/api/v1/posts/` | Yes | IsAuthenticated |
| GET | `/api/v1/posts/{id}/` | Yes | IsOwner |
| PUT | `/api/v1/posts/{id}/` | Yes | IsOwner |
| DELETE | `/api/v1/posts/{id}/` | Yes | IsOwner |
| POST | `/api/v1/posts/{id}/publish/` | Yes | IsAdminUser |
| GET | `/api/v1/posts/{id}/comments/` | Yes | IsAuthenticated |
| POST | `/api/v1/posts/{id}/comments/` | Yes | IsAuthenticated |
| GET | `/api/v1/my-posts/` | Yes | IsAuthenticated |

### Permission Flow
```
Request → Throttle check → Auth check → Permission check → Handler
                                                  ↓
                                          Has object perm? → 403
```

### ADHD-Friendly Summary
```
Anon: only published GET
Auth: create + own edit/delete
Admin: publish any post
Owner: edit/delete own posts
All: throttled by rate
```

## 🛠️ Code

```python
# serializers.py
class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'is_published',
                  'comments', 'comment_count', 'created_at']
        read_only_fields = ['id', 'author', 'is_published', 'created_at']


# permissions.py
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# views.py
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    pagination_class = PostPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'likes']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.is_published = True
        post.save()
        return Response({'status': 'published'})


# urls.py
router = DefaultRouter()
router.register('posts', PostViewSet)
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/my-posts/', MyPostList.as_view(), name='my-posts'),
]
```

## 🧪 Practice

Build the complete REST API:

1. **Setup**: Install djangorestframework, add to INSTALLED_APPS
2. **Serializers**: PostSerializer with nested comments, AuthorSerializer
3. **Permissions**: IsOwner, IsAdminOrReadOnly
4. **ViewSet**: PostViewSet with all CRUD + custom publish action
5. **Router**: DefaultRouter with version prefix `/api/v1/`
6. **Pagination**: 10 per page, configurable via `?page_size=`
7. **Search**: By title and content
8. **Throttling**: Anon 30/min, Auth 100/min
9. **Test**: Verify anon can only read published; owner can edit; admin can publish

## 🧠 Key Takeaways

- Routers + ViewSets = minimal URL config
- Stack permission classes for layered security
- Override `get_queryset()` to filter published posts for anon
- Custom `@action` for non-CRUD endpoints
- Always set `perform_create` to auto-assign the author
- Version your API from the start with URL prefix
