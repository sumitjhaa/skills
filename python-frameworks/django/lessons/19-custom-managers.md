# 📘 Django Phase 02 — Lesson 09: Custom Managers & QuerySets

> 🎯 **Goal**: Encapsulate query logic in custom managers and custom QuerySets for reusable, chainable queries.

## 📖 Concepts

### Default Manager
Every model has `objects = models.Manager()`. You can replace or add managers.

### Why Custom Managers?
- Encapsulate common filters (e.g., `PublishedManager`)
- Expose business-specific methods (e.g., `manager.popular(10)`)
- Provide default-scoped QuerySets

### Simple Manager vs Custom QuerySet

**Simple Manager** — add methods to a manager class:
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

class Post(models.Model):
    published = PublishedManager()
```

**Custom QuerySet** — chainable methods on the QuerySet itself:
```python
class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def popular(self, threshold=10):
        return self.filter(likes__gte=threshold)

class Post(models.Model):
    objects = PostQuerySet.as_manager()
```

### Chaining with Custom QuerySet
```python
Post.objects.published().popular(5).by_author('alice')
```

### Manager vs QuerySet Pattern
| Pattern | Methods on | Return Type |
|---------|-----------|-------------|
| Manager-only | Manager | QuerySet |
| Custom QuerySet | QuerySet | QuerySet (chainable) |
| Manager + QuerySet | Both | Flexible |

### Best Practice: QuerySet.as_manager()
```python
class PostQuerySet(models.QuerySet):
    def published(self): ...
    def popular(self, n): ...

class Post(models.Model):
    objects = PostQuerySet.as_manager()
    # objects = Manager() + custom QuerySet in one
```

### ADHD-Friendly Summary
```
Custom Manager   → override get_queryset() for default scope
Custom QuerySet  → add methods → chainable: .published().popular()
.as_manager()    → combines both in one line

Keep queries in models, not views!
```

## 🛠️ Code

```python
class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def drafts(self):
        return self.filter(is_published=False)

    def popular(self, min_likes=10):
        return self.filter(likes__gte=min_likes)

    def by_author(self, name):
        return self.filter(author=name)

    def search(self, term):
        return self.filter(
            Q(title__icontains=term) | Q(content__icontains=term)
        )

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)

    objects = PostQuerySet.as_manager()

# Usage
Post.objects.published()                 # all published
Post.objects.popular(5)                  # 5+ likes
Post.objects.by_author('alice')          # by alice
Post.objects.published().popular()       # chained: published AND popular
Post.objects.published().search('django') # published AND matching
```

## 🧪 Practice

1. Create a `PublishedManager` that only returns published posts
2. Create a custom `PostQuerySet` with methods: `recent(days=7)`, `by_author()`, `popular(n)`
3. Register it on the `Post` model with `as_manager()`
4. Chain 3 methods: `Post.objects.published().popular(5).by_author('alice')`
5. Add a `FeaturedManager` that returns posts with `is_featured=True`

## 🧠 Key Takeaways

- Custom managers encapsulate query logic — don't repeat filters across views
- Custom QuerySets enable **chaining**: `.published().popular().by_author()`
- `QuerySet.as_manager()` creates a manager from a QuerySet class in one step
- Override `get_queryset()` to change the default scope
- Keep domain-specific query methods on the model, not scattered in views
