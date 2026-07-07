# 🧩 Class-Based Views
<!-- ⏱️ 12 min | 🟡 Applied -->

**What You'll Learn:** Use Django's generic class-based views (CBVs) to write less code.

## The Concept

Function views work. Class-based views save repetition. Django provides built-in views for common patterns: list, detail, create, update, delete.

## Generic Display Views

```python
# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
```

## Generic Edit Views

```python
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'slug', 'content', 'category']
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'category']
    slug_field = 'slug'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'slug': self.object.slug})

class PostDeleteView(DeleteView):
    model = Post
    slug_field = 'slug'
    success_url = reverse_lazy('post_list')
```

## URL Patterns

```python
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
```

## Mixin Pattern

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminPostCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
```

## Code Example

```python
"""Class-based views — pure Python simulation."""
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class HttpRequest:
    user: str = 'anonymous'
    method: str = 'GET'

@dataclass
class HttpResponse:
    content: str = ''
    status: int = 200


class View:
    """Base class-based view."""
    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        handler = getattr(self, request.method.lower(), None)
        if handler is None:
            return HttpResponse(content="Method not allowed", status=405)
        return handler(request, *args, **kwargs)

    @classmethod
    def as_view(cls) -> Callable:
        def view(request, *args, **kwargs):
            instance = cls()
            return instance.dispatch(request, *args, **kwargs)
        return view


class ListView(View):
    model_name: str = 'items'
    items: list = field(default_factory=list)

    def get(self, request):
        items_str = '\n'.join(f"  - {item}" for item in self.items)
        return HttpResponse(content=f"{self.model_name}:\n{items_str}")


class DetailView(View):
    item: str = ''

    def get(self, request, **kwargs):
        return HttpResponse(content=f"Detail: {self.item}")


# Subclass with concrete data
class PostListView(ListView):
    model_name = 'Posts'
    items = ['Hello Django', 'Django Models', 'Django Views']

class PostDetailView(DetailView):
    def get(self, request, **kwargs):
        posts = {'hello-django': 'First post!', 'django-models': 'Second post!'}
        slug = kwargs.get('slug', '')
        content = posts.get(slug, 'Not found')
        return HttpResponse(content=f"Post '{slug}': {content}")


# Usage
list_view = PostListView.as_view()
print(list_view(HttpRequest()).content)

detail_view = PostDetailView.as_view()
print(detail_view(HttpRequest(), slug='hello-django').content)
```

## CBV Cheatsheet

| View | Purpose | Template (default) | Context |
|------|---------|-------------------|---------|
| `ListView` | List objects | `model_list.html` | `object_list`, `model_list` |
| `DetailView` | Single object | `model_detail.html` | `object`, `model` |
| `CreateView` | Create form | `model_form.html` | `form` |
| `UpdateView` | Edit form | `model_form.html` | `form`, `object` |
| `DeleteView` | Confirm delete | `model_confirm_delete.html` | `object` |

## Key Points
- CBVs reduce boilerplate — set `model` and `fields`, get CRUD free
- Override `get_queryset()` to filter, `get_context_data()` to add extra data
- Mixins (like `LoginRequiredMixin`) add cross-cutting behavior
- Use `as_view()` in URL patterns, not directly
- `reverse_lazy()` is for class attributes (URLs not loaded yet)
