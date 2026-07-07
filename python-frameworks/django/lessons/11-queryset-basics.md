# 📘 Django Phase 02 — Lesson 01: QuerySet Basics

> 🎯 **Goal**: Understand Django's QuerySet API — `all()`, `filter()`, `exclude()`, `get()`, `first()`, `last()`, and `count()`.

## 📖 Concepts

### What is a QuerySet?
A **QuerySet** is Django's lazy, chainable abstraction over database rows. It translates Python method calls into SQL queries — but **only hits the DB when evaluated** (lazy evaluation).

```python
# QuerySets are lazy — no DB hit yet
qs = Post.objects.all()
qs = qs.filter(author='alice')

# DB hit happens here (evaluation)
posts = list(qs)
```

### Core Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `.all()` | All rows | `QuerySet` |
| `.filter(**kwargs)` | Matching rows | `QuerySet` |
| `.exclude(**kwargs)` | Non-matching rows | `QuerySet` |
| `.get(**kwargs)` | Single match | Model instance |
| `.first()` | First row or `None` | Model or `None` |
| `.last()` | Last row or `None` | Model or `None` |
| `.count()` | Row count | `int` |

### `get()` vs `filter()`
- `get()` raises `DoesNotExist` (0 matches) or `MultipleObjectsReturned` (2+ matches)
- `filter()` never raises — returns empty QuerySet for 0 matches

### Chaining
Methods return new `QuerySet` objects — chain indefinitely:

```python
Post.objects.filter(author='alice').exclude(title__startswith='Draft')
```

### Common Pitfalls
- ❌ `Post.objects.filter(author='alice').get(id=1)` — inefficient, use `get(author='alice', id=1)`
- ❌ Reusing evaluated QuerySets — each evaluation re-queries
- ✅ Use `.count()` instead of `len(qs)` for performance

### ADHD-Friendly Summary
```
QuerySet = lazy list of DB rows
         → chain: all() → filter() → exclude()
         → grab: get(), first(), last()
         → count: .count()
         → DB hits only on: list(), for, len(), bool(), repr()
```

## 🛠️ Code

```python
from code.queryset_basics import QuerySet

POSTS = [
    {"id": 1, "title": "Hello Django", "author": "alice",
     "published": True, "likes": 12},
    {"id": 2, "title": "Django Models", "author": "bob",
     "published": True, "likes": 5},
    {"id": 3, "title": "Django ORM", "author": "alice",
     "published": False, "likes": 8},
    {"id": 4, "title": "Python Tips", "author": "charlie",
     "published": True, "likes": 3},
]

qs = QuerySet(POSTS)

# all
all_posts = qs.all()  # all 4

# filter
published = qs.filter(published=True)  # 3

# exclude
without_alice = qs.exclude(author='alice')  # 2

# get (single match)
post = qs.get(id=1)  # {id: 1, title: 'Hello Django', ...}

# first / last
first = qs.first()  # id=1
last = qs.last()    # id=4

# count
n = qs.count()  # 4
```

## 🧪 Practice

Write a function that:
1. Creates a `Post` QuerySet
2. Filters to only published posts by "alice"
3. Excludes posts with likes < 5
4. Returns the count

## 🧠 Key Takeaways

- QuerySets are **lazy** — chain freely, DB hits only on evaluation
- `filter()` = AND conditions. Multiple kwargs = AND
- `get()` for **exactly one** result (raises otherwise)
- Always prefer `.count()` over `len(qs)` for performance
