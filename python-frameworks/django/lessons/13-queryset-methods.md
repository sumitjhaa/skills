# 📘 Django Phase 02 — Lesson 03: QuerySet Methods

> 🎯 **Goal**: Master ordering, deduplication, field selection, and date extraction methods.

## 📖 Concepts

### `order_by(*fields)`
Sort by field name. Prefix with `-` for descending.

```python
Post.objects.order_by('title')        # ascending
Post.objects.order_by('-created')     # descending (newest first)
Post.objects.order_by('author', '-likes')  # multi-field
```

⚠️ **Meta.ordering**: sets a default order on the model. You can override with `order_by()`.

### `reverse()`
Reverse the current ordering. Only works if there's a default `ordering` or you've called `order_by()`.

### `distinct(*fields)`
Remove duplicate rows. With `*fields`, unique on those columns.

```python
Post.objects.distinct()                # fully unique rows
Post.objects.distinct('author')        # unique authors
```

⚠️ PostgreSQL only supports `distinct(*fields)`. Other DBs support only `distinct()`.

### `values(*fields)`
Return `list[dict]` instead of model instances. Reduces memory.

```python
Post.objects.values('id', 'title')
# → [{'id': 1, 'title': 'Hello Django'}, ...]
```

### `values_list(*fields, flat=False)`
Return lists or tuples. `flat=True` returns single values.

```python
Post.objects.values_list('id', 'title')
# → [(1, 'Hello Django'), ...]

Post.objects.values_list('title', flat=True)
# → ['Hello Django', 'Django Models', ...]
```

### `dates(field, kind)`
Extract distinct dates by `kind='year'`, `'month'`, or `'day'`.

```python
Post.objects.dates('created', 'month')
# → [datetime.date(2024, 1, 1), datetime.date(2024, 2, 1), ...]
```

### Performance Rule of Thumb
```
Model instances  → most convenient, heaviest
values()         → lighter (dicts)
values_list()    → lightest (tuples)
```

### ADHD-Friendly Summary
```
order_by('field') / order_by('-field')
distinct() / distinct('field')
values('a','b')        → [{...}]
values_list('a','b')   → [(...)]
values_list('a',flat=True) → [...]
dates('field','month') → unique dates
```

## 🛠️ Code

```python
# order_by
Post.objects.order_by('likes')                    # ascending
Post.objects.order_by('-likes')                   # descending
Post.objects.order_by('author', '-likes')         # multi-field

# reverse
Post.objects.order_by('id').reverse()             # reversed order

# distinct
Post.objects.distinct()                           # unique rows
Post.objects.distinct('author')                   # unique authors

# values (list of dicts)
Post.objects.values('id', 'title')

# values_list (list of tuples or flat list)
Post.objects.values_list('id', 'title')
Post.objects.values_list('title', flat=True)

# dates
Post.objects.dates('created', 'month')            # unique months
Post.objects.dates('created', 'year')             # unique years
```

## 🧪 Practice

1. Get the 5 most liked posts (title and likes only)
2. Get unique authors who have published posts
3. Get the creation months for all posts in 2024
4. Get all post titles as a flat list, ordered by title

## 🧠 Key Takeaways

- `order_by('-field')` for descending; chain multiple fields
- `values()` and `values_list()` reduce DB-to-Python overhead
- `flat=True` works only with a single field in `values_list`
- `dates()` is a distinct-date convenience for time-series data
- **Lazy**: nothing above hits DB until you iterate, count, or slice
