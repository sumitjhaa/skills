# 📘 Django Phase 05 — Lesson 10: Integration — Production-Ready Blog

> 🎯 **Goal**: Combine all Phase 05 patterns — Celery, caching, signals, middleware, management commands, and storage — into a production-ready blog.

## 📖 Concepts

### What We're Building
A blog that's ready for production traffic:
- Cached post listings (Redis)
- Async email notifications (Celery)
- Image uploads with thumbnails (S3 + Pillow)
- Request timing + security middleware
- Dashboard with real-time stats
- Audit log via signals
- CLI commands for maintenance

### Architecture
```
Client                    Django                         Services
┌─────┐    request        ┌────────────────────┐    ┌──────────┐
│Browser├───┬─────────────┤ Middleware stack    │    │  Redis   │
└─────┘   │  │            │ ├─ SecurityHeaders  │    │ (cache)  │
          │  │            │ ├─ RequestTiming    │    └──────────┘
          │  │            │ ├─ AdminOnly        │    ┌──────────┐
          │  │            │ └─ ...              │    │ Celery   │
          │  │            ├────────────────────┤    │ (tasks)  │
          │  └────────────┤ Views              │    └──────────┘
          │               │ ├─ Cached post list│    ┌──────────┐
          │               │ ├─ Post detail      │    │   S3     │
          │               │ │  (signals)        │    │ (files)  │
          │               │ ├─ Image upload     │    └──────────┘
          │               │ └─ Dashboard        │    ┌──────────┐
          │               ├────────────────────┤    │PostgreSQL│
          │               │ Signals → audit,    │    └──────────┘
          │               │  cache bust, stats  │
          │               └────────────────────┘
```

### Key Integrations

| Feature | Technology | File |
|---------|-----------|------|
| Task queue | Celery + Redis | `tasks.py` |
| Caching | `@cache_page`, `cache.get/set` | `views.py`, `signals.py` |
| Signals | `post_save`, `post_viewed` | `signals.py` |
| Middleware | Custom timing + security | `middleware.py` |
| File storage | S3 + thumbnails | `models.py`, `storages.py` |
| Admin CLI | Management commands | `management/commands/` |
| Monitoring | django-debug-toolbar | `settings.py` |

### Performance Budget
```
Post list:    < 50ms  (cached)
Post detail:  < 100ms (cached + eager loaded)
Dashboard:    < 200ms (aggregated queries)
Image upload: < 500ms (async thumbnail via Celery)
```

### ADHD-Friendly Summary
```
Cache hot pages → Redis
Async heavy work → Celery
React to events → Signals
Protect globally → Middleware
Manage via CLI → Commands
Store to cloud → S3
```

## 🛠️ Code

```python
# Full integration snippet
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_notification

@cache_page(60 * 15)
def post_list(request):
    posts = Post.objects.select_related('author').all()
    return render(request, 'blog/list.html', {'posts': posts})

@receiver(post_save, sender=Post)
def on_post_save(sender, instance, created, **kwargs):
    cache.delete('post_list')
    if created:
        send_notification.delay('New post: {instance.title}')

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        import time
        start = time.time()
        response = self.get_response(request)
        response['X-Duration'] = f'{time.time() - start:.3f}s'
        return response
```

## 🧪 Practice

Build the complete production-ready blog:

1. **Caching**: Set up Redis, add `@cache_page` to list view, bust cache on post save
2. **Celery**: Create a `send_new_post_notification` task, call it from signal
3. **Signals**: Create `post_viewed` custom signal that increments a view counter
4. **Middleware**: Add timing middleware + admin IP whitelist
5. **Storage**: Configure S3 for uploaded images, generate thumbnails on save
6. **Commands**: Create a `publish_scheduled_posts` management command
7. **Testing**: Write factory-based tests for all views + mock Celery
8. **Performance**: Verify query count with debug-toolbar, fix any N+1
9. **Deploy**: Collect static, migrate, restart services

## 🧠 Key Takeaways

- Production readiness = caching + async + monitoring + security
- Caching is the biggest performance win for read-heavy apps
- Celery keeps the response fast by deferring slow work
- Signals decouple cross-cutting concerns
- Middleware protects and measures every request
- Management commands automate ops tasks
- Always profile before optimizing — measure, then fix
