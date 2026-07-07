# 📘 Django Phase 05 — Lesson 09: Performance Optimization

> 🎯 **Goal**: Identify and fix common Django performance issues — N+1 queries, missing indexes, connection pooling, profiling.

## 📖 Concepts

### The N+1 Query Problem
The most common Django perf issue:

```python
# BAD: N+1 queries
posts = Post.objects.all()
for post in posts:                    # 1 query
    print(post.author.name)           # N queries (one per post!)
    for comment in post.comments.all(): # N more queries!
        print(comment.text)

# GOOD: eager loading
posts = Post.objects.select_related('author').prefetch_related('comments')
for post in posts:                    # 1 query (JOIN)
    print(post.author.name)           # 0 queries — already loaded
    for comment in post.comments:     # 0 queries — already prefetched
        print(comment.text)
```

| Method | Loads | SQL |
|--------|-------|-----|
| `select_related('fk')` | FK/O2O | `LEFT JOIN` (single query) |
| `prefetch_related('m2m')` | M2M/reverse | Separate query + Python join |

### Database Indexes
```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['author', 'created_at']),
            models.Index(fields=['slug'], name='post_slug_idx'),
        ]
```

### Query Optimization Tips

| Pattern | Instead Of | Use |
|---------|-----------|-----|
| Count | `len(queryset)` | `queryset.count()` |
| Exists | `if queryset:` | `queryset.exists()` |
| Specific fields | `Post.objects.all()` | `Post.objects.only('title', 'id')` |
| Defer heavy fields | `Post.objects.all()` | `Post.objects.defer('content')` |
| Bulk create | Loop + save | `Post.objects.bulk_create([...])` |
| Bulk update | Loop + save | `Post.objects.bulk_update([...], ['field'])` |

### Connection Pooling
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'pool': True,  # or use pgBouncer/pgpool
        },
    }
}
```

### Profiling Tools

| Tool | What It Shows |
|------|--------------|
| `django-debug-toolbar` | SQL queries per page, timing |
| `django-extensions` + `RunProfile` | Code profiling |
| `nplusone` profiler | Detects N+1 in dev |
| `silk` | All requests, SQL, timing |

### ADHD-Friendly Summary
```
select_related('fk')  → JOIN (single query)
prefetch_related('m2m') → 2 queries total
db_index=True → faster WHERE/ORDER BY
.count() > len()  .exists() > if queryset:
django-debug-toolbar → see every query
```

## 🛠️ Code

```python
# views.py — optimized
from django.db import connection

def post_list(request):
    # Eager load author + comments
    posts = Post.objects.select_related('author').prefetch_related(
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    ).only('title', 'slug', 'author__username').all()

    # Count is separate optimized query
    total = Post.objects.count()

    return render(request, 'posts.html', {'posts': posts})

# Check query count
print(f"Queries: {len(connection.queries)}")

# Bulk operations
def publish_all_drafts():
    drafts = Post.objects.filter(is_published=False)
    count = drafts.update(is_published=True)  # single query!
    return count
```

## 🧪 Practice

1. Add `django-debug-toolbar` and observe query count on a page
2. Fix an N+1 by adding `select_related` — verify query count dropped
3. Add `db_index=True` to a frequently filtered field
4. Replace `len(queryset)` with `.count()` — measure the difference
5. Use `bulk_create` to insert 1000 posts vs loop — time both

## 🧠 Key Takeaways

- N+1 is the #1 Django perf issue — always eager-load relationships
- `select_related` for FK/O2O, `prefetch_related` for M2M/reverse
- `only()` and `defer()` reduce data transfer from DB
- Add `db_index=True` on fields used in `filter()`, `order_by()`, `distinct()`
- Profile before optimizing — don't guess where the bottleneck is
- Use `django-debug-toolbar` in development to catch issues early
