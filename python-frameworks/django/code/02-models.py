"""Django models — pure Python version for learning without Django."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Category:
    name: str
    slug: str

    def __str__(self):
        return self.name


@dataclass
class Post:
    title: str
    slug: str
    content: str
    category: Optional[Category] = None
    is_published: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def __str__(self):
        return self.title

    def publish(self):
        self.is_published = True
        self.updated_at = datetime.now(timezone.utc)


# Demo
cat = Category(name="Python", slug="python")
post = Post(
    title="Hello Django",
    slug="hello-django",
    content="This is my first Django post!",
    category=cat,
)

print(f"Post: {post}")
print(f"Category: {post.category}")
print(f"Published: {post.is_published}")

post.publish()
print(f"After publish: {post.is_published}")
print(f"Updated at: {post.updated_at}")
