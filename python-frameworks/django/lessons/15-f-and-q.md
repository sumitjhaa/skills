# 📘 Django Phase 02 — Lesson 05: F Expressions & Q Expressions

> 🎯 **Goal**: Write complex queries with `F()` for field references and `Q()` for OR/NOT logic.

## 📖 Concepts

### F Expressions — Reference Field Values
`F()` lets you **reference a field's value** in queries. DB evaluates, not Python.

```python
from django.db.models import F

# Compare two fields
Post.objects.filter(likes=F('views'))  # likes == views

# Update relative to current value
Post.objects.update(likes=F('likes') + 1)
```

**SQL generated**: `SET likes = likes + 1` (atomic, no race conditions)

### F() with Arithmetic
```python
F('likes') + 1
F('price') * F('quantity')
F('discount').bitand(2)  # bitwise operations
```

### Q Expressions — OR, NOT, AND
`Q()` objects encapsulate filter conditions. Combine with `|` (OR), `&` (AND), `~` (NOT).

```python
from django.db.models import Q

# OR
Post.objects.filter(Q(author='alice') | Q(author='bob'))

# AND + NOT
Post.objects.filter(Q(author='alice') & ~Q(draft=True))

# Complex: (author=alice AND published) OR (likes > 10)
Post.objects.filter(
    Q(author='alice', published=True) | Q(likes__gt=10)
)
```

### Q() in `exclude()`
```python
Post.objects.exclude(Q(author='alice') | Q(likes__lt=5))
```

### When to use Q?
- When you need **OR** (normal filter kwargs are AND)
- When you need **NOT** combined with complex logic
- When building dynamic queries (programmatic Q construction)

### ADHD-Friendly Summary
```
F('field')       → reference field value in query
F('likes') + 1   → atomic increment (no race condition)

Q(a=1) | Q(b=2)  → OR
Q(a=1) & Q(b=2)  → AND (or just filter kwargs)
~Q(a=1)          → NOT
```

## 🛠️ Code

```python
from django.db.models import F, Q

# F — field comparison
Post.objects.filter(likes=F('id'))

# F — atomic update
Post.objects.filter(draft=False).update(likes=F('likes') + 1)

# Q — OR
Post.objects.filter(Q(author='alice') | Q(author='bob'))

# Q — AND
Post.objects.filter(Q(author='alice') & Q(draft=True))

# Q — NOT
Post.objects.filter(~Q(author='alice'))

# Q — complex combinations
Post.objects.filter(
    (Q(author='alice') & Q(draft=False)) | Q(likes__gt=10)
)

# Q in exclude
Post.objects.exclude(Q(author='alice') | Q(likes__lt=5))
```

## 🧪 Practice

1. Find posts where likes > views (F expression)
2. Increment likes by 5 for all posts by "alice"
3. Find posts by "alice" OR posts with > 10 likes
4. Exclude posts that are drafts AND have < 3 likes

## 🧠 Key Takeaways

- `F()` delegates arithmetic to the **database**, not Python — prevents race conditions
- `Q()` is required for **OR** logic; filter kwargs are always AND
- Combine `Q()` with `|`, `&`, `~` for complex boolean logic
- `F()` works in `filter()`, `update()`, `annotate()`, `order_by()`
