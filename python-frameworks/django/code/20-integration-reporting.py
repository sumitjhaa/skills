"""Integration: Advanced Querying & Reporting System.

Pulls together: QuerySets, field lookups, aggregation, F/Q, relationships, custom managers.
"""
from dataclasses import dataclass, field
from typing import Any, Optional, Callable
from collections import defaultdict
from datetime import datetime


# ======================== Core ORM ========================

class F:
    def __init__(self, name: str):
        self.name = name


class Q:
    def __init__(self, **conditions):
        self.conditions = conditions
        self.connector = "AND"
        self.children: list["Q"] = []
        self.negated = False

    @staticmethod
    def _or(*children: "Q") -> "Q":
        q = Q()
        q.connector = "OR"
        q.children = list(children)
        return q

    @staticmethod
    def _and(*children: "Q") -> "Q":
        q = Q()
        q.connector = "AND"
        q.children = list(children)
        return q

    @staticmethod
    def _not(child: "Q") -> "Q":
        q = Q()
        q.negated = True
        q.children = [child]
        return q

    def _eval(self, item: dict) -> bool:
        if self.children:
            results = [c._eval(item) for c in self.children]
            r = all(results) if self.connector == "AND" else any(results)
            return not r if self.negated else r
        return all(item.get(k) == v for k, v in self.conditions.items())


class QuerySet:
    def __init__(self, table: list[dict], results: list[dict] = None):
        self.table = table
        self._results = results or list(table)

    def filter(self, *args, **kwargs) -> "QuerySet":
        results = list(self._results)
        if args and isinstance(args[0], Q):
            results = [r for r in results if args[0]._eval(r)]
        for k in list(kwargs.keys()):
            v = kwargs[k]
            if isinstance(v, F):
                results = [r for r in results if r.get(k) == r.get(v.name)]
            elif isinstance(v, (list, tuple)):
                results = [r for r in results if r.get(k) in v]
            else:
                results = [r for r in results if r.get(k) == v]
        return QuerySet(self.table, results)

    def exclude(self, *args, **kwargs) -> "QuerySet":
        results = list(self._results)
        if args and isinstance(args[0], Q):
            results = [r for r in results if not args[0]._eval(r)]
        for k, v in kwargs.items():
            results = [r for r in results if r.get(k) != v]
        return QuerySet(self.table, results)

    def order_by(self, *fields: str) -> "QuerySet":
        def sort_key(item):
            keys = []
            for f in fields:
                desc = f.startswith("-")
                fn = f[1:] if desc else f
                val = item.get(fn, 0)
                if val is None:
                    val = 0
                keys.append(-val if desc else val)
            return tuple(keys)
        return QuerySet(self.table, sorted(self._results, key=sort_key))

    def annotate(self, **annotations) -> "QuerySet":
        annotated = []
        for r in self._results:
            row = dict(r)
            for alias, expr in annotations.items():
                if expr["type"] == "upper":
                    row[alias] = str(row.get(expr["field"], "")).upper()
                elif expr["type"] == "lower":
                    row[alias] = str(row.get(expr["field"], "")).lower()
            annotated.append(row)
        return QuerySet(self.table, annotated)

    def aggregate(self, **kwargs) -> dict:
        result = {}
        for alias, expr in kwargs.items():
            vals = [r.get(expr["field"], 0) for r in self._results if r.get(expr["field"]) is not None]
            if not vals:
                result[alias] = 0
                continue
            t = expr.get("type", "Count")
            if t == "Count":
                result[alias] = len(vals)
            elif t == "Sum":
                result[alias] = sum(vals)
            elif t == "Avg":
                result[alias] = round(sum(vals) / len(vals), 2)
            elif t == "Max":
                result[alias] = max(vals)
            elif t == "Min":
                result[alias] = min(vals)
        return result

    def values(self, *fields: str) -> list[dict]:
        if not fields:
            return list(self._results)
        return [{f: r.get(f) for f in fields} for r in self._results]

    def count(self) -> int:
        return len(self._results)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return QuerySet(self.table, self._results[index])
        return self._results[index]

    def __repr__(self) -> str:
        return f"<QuerySet [{len(self._results)} results]>"


class Manager:
    def __init__(self, table: list[dict]):
        self.table = table

    def get_queryset(self) -> QuerySet:
        return QuerySet(self.table)

    def all(self) -> QuerySet:
        return QuerySet(self.table)

    def filter(self, **kwargs) -> QuerySet:
        return self.get_queryset().filter(**kwargs)


class PublishedManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=True)

    def all(self) -> QuerySet:
        return self.get_queryset()


class ReportManager(Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def summary_by_author(self) -> list[dict]:
        authors = defaultdict(lambda: {"total_posts": 0, "total_likes": 0, "avg_likes": 0.0, "posts": []})
        for p in self.table:
            a = p.get("author", "unknown")
            authors[a]["total_posts"] += 1
            authors[a]["total_likes"] += p.get("likes", 0)
            authors[a]["posts"].append(p["title"])
        for a in authors:
            t = authors[a]["total_posts"]
            authors[a]["avg_likes"] = round(authors[a]["total_likes"] / t, 2) if t else 0
        return [{"author": k, **v} for k, v in sorted(authors.items())]

    def monthly_report(self, year: int) -> dict:
        monthly = defaultdict(lambda: {"count": 0, "likes": 0})
        for p in self.table:
            date_str = p.get("published_date", "")
            if date_str and date_str.startswith(str(year)):
                month = date_str[5:7]
                monthly[month]["count"] += 1
                monthly[month]["likes"] += p.get("likes", 0)
        return dict(sorted(monthly.items()))


# ======================== Sample Data ========================

AUTHORS = [
    {"id": 1, "name": "Alice", "role": "editor"},
    {"id": 2, "name": "Bob", "role": "writer"},
    {"id": 3, "name": "Charlie", "role": "writer"},
    {"id": 4, "name": "Diana", "role": "admin"},
]

POSTS = [
    {"id": 1, "title": "Hello Django", "slug": "hello-django", "author_id": 1, "author": "Alice", "likes": 12, "views": 340, "is_published": True, "published_date": "2024-01-15", "category": "web"},
    {"id": 2, "title": "Django Models Deep Dive", "slug": "django-models", "author_id": 2, "author": "Bob", "likes": 5, "views": 120, "is_published": True, "published_date": "2024-03-20", "category": "backend"},
    {"id": 3, "title": "Advanced ORM Techniques", "slug": "advanced-orm", "author_id": 1, "author": "Alice", "likes": 8, "views": 210, "is_published": True, "published_date": "2024-06-10", "category": "backend"},
    {"id": 4, "title": "Python Tips & Tricks", "slug": "python-tips", "author_id": 3, "author": "Charlie", "likes": 3, "views": 95, "is_published": True, "published_date": "2024-02-01", "category": "python"},
    {"id": 5, "title": "Django REST Framework Guide", "slug": "django-rest", "author_id": 4, "author": "Diana", "likes": 15, "views": 520, "is_published": True, "published_date": "2024-04-05", "category": "api"},
    {"id": 6, "title": "Testing Django Applications", "slug": "testing-django", "author_id": 1, "author": "Alice", "likes": 7, "views": 180, "is_published": False, "published_date": None, "category": "testing"},
    {"id": 7, "title": "Django Forms Handbook", "slug": "django-forms", "author_id": 2, "author": "Bob", "likes": 9, "views": 275, "is_published": True, "published_date": "2024-05-18", "category": "web"},
    {"id": 8, "title": "Docker for Django", "slug": "docker-django", "author_id": 4, "author": "Diana", "likes": 11, "views": 400, "is_published": True, "published_date": "2024-07-01", "category": "devops"},
    {"id": 9, "title": "Draft: New Features", "slug": "new-features", "author_id": 3, "author": "Charlie", "likes": 2, "views": 45, "is_published": False, "published_date": None, "category": "draft"},
]

COMMENTS = [
    {"id": 1, "post_id": 1, "author": "Bob", "text": "Great introduction!", "created": "2024-01-16"},
    {"id": 2, "post_id": 1, "author": "Charlie", "text": "Very helpful", "created": "2024-01-17"},
    {"id": 3, "post_id": 2, "author": "Alice", "text": "Nice explanation", "created": "2024-03-21"},
    {"id": 4, "post_id": 5, "author": "Alice", "text": "This is gold!", "created": "2024-04-06"},
    {"id": 5, "post_id": 5, "author": "Bob", "text": "Bookmarked", "created": "2024-04-07"},
    {"id": 6, "post_id": 5, "author": "Charlie", "text": "Thanks!", "created": "2024-04-08"},
    {"id": 7, "post_id": 7, "author": "Alice", "text": "Well written", "created": "2024-05-19"},
    {"id": 8, "post_id": 8, "author": "Bob", "text": "This saved me hours", "created": "2024-07-02"},
]

published = PublishedManager(POSTS)
report = ReportManager(POSTS)
qs = QuerySet(POSTS)


# ======================== REPORTS ========================

print("=" * 60)
print("📊 DASHBOARD REPORT")
print("=" * 60)

print("\n--- 1. Published Post Count ---")
print(f"  Published: {published.all().count()}")
print(f"  Drafts:    {qs.filter(is_published=False).count()}")

print("\n--- 2. Top Posts (by likes, published only) ---")
top_published = published.all().order_by("-likes")[:5]
for p in top_published._results:
    print(f"  ❤ {p['likes']:3d}  👁 {p['views']:3d}  {p['title']}  ({p['author']})")

print("\n--- 3. Author Summary ---")
for entry in report.summary_by_author():
    print(f"  {entry['author']:8s}: {entry['total_posts']} posts, {entry['total_likes']} likes, avg {entry['avg_likes']:.1f}/post")

print("\n--- 4. Monthly Activity (2024) ---")
for month, data in report.monthly_report(2024).items():
    print(f"  {month}: {data['count']} posts, {data['likes']} likes")

print("\n--- 5. Engagement Ratio (likes/views for posts > 5 likes) ---")
engaged = published.all().filter(likes__gte=5)
for p in engaged._results:
    ratio = round(p['likes'] / p['views'] * 100, 2) if p['views'] > 0 else 0
    bar = "█" * int(ratio / 2)
    print(f"  {ratio:5.1f}% {bar} {p['title']}")

print("\n--- 6. Comments per Post (top 3) ---")
post_comments = defaultdict(int)
for c in COMMENTS:
    post_comments[c["post_id"]] += 1
for post_id in sorted(post_comments, key=post_comments.get, reverse=True)[:3]:
    post = next(p for p in POSTS if p["id"] == post_id)
    print(f"  💬 {post_comments[post_id]} comments  — {post['title']}")

print("\n--- 7. Category Breakdown ---")
categories = defaultdict(lambda: {"posts": 0, "likes": 0, "views": 0})
for p in POSTS:
    cat = p["category"]
    categories[cat]["posts"] += 1
    categories[cat]["likes"] += p["likes"]
    categories[cat]["views"] += p["views"]
for cat, data in sorted(categories.items()):
    print(f"  {cat:8s}: {data['posts']} posts, {data['likes']} likes, {data['views']} views")

print("\n--- 8. Popular Drafts (unpublished with >5 likes — Q expression) ---")
popular_drafts = qs.filter(Q._and(Q(is_published=False), Q(likes__gt=5)))
for p in popular_drafts._results:
    print(f"  ⚠  {p['title']}  ({p['likes']} likes) — consider publishing!")

print("\n--- 9. Author Role: Editors vs Writers ---")
author_map = {a["name"]: a["role"] for a in AUTHORS}
editors = published.all().filter(author=[n for n, r in author_map.items() if r == "editor"])
writers = published.all().filter(author=[n for n, r in author_map.items() if r == "writer"])
print(f"  Editors: {editors.count()} posts")
print(f"  Writers: {writers.count()} posts")

print("\n--- 10. Annotated Titles ---")
annotated = published.all().annotate(title_upper=dict(type="upper", field="title"))[:3]
for p in annotated._results:
    print(f"  {p['title']:30s} → {p['title_upper']}")

print("\n✅ Report complete.")
