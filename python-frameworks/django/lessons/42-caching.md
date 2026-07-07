# 📘 Django Phase 05 — Lesson 02: Caching Strategies

> 🎯 **Goal**: Speed up your app with per-view, template fragment, and low-level caching.

## 📖 Concepts

### Cache Backends

| Backend | Best For | Storage |
|---------|----------|---------|
| `Memcached` | Production | Distributed memory |
| `Redis` | Production + sessions | In-memory with persistence |
| `DatabaseCache` | Small sites | Database table |
| `FileBasedCache` | Dev | Filesystem |
| `LocalMemoryCache` | Dev (default) | Process memory |
| `DummyCache` | Testing | No-op |

### Cache Strategies

| Strategy | How | When |
|----------|-----|------|
| Per-view cache | `@cache_page(60)` | Entire page is static |
| Template fragment | `{% cache 60 sidebar %}` | Part of page changes |
| Low-level cache | `cache.get()` / `cache.set()` | API responses, DB results |
| Per-site cache | `UpdateCacheMiddleware` | Full-site caching |

### Cache Key Structure
```
views.decorators.cache.cache_page
  → key_prefix:path:query_string:accept-language:...
  → e.g.: "cache_page:GET:/posts/:en"
```

### Cache Invalidation
```python
# Delete specific key
cache.delete('trending_posts')

# Bust all (if using Redis)
from django.core.cache import cache
cache.clear()

# Versioned keys (auto-bust on increment)
cache.set('my_key', value, version=2)  # key becomes my_key:2
```

### ADHD-Friendly Summary
```
@cache_page(60)       → cache entire view for 60s
{% cache 300 sidebar %} → cache template fragment
cache.set(key, val, timeout) → low-level API
cache.get(key) → retrieve
```

## 🛠️ Code

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
CACHE_MIDDLEWARE_SECONDS = 600  # default TTL

# views.py
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 15)  # 15 minutes
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})

# Low-level caching
def get_trending_posts():
    posts = cache.get('trending_posts')
    if posts is None:
        posts = Post.objects.filter(likes__gt=10)[:10]
        cache.set('trending_posts', posts, 300)
    return posts
```

## 🧪 Practice

1. Set up Redis as the cache backend
2. Add `@cache_page(300)` to a slow view — verify speedup
3. Use `{% cache 600 sidebar %}` in a template
4. Implement `cache.get_or_set()` for a DB query
5. Bust the cache after creating a new post (via signal)

## 🧠 Key Takeaways

- Cache aggressively in production — it's the cheapest perf win
- Per-view caching is easiest; fragment caching is more precise
- Always set a timeout — don't cache forever
- Invalidate on writes (create/update/delete) via signals
- Use Redis in production; local memory or file for dev
