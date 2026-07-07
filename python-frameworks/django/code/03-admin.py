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
