# ⚡ Caching
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** In-memory caching, TTL, cache decorators, cache invalidation patterns.

## Why Cache?

Avoid recomputing expensive results (DB queries, API calls, template rendering).

## In-Memory Cache

```python
import time

class Cache:
    def __init__(self, default_ttl=60):
        self._data = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key in self._data:
            value, expiry = self._data[key]
            if expiry > time.time():
                self.hits += 1
                return value
            del self._data[key]
        self.misses += 1
        return None

    def set(self, key, value, ttl=None):
        ttl = ttl or self.default_ttl
        self._data[key] = (value, time.time() + ttl)
```

## Using Flask-Caching

```bash
pip install flask-caching
```

```python
from flask_caching import Cache

app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
cache = Cache(app)

@app.route("/products")
@cache.cached(timeout=60)
def list_products():
    # Expensive DB query
    return {"products": get_all_products()}
```

## Cache Decorator Pattern

```python
cache = Cache(default_ttl=30)

@cache.cached(key_prefix="products:all", ttl=60, tags=["products"])
def get_all_products_cached():
    return store.all()
```

## Cache Invalidation

```python
def create_product(data):
    product = store.create(data)
    cache.invalidate_tag("products")  # Clear all product caches
    return product

def update_product(pid, data):
    product = store.update(pid, data)
    cache.invalidate_tag("products")
    cache.delete(f"product:{pid}")  # Clear specific entry
    return product
```

## Cache Stats

```python
{
    "size": 15,        # Current cache entries
    "hits": 120,       # Cache hits
    "misses": 30,      # Cache misses
    "hit_rate": 80.0,  # Hit rate %
}
```

## Cache Types

| Backend | Use Case |
|---------|----------|
| `SimpleCache` | Development, single process |
| `RedisCache` | Production, distributed |
| `MemcachedCache` | High-performance |
| `FileSystemCache` | Persistent, no extra service |

<!-- 🧠 Invalidation is hard. Use tag-based invalidation to avoid stale data. -->

## Run the Code

```bash
python code/17-caching.py
```
