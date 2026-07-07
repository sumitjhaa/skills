# 🎯 Integration: Blog Engine
<!-- ⏱️ 20 min | 🔴 Mastery -->

**What You'll Learn:** Build a complete blog engine combining models, admin, views, templates, URLs, forms, and CBVs.

## The Complete Blog

```python
"""Blog engine — complete Django app concept in pure Python."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import re


# ── Models ──
@dataclass
class Category:
    name: str
    slug: str

@dataclass
class Tag:
    name: str
    slug: str

@dataclass
class Post:
    title: str
    slug: str
    content: str
    category: Optional[Category] = None
    tags: list = field(default_factory=list)
    is_published: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# ── Storage ──
class BlogDB:
    def __init__(self):
        self.posts: dict[str, Post] = {}
        self.categories: dict[str, Category] = {}

    def add_post(self, post: Post):
        self.posts[post.slug] = post

    def get_published(self):
        return [p for p in self.posts.values() if p.is_published]

    def get_by_slug(self, slug: str) -> Optional[Post]:
        return self.posts.get(slug)

# ── Template Engine ──
def render(template: str, context: dict) -> str:
    result = template
    for key, value in context.items():
        result = result.replace(f'{{{{{key}}}}}', str(value))
    return result

# ── Admin ──
admin_site = {}
def admin_register(name, config):
    admin_site[name] = config

# ── Demo ──
db = BlogDB()

# Create categories
cat_python = Category("Python", "python")
cat_django = Category("Django", "django")
db.categories = {"python": cat_python, "django": cat_django}

# Create posts
posts_data = [
    Post("Getting Started with Python", "python-intro", "Python is awesome...", cat_python, ["beginner"], True),
    Post("Django Models Guide", "django-models", "Models define your data...", cat_django, ["database"], True),
    Post("Django Views Explained", "django-views", "Views handle requests...", cat_django, ["intermediate"], True),
    Post("Draft: Advanced Topics", "advanced", "Coming soon...", cat_django, [], False),
]
for p in posts_data:
    db.add_post(p)

# Admin registration
admin_register("Post", {"list_display": ["title", "category", "is_published"]})

# Views
def post_list():
    posts = db.get_published()
    template = "<h1>Blog Posts</h1>\n{% for post in posts %}<h2>{{title}}</h2>\n<p>{{content}}</p>\n{% endfor %}"
    rendered = ""
    for p in posts:
        rendered += f"<h2><a href='/posts/{p.slug}/'>{p.title}</a></h2>\n"
        rendered += f"<p>{p.content[:50]}...</p>\n"
        rendered += f"<small>Category: {p.category.name}</small>\n\n"
    return f"<h1>My Blog</h1>\n{rendered}"

def post_detail(slug: str):
    post = db.get_by_slug(slug)
    if not post or not post.is_published:
        return "<h1>404</h1><p>Post not found.</p>"
    return f"<h1>{post.title}</h1>\n<p>{post.content}</p>\n<small>Category: {post.category.name}</small>"

# URLs
routes = [
    (r'^$', lambda: post_list()),
    (r'^posts/(?P<slug>[-\w]+)/$', lambda slug: post_detail(slug)),
]

# Simulate requests
for path, handler in [('/', None), ('/posts/python-intro/', None)]:
    for pattern, view in routes:
        match = re.match(pattern, path)
        if match:
            result = view(**match.groupdict()) if match.groupdict() else view()
            print(f"=== {path} ===")
            print(result[:200])
            print()
            break
```

## What We Built

- **Models:** Post, Category, Tag with relationships
- **Admin:** Registered models with `list_display`
- **Views:** Post list (published only) and detail view
- **Templates:** HTML rendering with template engine
- **URLs:** Pattern matching with slug parameter
- **Database:** In-memory storage with query methods

## Key Files in Real Django

```
blog/
├── models.py          # Post, Category, Tag
├── admin.py           # PostAdmin, CategoryAdmin
├── views.py           # PostListView, PostDetailView
├── urls.py            # URL patterns
├── forms.py           # PostForm, CommentForm
├── templates/
│   ├── base.html
│   └── blog/
│       ├── post_list.html
│       ├── post_detail.html
│       └── post_form.html
└── tests.py           # Tests for everything
```

## Key Points
- One app, one responsibility: blog app handles blog features
- Admin gives you free CRUD — register everything
- Templates are HTML + Django template language
- URLs use `slug` for SEO-friendly paths
- This pattern scales: add features by adding views, not rewriting structure
