"""Field lookups: exact, contains, gt, lt, gte, lte, in, range, startswith, isnull."""
from typing import Any


class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = list(results) if results is not None else list(table)

    def filter(self, **kwargs) -> "QuerySet":
        results = list(self._results)
        for key, value in kwargs.items():
            parts = key.split("__")
            if len(parts) == 1:
                results = [r for r in results if r.get(key) == value]
            else:
                field_name = parts[0]
                lookup = parts[1]
                filtered = []
                for r in results:
                    fval = r.get(field_name)
                    if lookup == "exact":
                        if fval == value:
                            filtered.append(r)
                    elif lookup == "contains":
                        if value.lower() in str(fval).lower():
                            filtered.append(r)
                    elif lookup == "icontains":
                        if value.lower() in str(fval).lower():
                            filtered.append(r)
                    elif lookup == "gt":
                        if fval is not None and fval > value:
                            filtered.append(r)
                    elif lookup == "gte":
                        if fval is not None and fval >= value:
                            filtered.append(r)
                    elif lookup == "lt":
                        if fval is not None and fval < value:
                            filtered.append(r)
                    elif lookup == "lte":
                        if fval is not None and fval <= value:
                            filtered.append(r)
                    elif lookup == "in":
                        if fval in value:
                            filtered.append(r)
                    elif lookup == "range":
                        if value[0] <= fval <= value[1]:
                            filtered.append(r)
                    elif lookup == "startswith":
                        if str(fval).startswith(value):
                            filtered.append(r)
                    elif lookup == "istartswith":
                        if str(fval).lower().startswith(value.lower()):
                            filtered.append(r)
                    elif lookup == "isnull":
                        if value and fval is None:
                            filtered.append(r)
                        elif not value and fval is not None:
                            filtered.append(r)
                    else:
                        filtered.append(r)
                results = filtered
        return QuerySet(self.table, results)

    def count(self) -> int:
        return len(self._results)


POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "created": "2024-01-15"},
    {"id": 2, "title": "Django Models Deep Dive", "author": "bob", "likes": 5, "created": "2024-03-20"},
    {"id": 3, "title": "Advanced ORM", "author": "alice", "likes": 8, "created": "2024-06-10"},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "created": "2024-02-01"},
    {"id": 5, "title": "django rest framework", "author": "dave", "likes": 15, "created": "2024-04-05"},
    {"id": 6, "title": "Testing in Django", "author": None, "likes": 0, "created": "2024-05-12"},
]

qs = QuerySet(POSTS)

print(f"exact (title='Hello Django'): {qs.filter(title__exact='Hello Django').count()}")
print(f"contains ('django'): {qs.filter(title__contains='django').count()}")
print(f"icontains ('django'): {qs.filter(title__icontains='django').count()}")
print(f"gt (likes > 10): {qs.filter(likes__gt=10).count()}")
print(f"gte (likes >= 8): {qs.filter(likes__gte=8).count()}")
print(f"lt (likes < 5): {qs.filter(likes__lt=5).count()}")
print(f"lte (likes <= 3): {qs.filter(likes__lte=3).count()}")
print(f"in (author in ['alice','bob']): {qs.filter(author__in=['alice','bob']).count()}")
print(f"range (likes 3-10): {qs.filter(likes__range=(3, 10)).count()}")
print(f"startswith ('Ad'): {qs.filter(title__startswith='Ad').count()}")
print(f"istartswith ('django'): {qs.filter(title__istartswith='django').count()}")
print(f"isnull (True): {qs.filter(author__isnull=True).count()}")
print(f"isnull (False): {qs.filter(author__isnull=False).count()}")
