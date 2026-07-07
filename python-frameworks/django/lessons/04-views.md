# 👁️ Views & Request Handling
<!-- ⏱️ 12 min | 🟡 Applied -->

**What You'll Learn:** Handle HTTP requests, return responses, and use Django's request/response objects.

## Function-Based Views

```python
# blog/views.py
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Post

def home(request):
    return HttpResponse("Welcome to my blog!")

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_list_json(request):
    posts = Post.objects.filter(is_published=True).values('title', 'slug', 'created_at')
    return JsonResponse(list(posts), safe=False)
```

## URL Patterns

```python
# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('api/posts/', views.post_list_json, name='post_list_json'),
]

# myproject/urls.py
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Include blog URLs
]
```

## Code Example

```python
"""View concepts — pure Python simulation."""
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class HttpRequest:
    method: str = 'GET'
    path: str = '/'
    GET: dict = field(default_factory=dict)
    POST: dict = field(default_factory=dict)

@dataclass
class HttpResponse:
    content: str = ''
    status_code: int = 200
    content_type: str = 'text/html'

@dataclass
class JsonResponse(HttpResponse):
    content_type: str = 'application/json'

# Simulated view functions
def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="<h1>Welcome to my blog!</h1>")

def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    # Simulate database lookup
    posts = {
        'hello-django': {'title': 'Hello Django', 'content': 'First post!'},
        'django-models': {'title': 'Django Models', 'content': 'Second post!'},
    }
    post = posts.get(slug)
    if not post:
        return HttpResponse(content="Not found", status_code=404)
    content = f"<h1>{post['title']}</h1><p>{post['content']}</p>"
    return HttpResponse(content=content)

# Test
req = HttpRequest(path='/')
resp = home(req)
print(f"GET {req.path} → {resp.status_code}")
print(resp.content[:50])

req2 = HttpRequest(path='/posts/hello-django/')
resp2 = post_detail(req2, 'hello-django')
print(f"\nGET {req2.path} → {resp2.status_code}")
print(resp2.content)

req3 = HttpRequest(path='/posts/nonexistent/')
resp3 = post_detail(req3, 'nonexistent')
print(f"\nGET {req3.path} → {resp3.status_code}")
print(resp3.content)
```

## URL Patterns Reference

| Pattern | Matches | Example |
|---------|---------|---------|
| `str:name` | Any string (no `/`) | `hello-world` |
| `int:id` | Integer | `42` |
| `slug:slug` | Slug (letters, numbers, hyphens) | `hello-django` |
| `uuid:id` | UUID | `550e8400-...` |
| `path:path` | Full path (with `/`) | `2024/01/hello/` |

## Key Points
- Views are functions (or classes) that take a request and return a response
- `render()` combines a template with context data
- `get_object_or_404()` returns 404 if object doesn't exist
- `JsonResponse` converts dicts/lists to JSON
- Always use named URL patterns (`name='home'`) — reference with `{% url 'home' %}`
