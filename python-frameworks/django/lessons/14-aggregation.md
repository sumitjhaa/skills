# 📘 Django Phase 02 — Lesson 04: Aggregation & Annotation

> 🎯 **Goal**: Compute summary statistics with `aggregate()` and add computed columns with `annotate()`.

## 📖 Concepts

### `aggregate()` — Over Entire QuerySet
Returns a `dict` with computed values. Uses **aggregate functions** from `django.db.models`:

```python
from django.db.models import Count, Sum, Avg, Max, Min

stats = Post.objects.aggregate(
    total=Count('id'),
    avg_likes=Avg('likes'),
    max_likes=Max('likes'),
)
# → {'total': 7, 'avg_likes': 8.14, 'max_likes': 15}
```

### Common Aggregates

| Function | Purpose |
|----------|---------|
| `Count('field')` | Number of non-null values |
| `Count('field', distinct=True)` | Unique count |
| `Sum('field')` | Total |
| `Avg('field')` | Average |
| `Max('field')` | Maximum |
| `Min('field')` | Minimum |

### `annotate()` — Per-Row Computed Fields
Adds a virtual field to **each row** in the QuerySet:

```python
from django.db.models import Count

posts = Post.objects.annotate(comment_count=Count('comments'))
for p in posts:
    print(p.title, p.comment_count)
```

### Filtering Before Aggregation
```python
Post.objects.filter(author='alice').aggregate(Sum('likes'))
```

### Filtering on Annotations
```python
from django.db.models import Count, Q

Post.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count__gt=5)
```

### `values()` + `annotate()` — Group By
```python
Post.objects.values('author').annotate(
    total_likes=Sum('likes')
).order_by('-total_likes')
```

### ADHD-Friendly Summary
```
aggregate() → one row of stats        [Count, Sum, Avg, Max, Min]
annotate()  → one computed column per row [comment_count=Count(...)]
values() + annotate() → GROUP BY equivalent
```

## 🛠️ Code

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Basic aggregation
stats = Post.objects.aggregate(
    total=Count('id'),
    total_likes=Sum('likes'),
    avg_likes=Avg('likes'),
    max_likes=Max('likes'),
    min_likes=Min('likes'),
)

# Annotation
posts = Post.objects.annotate(
    title_upper=Upper('title'),
    word_count=Count('title'),
)

# Filtered aggregation
alice_stats = Post.objects.filter(
    author='alice'
).aggregate(total=Sum('likes'))

# values + annotate (GROUP BY)
by_author = Post.objects.values('author').annotate(
    total=Sum('likes')
).order_by('-total')
```

## 🧪 Practice

1. Get total, average, max, and min likes for published posts
2. Annotate each post with its comment count
3. Find the author with the most total likes
4. Get the number of posts per category

## 🧠 Key Takeaways

- `aggregate()` collapses QuerySet → single dict of stats
- `annotate()` adds columns to each row
- Combine with `values()` for GROUP BY behavior
- Aggregate functions live in `django.db.models`
- Use `filter()` before aggregate/annotate for pre-filtering
