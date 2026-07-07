# 📘 Django Phase 05 — Lesson 03: Signals

> 🎯 **Goal**: Decouple code with Django signals — react to model saves, deletes, and custom events.

## 📖 Concepts

### What Are Signals?
A dispatcher system that allows decoupled applications to get notified when certain actions happen elsewhere.

### Built-in Model Signals

| Signal | Triggered By | Useful For |
|--------|-------------|------------|
| `pre_save` | `model.save()` called | Modify data before save |
| `post_save` | After `model.save()` | Create related objects, cache bust |
| `pre_delete` | `model.delete()` called | Cleanup related files |
| `post_delete` | After `model.delete()` | Cleanup cached data |
| `m2m_changed` | Many-to-many changed | Update counts |
| `request_started` / `request_finished` | HTTP request | Logging, timing |

### Signal Flow
```
model.save()
  → pre_save.send(sender=MyModel, instance=...)
    → [all connected receivers run]
  → actual DB save
  → post_save.send(sender=MyModel, instance=..., created=True)
    → [all connected receivers run]
```

### Connecting Receivers

```python
# Decorator (preferred)
@receiver(post_save, sender=Post)
def update_search_index(sender, instance, created, **kwargs):
    if created:
        SearchIndex.add(instance)

# Manual connect
post_save.connect(update_search_index, sender=Post)
```

### Custom Signals
```python
from django.dispatch import Signal

post_viewed = Signal()  # no providing_args needed in modern Django

# Send
post_viewed.send(sender=Post, post=post, user=request.user)

# Receive
@receiver(post_viewed)
def track_view(sender, post, user, **kwargs):
    ViewTracker.record(post, user)
```

### ADHD-Friendly Summary
```
@receiver(post_save, sender=Post) → run on save
Signal() → custom event
.send(sender=..., key=val) → fire event
**kwargs → always include in receivers
```

## 🛠️ Code

```python
# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal
from .models import Post, Comment

# Cache invalidation
@receiver(post_save, sender=Post)
def bust_post_cache(sender, instance, **kwargs):
    cache.delete('published_posts')

# Auto-create profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Custom signal
post_viewed = Signal()

@receiver(post_viewed)
def increment_view_count(sender, post, user, **kwargs):
    post.views += 1
    post.save(update_fields=['views'])
```

## 🧪 Practice

1. Connect `post_save` on `Post` to bust the post list cache
2. Create a custom `order_placed` signal with `order` and `user` params
3. Auto-create a `Profile` when a `User` is created
4. Connect `post_delete` on `Post` to delete associated images
5. Disconnect a receiver temporarily and verify it doesn't fire

## 🧠 Key Takeaways

- Signals decouple concerns — a post save doesn't need to know about search indexing
- Always include `**kwargs` in signal receivers (future-proof)
- `created=True` only on first save; subsequent saves have `created=False`
- Custom signals are great for cross-app communication
- Too many signals = hard to debug — use sparingly
