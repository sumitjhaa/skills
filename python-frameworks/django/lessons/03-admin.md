# 🎛️ Django Admin
<!-- ⏱️ 10 min | 🟡 Applied -->

**What You'll Learn:** Use Django's built-in admin interface to manage your data.

## Register Models

```python
# blog/admin.py
from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'created_at']
    list_filter = ['is_published', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Mark selected posts as published"
```

## Create Superuser

```bash
python manage.py createsuperuser
# Enter username, email, password
# Login at http://127.0.0.1:8000/admin/
```

## Code Example

```python
"""Django admin concepts — pure Python simulation."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class ModelAdmin:
    model_name: str
    list_display: list = None
    list_filter: list = None
    search_fields: list = None
    actions: list = None

# Simulated admin registration
admin_site = {}

def register(model_admin):
    name = model_admin.model_name
    admin_site[name] = model_admin
    print(f"Registered {name} in admin")
    print(f"  list_display: {model_admin.list_display}")
    print(f"  list_filter: {model_admin.list_filter}")
    print(f"  search_fields: {model_admin.search_fields}")

# Register Post admin
post_admin = ModelAdmin(
    model_name="Post",
    list_display=['title', 'category', 'is_published', 'created_at'],
    list_filter=['is_published', 'category', 'created_at'],
    search_fields=['title', 'content'],
)

register(post_admin)

print(f"\nAdmin site has {len(admin_site)} registered models")
for name, config in admin_site.items():
    print(f"  /admin/{name.lower()}/ → {config.model_name}")
```

## Key Points
- Admin is free CRUD UI — register your models and you're done
- `list_display` controls columns shown in list view
- `prepopulated_fields` auto-fills slug from title
- `actions` add batch operations (publish, delete, export)
- Create superuser first, then login at `/admin/`
