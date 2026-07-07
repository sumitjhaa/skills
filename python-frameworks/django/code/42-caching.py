"""Caching strategies: per-view, template fragments, low-level cache API."""
from typing import Any, Optional, Callable
from functools import wraps
import time
import hashlib


# ======================== Cache Backend Simulation ========================
CACHE_STORE: dict[str, tuple[Any, float]] = {}  # key -> (value, expiry)

class Cache:
    """Simulates Django's cache framework."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}" if self.prefix else key

    def get(self, key: str, default: Any = None) -> Any:
        full_key = self._key(key)
        if full_key in CACHE_STORE:
            value, expiry = CACHE_STORE[full_key]
            if expiry is None or time.time() < expiry:
                return value
            del CACHE_STORE[full_key]
        return default

    def set(self, key: str, value: Any, timeout: int = 300):
        full_key = self._key(key)
        expiry = time.time() + timeout if timeout else None
        CACHE_STORE[full_key] = (value, expiry)

    def delete(self, key: str):
        full_key = self._key(key)
        CACHE_STORE.pop(full_key, None)

    def get_or_set(self, key: str, get_value: Callable, timeout: int = 300) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = get_value()
        self.set(key, value, timeout)
        return value

    def clear(self):
        CACHE_STORE.clear()


cache = Cache()


# ======================== Per-View Cache Simulation ========================

def cache_page(timeout: int = 300):
    """Simulates @cache_page decorator — caches the entire response."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Build unique cache key from request path + query params
            path = request.get("path", "/") + str(request.get("query", ""))
            cache_key = f"view:{hashlib.md5(path.encode()).hexdigest()}"
            cached = cache.get(cache_key)
            if cached is not None:
                return {"from_cache": True, "data": cached}
            response = view_func(request, *args, **kwargs)
            cache.set(cache_key, response, timeout)
            return {"from_cache": False, "data": response}
        return wrapper
    return decorator


# ======================== Low-Level Cache Demos ========================

def expensive_query(query_name: str) -> list[dict]:
    """Simulate an expensive DB query."""
    time.sleep(0.5)  # Simulate 500ms query
    return [
        {"id": 1, "title": f"Result from {query_name}", "value": 100},
        {"id": 2, "title": f"Another {query_name} result", "value": 200},
    ]


def cached_expensive_query(query_name: str) -> list[dict]:
    """Same query but cached."""
    return cache.get_or_set(
        f"query:{query_name}",
        lambda: expensive_query(query_name),
        timeout=60,
    )


# ======================== Template Fragment Caching Sim ========================
class TemplateFragmentCache:
    """Simulates {% cache %} template tag for fragment caching."""
    def __init__(self):
        self.cache = Cache(prefix="fragment")

    def render_cached(self, fragment_name: str, content_fn: Callable, timeout: int = 300) -> str:
        return self.cache.get_or_set(fragment_name, content_fn, timeout)


fragment_cache = TemplateFragmentCache()


# ======================== Demo ========================
print("=== Caching Demo ===\n")

# --- Per-view cache ---
@cache_page(timeout=10)
def post_list_view(request):
    time.sleep(0.3)  # Simulate view processing
    return {"posts": [{"id": 1, "title": "Hello"}], "count": 1}

print("1. Per-view cache:")
req = {"path": "/posts/", "query": ""}
resp1 = post_list_view(req)
print(f"   First call (cold):  from_cache={resp1['from_cache']}")
resp2 = post_list_view(req)
print(f"   Second call (hot): from_cache={resp2['from_cache']}")
resp3 = post_list_view(dict(req))
print(f"   Different req:     from_cache={resp3['from_cache']}")

# --- Low-level cache ---
print("\n2. Low-level cache API:")
t0 = time.time()
result1 = cached_expensive_query("trending_posts")
t1 = time.time()
print(f"   First call:  {len(result1)} results in {(t1-t0)*1000:.0f}ms")

t2 = time.time()
result2 = cached_expensive_query("trending_posts")
t3 = time.time()
print(f"   Second call: {len(result2)} results in {(t3-t2)*1000:.0f}ms (cached!)")

# --- Cache API operations ---
print("\n3. Cache API:")
cache.set("user_count", 42, timeout=60)
print(f"   get('user_count'): {cache.get('user_count')}")
cache.delete("user_count")
print(f"   after delete: {cache.get('user_count', 'NOT_FOUND')}")

# --- Template fragment cache ---
print("\n4. Fragment caching:")
def render_sidebar():
    time.sleep(0.2)
    return "<!-- sidebar with recent posts -->"

frag = fragment_cache.render_cached("sidebar", render_sidebar, timeout=30)
print(f"   Cached fragment: {frag}")

# --- Cache stats ---
print(f"\n5. Cache store entries: {len(CACHE_STORE)}")
for k, (v, exp) in CACHE_STORE.items():
    ttl = round(exp - time.time(), 1) if exp else "∞"
    print(f"   {k}: ttl={ttl}s")
