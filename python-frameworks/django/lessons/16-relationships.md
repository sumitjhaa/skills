# 📘 Django Phase 02 — Lesson 06: Relationships & Related Queries

> 🎯 **Goal**: Query across models with forward/reverse relations, `select_related`, and `prefetch_related`.

## 📖 Concepts

### Forward vs Reverse
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
```

- **Forward**: `post.author` — Post → Author (read the FK target)
- **Reverse**: `author.post_set.all()` — Author → Posts (related manager)

### `select_related()` — SQL JOIN (FK + OneToOne)
Fetches related objects in the **same query**. Use for ForeignKey and OneToOneField.

```python
# Without: N+1 queries
posts = Post.objects.all()
for p in posts:
    print(p.author.name)  # 1 query per post!

# With: 1 query (JOIN)
posts = Post.objects.select_related('author').all()
for p in posts:
    print(p.author.name)  # no extra queries
```

### `prefetch_related()` — Python JOIN (ManyToMany + Reverse FK)
Fetches in **separate queries**, then joins in Python. Use for ManyToMany and reverse ForeignKey.

```python
# Without: N+1 queries
authors = Author.objects.all()
for a in authors:
    print(a.post_set.all())  # 1 query per author!

# With: 2 queries total
authors = Author.objects.prefetch_related('post_set').all()
for a in authors:
    print(a.post_set.all())  # cached
```

### When to Use Which
| Relationship | Use |
|--------------|-----|
| ForeignKey (forward) | `select_related` |
| OneToOneField | `select_related` |
| ManyToManyField (forward) | `prefetch_related` |
| Reverse ForeignKey | `prefetch_related` |
| GenericRelation | `prefetch_related` |

### Chaining
```python
Post.objects.select_related('author').prefetch_related('comments')
```

### ADHD-Friendly Summary
```
select_related('fk')    → 1 query, JOIN (FK, OneToOne)
prefetch_related('rev') → 2 queries, batch (M2M, reverse FK)

Always prefetch in bulk: fetch once, use many
Avoid N+1 queries!
```

## 🛠️ Code

```python
# Forward: Post → Author (ForeignKey)
post.author              # hits DB if not cached
post.author.name         # lazy load

# Reverse: Author → Posts (implicit related_name='post_set')
author.post_set.all()    # hits DB if not cached

# select_related — 1 query with JOIN
Post.objects.select_related('author').all()

# prefetch_related — 2 batch queries
Author.objects.prefetch_related('post_set').all()

# Chained
Post.objects.select_related('author').prefetch_related('comment_set')
```

## 🧪 Practice

Models: `Category` → `Post` → `Comment`

1. Fetch all posts with their author (use select_related)
2. Fetch all authors with their posts (use prefetch_related)
3. Fetch all posts with author AND comments (chain both)
4. Count how many queries would run without prefetch vs with prefetch for 10 posts with 3 comments each

## 🧠 Key Takeaways

- `select_related` = SQL JOIN (one query, good for FK/OneToOne)
- `prefetch_related` = separate batch query + Python merge (good for M2M/reverse)
- **N+1 problem**: without eager loading, each related access hits DB once
- Always prefetch in the **view**, before template rendering
- Use `Prefetch()` object for advanced filtering on prefetched relations
