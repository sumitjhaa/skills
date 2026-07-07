"""Custom managers & QuerySets."""
from dataclasses import dataclass, field
from typing import Any, Optional, Callable


# --- Simulated model with custom manager ---
class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = results or list(table)

    def filter(self, **kwargs) -> "QuerySet":
        def match(item):
            return all(item.get(k) == v for k, v in kwargs.items())
        return QuerySet(self.table, [r for r in self._results if match(r)])

    def exclude(self, **kwargs) -> "QuerySet":
        def match(item):
            return any(item.get(k) != v for k, v in kwargs.items())
        return QuerySet(self.table, [r for r in self._results if match(r)])

    def order_by(self, field: str) -> "QuerySet":
        desc = field.startswith("-")
        key = field[1:] if desc else field
        sorted_r = sorted(self._results, key=lambda x: (x.get(key) is None, x.get(key, 0)), reverse=desc)
        return QuerySet(self.table, sorted_r)

    def count(self) -> int:
        return len(self._results)

    def all(self) -> "QuerySet":
        return QuerySet(self.table, list(self._results))

    def __repr__(self) -> str:
        return f"<QuerySet [{len(self._results)} results]>"


class Manager:
    """Custom manager that can have custom methods."""
    def __init__(self, table: list[dict]):
        self.table = table

    def get_queryset(self) -> QuerySet:
        return QuerySet(self.table)

    def all(self) -> QuerySet:
        return self.get_queryset().all()

    def filter(self, **kwargs) -> QuerySet:
        return self.get_queryset().filter(**kwargs)


# --- Custom Manager ---
class PublishedManager(Manager):
    """Only returns published posts."""
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=True)

    def published_today(self) -> QuerySet:
        return self.get_queryset().filter(published_date="2024-07-07")


class FeaturedManager(Manager):
    """Manages featured posts."""
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def top_liked(self, min_likes: int = 10) -> QuerySet:
        return self.get_queryset().filter(likes__gte=min_likes)

    def by_author(self, author: str) -> QuerySet:
        return self.get_queryset().filter(author=author)


# --- Custom QuerySet Methods ---
class PostQuerySet(QuerySet):
    def published(self) -> "PostQuerySet":
        return PostQuerySet(self.table, [r for r in self._results if r.get("is_published")])

    def drafts(self) -> "PostQuerySet":
        return PostQuerySet(self.table, [r for r in self._results if not r.get("is_published")])

    def by_author(self, name: str) -> "PostQuerySet":
        return PostQuerySet(self.table, [r for r in self._results if r.get("author") == name])

    def popular(self, threshold: int = 5) -> "PostQuerySet":
        return PostQuerySet(self.table, [r for r in self._results if r.get("likes", 0) >= threshold])

    def search(self, term: str) -> "PostQuerySet":
        term_lower = term.lower()
        return PostQuerySet(
            self.table,
            [r for r in self._results if term_lower in r.get("title", "").lower() or term_lower in r.get("content", "").lower()]
        )


class PostManager(Manager):
    def get_queryset(self) -> PostQuerySet:
        return PostQuerySet(self.table)


# --- Data ---
POST_DATA = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "is_published": True, "published_date": "2024-07-01"},
    {"id": 2, "title": "Django Models", "author": "bob", "likes": 5, "is_published": True, "published_date": "2024-07-05"},
    {"id": 3, "title": "Advanced ORM Draft", "author": "alice", "likes": 8, "is_published": False, "published_date": None},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "is_published": True, "published_date": "2024-06-20"},
    {"id": 5, "title": "Django REST Framework", "author": "dave", "likes": 15, "is_published": True, "published_date": "2024-07-01"},
    {"id": 6, "title": "Testing in Django", "author": "alice", "likes": 7, "is_published": False, "published_date": None},
]

pub_manager = PublishedManager(POST_DATA)
featured_manager = FeaturedManager(POST_DATA)
post_manager = PostManager(POST_DATA)

print("=== PublishedManager (only published) ===")
print(f"  Published count: {pub_manager.all().count()}")
print(f"  All 'alice' via default: {pub_manager.filter(author='alice').count()}")

print("\n=== FeaturedManager (custom methods) ===")
top = featured_manager.top_liked(10)
print(f"  top_liked(10): {[(p['title'], p['likes']) for p in top._results]}")
alice_posts = featured_manager.by_author("alice")
print(f"  by_author('alice'): {[p['title'] for p in alice_posts._results]}")

print("\n=== PostQuerySet (chained methods) ===")
qs = post_manager.get_queryset()
published = qs.published()
print(f"  published: {[p['title'] for p in published._results]}")

popular_published = qs.published().popular()
print(f"  published().popular(): {[p['title'] for p in popular_published._results]}")

alice_popular = qs.by_author("alice").popular()
print(f"  by_author('alice').popular(): {[p['title'] for p in alice_popular._results]}")

drafts = qs.drafts()
print(f"  drafts: {[p['title'] for p in drafts._results]}")

searched = qs.search("django")
print(f"  search('django'): {[p['title'] for p in searched._results]}")

chained = qs.published().by_author("alice").popular(5)
print(f"  published.by_author('alice').popular(5): {[p['title'] for p in chained._results]}")
