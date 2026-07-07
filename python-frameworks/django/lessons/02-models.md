# 🗄️ Django Models
<!-- ⏱️ 15 min | 🟡 Applied -->

**What You'll Learn:** Define database models, create migrations, and interact with data.

## The Concept

Django models are Python classes that map to database tables. Each attribute is a column. Django handles the SQL — you write Python.

## Define Models

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

## Field Types

| Field | Stores | Example |
|-------|--------|---------|
| `CharField` | Short text | Title, name |
| `TextField` | Long text | Blog content |
| `IntegerField` | Integer | Page views |
| `FloatField` | Float | Price |
| `BooleanField` | True/False | Is published |
| `DateTimeField` | Date + time | Created at |
| `ForeignKey` | Many-to-one | Post → Category |
| `ManyToManyField` | Many-to-many | Post → Tags |
| `OneToOneField` | One-to-one | User → Profile |

## Migrations

```bash
# Create migration files (detects model changes)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# See SQL without running it
python manage.py sqlmigrate blog 0001
```

## Code Example

```python
"""Django models — modeled as pure Python for learning."""
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Category:
    name: str
    slug: str

@dataclass
class Post:
    title: str
    slug: str
    content: str
    category: Category
    is_published: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

    def __str__(self):
        return self.title
```

## CRUD Operations

```python
# In Django shell or views
from blog.models import Category, Post

# Create
cat = Category.objects.create(name="Python", slug="python")
post = Post.objects.create(
    title="Hello Django",
    slug="hello-django",
    content="First post!",
    category=cat,
)

# Read
Post.objects.all()              # All posts
Post.objects.filter(is_published=True)  # Filtered
Post.objects.get(slug="hello-django")   # Single by slug

# Update
post.title = "Updated Title"
post.save()

# Delete
post.delete()
```

## Key Points
- Models = database tables. Change models → create migration → apply
- Always define `__str__` for readable admin display
- Use `related_name` in ForeignKey for reverse queries: `category.posts.all()`
- `auto_now_add=True` sets on create; `auto_now=True` updates on every save
