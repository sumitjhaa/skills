# 📘 Django Phase 02 — Lesson 02: Field Lookups

> 🎯 **Goal**: Master Django field lookups — the `__` suffix syntax for precise filtering.

## 📖 Concepts

### Lookup Syntax
Append `__lookupname` to a field name in `filter()`:

```python
Post.objects.filter(title__contains='Django')
Post.objects.filter(created__year=2024)
Post.objects.filter(likes__gte=10)
```

### Common Lookups

| Lookup | SQL Equivalent | Example |
|--------|---------------|---------|
| `exact` | `=` (default) | `title__exact='Django'` |
| `iexact` | `ILIKE` | `title__iexact='django'` |
| `contains` | `LIKE %val%` | `title__contains='Django'` |
| `icontains` | `ILIKE %val%` | `title__icontains='django'` |
| `in` | `IN (...)` | `id__in=[1,3,5]` |
| `gt` | `>` | `likes__gt=10` |
| `gte` | `>=` | `likes__gte=5` |
| `lt` | `<` | `likes__lt=3` |
| `lte` | `<=` | `likes__lte=10` |
| `startswith` | `LIKE val%` | `title__startswith='Django'` |
| `istartswith` | `ILIKE val%` | `title__istartswith='django'` |
| `endswith` | `LIKE %val` | `title__endswith='Guide'` |
| `iendswith` | `ILIKE %val` | `title__iendswith='guide'` |
| `range` | `BETWEEN` | `likes__range=(3, 10)` |
| `isnull` | `IS NULL` | `author__isnull=True` |

### Date Lookups
| Lookup | Example |
|--------|---------|
| `year` | `created__year=2024` |
| `month` | `created__month=1` |
| `day` | `created__day=15` |
| `week_day` | `created__week_day=1` (Sunday) |

### Negating Lookups
Use `exclude()` or Q objects (lesson 05):

```python
Post.objects.exclude(title__startswith='Draft')
```

### ADHD-Friendly Summary
```
field__lookup=value
            → contains, icontains, gt, lt, gte, lte
            → in=[list], range=(a,b), isnull=True
            → startswith, endswith (or i_ case-insensitive)
            → year, month, day (date fields)
```

## 🛠️ Code

```python
# exact (default)
Post.objects.filter(title='Hello Django')

# contains (case-sensitive)
Post.objects.filter(title__contains='django')  # only lowercase 'django'

# icontains (case-insensitive)
Post.objects.filter(title__icontains='django')  # matches 'Django', 'django', etc.

# comparison
Post.objects.filter(likes__gt=10)    # likes > 10
Post.objects.filter(likes__gte=8)    # likes >= 8
Post.objects.filter(likes__lt=5)     # likes < 5

# in
Post.objects.filter(author__in=['alice', 'bob'])

# range
Post.objects.filter(likes__range=(3, 10))  # 3 <= likes <= 10

# string patterns
Post.objects.filter(title__startswith='Ad')       # 'Advanced ORM'
Post.objects.filter(title__istartswith='django')  # 'Django...', 'django...'

# null checks
Post.objects.filter(author__isnull=True)   # author is None
Post.objects.filter(author__isnull=False)  # author is not None
```

## 🧪 Practice

Write queries for:
1. Posts with "Python" in the title (case-insensitive)
2. Posts created in February 2024
3. Posts with likes between 5 and 20
4. Posts where the author is NOT null AND likes > 0

## 🧠 Key Takeaways

- Lookups use `__` double underscore as separator
- Most lookups have `i` prefix for case-insensitive version
- `in`, `range`, and `isnull` take special value types (list, tuple, bool)
- Chain lookups: `filter(title__icontains='django', likes__gte=5)`
