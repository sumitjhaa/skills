"""Aggregation & Annotation: aggregate, annotate, Count, Sum, Avg, Max, Min."""
from typing import Any


class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = list(results) if results is not None else list(table)

    def filter(self, **kwargs) -> "QuerySet":
        def match(item: dict) -> bool:
            return all(item.get(k) == v for k, v in kwargs.items())
        return QuerySet(self.table, [r for r in self._results if match(r)])

    def aggregate(self, **kwargs) -> dict:
        result = {}
        for alias, expr in kwargs.items():
            agg_type = expr.get("type", "Count")
            field_name = expr["field"]
            values = [r.get(field_name, 0) for r in self._results if r.get(field_name) is not None]
            if not values:
                result[alias] = 0
                continue
            if agg_type == "Count":
                result[alias] = len(values)
            elif agg_type == "Sum":
                result[alias] = sum(values)
            elif agg_type == "Avg":
                result[alias] = round(sum(values) / len(values), 2)
            elif agg_type == "Max":
                result[alias] = max(values)
            elif agg_type == "Min":
                result[alias] = min(values)
        return result

    def annotate(self, **annotations) -> "QuerySet":
        annotated = []
        for r in self._results:
            row = dict(r)
            for alias, expr in annotations.items():
                expr_type = expr.get("type", "")
                field_name = expr["field"]
                try:
                    if expr_type == "upper":
                        row[alias] = str(row.get(field_name, "")).upper()
                    elif expr_type == "lower":
                        row[alias] = str(row.get(field_name, "")).lower()
                    elif expr_type == "word_count":
                        row[alias] = len(str(row.get(field_name, "")).split())
                except Exception:
                    row[alias] = 0
            annotated.append(row)
        return QuerySet(self.table, annotated)

    def count(self) -> int:
        return len(self._results)

    def values(self, *fields: str) -> list[dict]:
        if not fields:
            return list(self._results)
        return [{f: r.get(f) for f in fields} for r in self._results]


POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice", "likes": 12, "category": "web"},
    {"id": 2, "title": "Django Models", "author": "bob", "likes": 5, "category": "backend"},
    {"id": 3, "title": "Advanced ORM", "author": "alice", "likes": 8, "category": "backend"},
    {"id": 4, "title": "Python Tips", "author": "charlie", "likes": 3, "category": "python"},
    {"id": 5, "title": "Django REST Framework", "author": "dave", "likes": 15, "category": "api"},
    {"id": 6, "title": "Testing Django", "author": "alice", "likes": 7, "category": "testing"},
    {"id": 7, "title": "Django Forms", "author": "bob", "likes": 7, "category": "web"},
]

qs = QuerySet(POSTS)

print("--- aggregate ---")
total_likes = qs.aggregate(total=dict(type="Sum", field="likes"))
print(f"Sum(likes): {total_likes['total']}")

stats = qs.aggregate(
    avg_likes=dict(type="Avg", field="likes"),
    max_likes=dict(type="Max", field="likes"),
    min_likes=dict(type="Min", field="likes"),
    count=dict(type="Count", field="id"),
)
print(f"Avg(likes): {stats['avg_likes']}")
print(f"Max(likes): {stats['max_likes']}")
print(f"Min(likes): {stats['min_likes']}")
print(f"Count: {stats['count']}")

print("\n--- annotate ---")
annotated = qs.annotate(
    title_upper=dict(type="upper", field="title"),
    title_words=dict(type="word_count", field="title"),
)
for p in annotated._results[:3]:
    print(f"  '{p['title']}' → upper='{p['title_upper']}', words={p['title_words']}")

print("\n--- filtered aggregate ---")
alice_total = qs.filter(author="alice").aggregate(total=dict(type="Sum", field="likes"))
print(f"Sum(likes) where author='alice': {alice_total['total']}")
