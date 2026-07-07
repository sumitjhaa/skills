"""QuerySet methods: order_by, distinct, values, values_list, dates, reverse."""
from typing import Any, Optional


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

    def order_by(self, *fields: str) -> "QuerySet":
        def sort_key(item: dict) -> tuple:
            keys = []
            for f in fields:
                desc = f.startswith("-")
                fn = f[1:] if desc else f
                val = item.get(fn, 0)
                if val is None:
                    val = 0
                keys.append(-val if desc else val)
            return tuple(keys)
        sorted_results = sorted(self._results, key=sort_key)
        return QuerySet(self.table, sorted_results)

    def reverse(self) -> "QuerySet":
        return QuerySet(self.table, list(reversed(self._results)))

    def distinct(self, *fields: str) -> "QuerySet":
        if not fields:
            seen = []
            uniq = []
            for r in self._results:
                if r not in seen:
                    seen.append(r)
                    uniq.append(r)
            return QuerySet(self.table, uniq)
        seen = set()
        uniq = []
        for r in self._results:
            key = tuple(r.get(f) for f in fields)
            if key not in seen:
                seen.add(key)
                uniq.append(r)
        return QuerySet(self.table, uniq)

    def values(self, *fields: str) -> list[dict]:
        if not fields:
            return list(self._results)
        return [{f: r.get(f) for f in fields} for r in self._results]

    def values_list(self, *fields: str, flat: bool = False) -> list:
        if flat and len(fields) == 1:
            return [r.get(fields[0]) for r in self._results]
        return [tuple(r.get(f) for f in fields) for r in self._results]

    def dates(self, field_name: str, kind: str = "year") -> list:
        seen = set()
        result = []
        for r in self._results:
            val = r.get(field_name, "")
            if kind == "year":
                key = val[:4]
            elif kind == "month":
                key = val[:7]
            elif kind == "day":
                key = val[:10]
            if key and key not in seen:
                seen.add(key)
                result.append(key)
        return sorted(result)

    def count(self) -> int:
        return len(self._results)

    def __repr__(self) -> str:
        return f"<QuerySet [{len(self._results)} results]>"


POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "created": "2024-01-15"},
    {"id": 2, "title": "Django Models", "author": "bob", "likes": 5, "created": "2024-03-20"},
    {"id": 3, "title": "Advanced ORM", "author": "alice", "likes": 8, "created": "2024-06-10"},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "created": "2024-02-01"},
    {"id": 5, "title": "Django REST", "author": "dave", "likes": 15, "created": "2024-04-05"},
    {"id": 6, "title": "Hello Django", "author": "alice", "likes": 12, "created": "2024-05-12"},
    {"id": 7, "title": "Django Forms", "author": "bob", "likes": 7, "created": "2024-07-01"},
]

qs = QuerySet(POSTS)

print("--- order_by ---")
by_likes = qs.order_by("likes")
print(f"order_by('likes'): {[p['likes'] for p in by_likes._results]}")

by_likes_desc = qs.order_by("-likes")
print(f"order_by('-likes'): {[p['likes'] for p in by_likes_desc._results]}")

multi = qs.order_by("author", "-likes")
print(f"order_by('author', '-likes'): {[(p['author'], p['likes']) for p in multi._results]}")

print("\n--- distinct ---")
print(f"distinct(): {qs.distinct().count()} (vs {qs.count()} total)")
print(f"distinct('author'): {qs.distinct('author').count()} unique authors")

print("\n--- values ---")
titles = qs.values("title", "likes")
print(f"values('title','likes'): {titles[:3]}...")

print("\n--- values_list ---")
id_titles = qs.values_list("id", "title")
print(f"values_list('id','title'): {id_titles[:3]}...")

flat = qs.values_list("title", flat=True)
print(f"values_list('title', flat=True): {flat[:3]}...")

print("\n--- dates ---")
months = qs.dates("created", "month")
print(f"dates('created','month'): {months}")

print("\n--- reverse ---")
rev = qs.reverse()
print(f"first → '{rev._results[0]['title']}' (was '{qs._results[0]['title']}')")
