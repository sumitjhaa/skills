"""QuerySet basics: all, filter, exclude, get, first, last."""
from typing import Optional


class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = list(results) if results is not None else list(table)

    def all(self) -> "QuerySet":
        return QuerySet(self.table, list(self.table))

    def filter(self, **kwargs) -> "QuerySet":
        def match(item: dict) -> bool:
            return all(item.get(k) == v for k, v in kwargs.items())
        return QuerySet(self.table, [r for r in self._results if match(r)])

    def exclude(self, **kwargs) -> "QuerySet":
        def match(item: dict) -> bool:
            return any(item.get(k) != v for k, v in kwargs.items())
        return QuerySet(self.table, [r for r in self._results if match(r)])

    def get(self, **kwargs) -> Optional[dict]:
        results = self.filter(**kwargs)._results
        if len(results) == 1:
            return results[0]
        if len(results) == 0:
            raise Exception("DoesNotExist")
        raise Exception("MultipleObjectsReturned")

    def first(self) -> Optional[dict]:
        return self._results[0] if self._results else None

    def last(self) -> Optional[dict]:
        return self._results[-1] if self._results else None

    def count(self) -> int:
        return len(self._results)

    def __repr__(self) -> str:
        return f"<QuerySet [{len(self._results)} results]>"


# --- Sample data ---
POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "published": True, "likes": 12},
    {"id": 2, "title": "Django Models", "author": "bob", "published": True, "likes": 5},
    {"id": 3, "title": "Django ORM", "author": "alice", "published": False, "likes": 8},
    {"id": 4, "title": "Python Tips", "author": "charlie", "published": True, "likes": 3},
]

qs = QuerySet(POSTS)

all_posts = qs.all()
print(f"all() → {all_posts.count()} posts")

published = qs.filter(published=True)
print(f"filter(published=True) → {published.count()} posts")

draft = qs.filter(published=False)
print(f"filter(published=False) → {draft.count()} posts")

alice_published = qs.filter(author="alice", published=True)
print(f"filter(author='alice', published=True) → {alice_published.count()} post(s)")

excluded = qs.exclude(author="alice")
print(f"exclude(author='alice') → {excluded.count()} posts")

try:
    post = qs.get(id=1)
    print(f"get(id=1) → '{post['title']}' by {post['author']}")
except Exception as e:
    print(f"get(id=1) → {e}")

try:
    qs.get(id=99)
except Exception as e:
    print(f"get(id=99) → {e}")

try:
    qs.get()  # returns multiple
except Exception as e:
    print(f"get() → {e}")

print(f"first() → '{qs.first()['title']}'")
print(f"last() → '{qs.last()['title']}'")
print(f"count() → {qs.count()}")
