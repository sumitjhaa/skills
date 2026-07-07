# 🔗 URLs & Routing
<!-- ⏱️ 10 min | 🟡 Applied -->

**What You'll Learn:** Design URL patterns, pass parameters, use namespaces, and reverse URLs.

## URL Patterns

```python
# blog/urls.py
from django.urls import path, include
from . import views

app_name = 'blog'  # Namespace for this app

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/', views.ArticleArchiveView.as_view(), name='archive'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]
```

## Including App URLs

```python
# myproject/urls.py
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),         # No prefix
    path('blog/', include('blog.urls')),    # With /blog/ prefix
    path('api/', include('blog.api_urls')), # Separate API URLs
]
```

## Reversing URLs

```python
# In views
from django.urls import reverse
from django.shortcuts import redirect

def redirect_to_post(request, slug):
    url = reverse('blog:post_detail', kwargs={'slug': slug})
    return redirect(url)

# In templates
<a href="{% url 'blog:post_detail' slug=post.slug %}">{{ post.title }}</a>
```

## Code Example

```python
"""URL routing — pure Python simulation."""
from dataclasses import dataclass, field
import re
from typing import Callable, Optional


@dataclass
class URLPattern:
    pattern: str
    view: Callable
    name: str = ''


class URLResolver:
    def __init__(self):
        self.patterns: list[URLPattern] = []

    def add(self, pattern: str, view: Callable, name: str = ''):
        self.patterns.append(URLPattern(pattern, view, name))

    def resolve(self, path: str):
        for p in self.patterns:
            regex = p.pattern.replace('<slug:slug>', r'(?P<slug>[-\w]+)')
            regex = regex.replace('<int:id>', r'(?P<id>\d+)')
            match = re.match(f'^{regex}$', path)
            if match:
                return p.view(**match.groupdict())
        return None


def post_detail(slug: str):
    return f"Viewing post: {slug}"

def archive(year: str, month: str):
    return f"Archive: {year}-{month}"


router = URLResolver()
router.add('post/<slug:slug>/', post_detail, name='post_detail')
router.add('archive/<int:id>/', archive, name='archive')

for path in ['post/hello-django/', 'archive/42/', 'nonexistent/']:
    result = router.resolve(path)
    print(f"  {path} → {result}")
```

## Key Points
- Use `path()` converters: `str`, `int`, `slug`, `uuid`, `path`
- `app_name = 'blog'` creates namespace — reference as `blog:post_detail`
- `include()` lets you split URLs across apps
- Use `reverse()` in views and `{% url %}` in templates (never hardcode URLs)
- Order matters — Django matches first pattern, so put specific routes first
