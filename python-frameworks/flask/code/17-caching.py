"""Caching: in-memory cache, TTL, cache decorator, cache invalidation."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import time
import functools
import re


# ======================== Cache System ========================

class Cache:
    def __init__(self, default_ttl: int = 60):
        self._data: dict[str, tuple[Any, float]] = {}
        self.default_ttl = default_ttl
        self.hits = 0
        self.misses = 0
        self._keys: dict[str, list[str]] = {}  # tag -> keys

    def get(self, key: str) -> Optional[Any]:
        if key in self._data:
            value, expiry = self._data[key]
            if expiry > time.time():
                self.hits += 1
                return value
            else:
                del self._data[key]
        self.misses += 1
        return None

    def set(self, key: str, value: Any, ttl: int | None = None, tags: list[str] = None):
        if ttl is None:
            ttl = self.default_ttl
        self._data[key] = (value, time.time() + ttl)
        if tags:
            for tag in tags:
                self._keys.setdefault(tag, []).append(key)

    def delete(self, key: str):
        self._data.pop(key, None)
        for tag, keys in self._keys.items():
            if key in keys:
                keys.remove(key)

    def clear(self):
        self._data.clear()
        self._keys.clear()

    def invalidate_tag(self, tag: str):
        """Invalidate all keys with a given tag."""
        for key in self._keys.get(tag, []):
            self._data.pop(key, None)
        self._keys[tag] = []

    def exists(self, key: str) -> bool:
        if key in self._data:
            _, expiry = self._data[key]
            if expiry > time.time():
                return True
            del self._data[key]
        return False

    def cached(self, key_prefix: str = "", ttl: int | None = None, tags: list[str] = None):
        """Decorator: cache function results."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kw):
                key = f"{key_prefix or func.__name__}:{str(args)}:{str(kw)}"
                result = self.get(key)
                if result is not None:
                    return result
                result = func(*args, **kw)
                self.set(key, result, ttl=ttl, tags=tags)
                return result
            return wrapper
        return decorator

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "size": len(self._data),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total * 100, 1) if total else 0,
            "tagged_keys": {t: len(k) for t, k in self._keys.items()},
        }


cache = Cache(default_ttl=30)


# ======================== Data Store ========================

class ProductStore:
    def __init__(self):
        self.products: dict[int, dict] = {}
        self._next = 1

    def all(self) -> list[dict]:
        time.sleep(0.05)
        return list(self.products.values())

    def get(self, pid: int) -> Optional[dict]:
        time.sleep(0.03)
        return self.products.get(pid)

    def create(self, data: dict) -> dict:
        product = {"id": self._next, **data, "created_at": datetime.now().isoformat()}
        self.products[self._next] = product
        self._next += 1
        cache.invalidate_tag("products")
        return product

    def update(self, pid: int, data: dict) -> Optional[dict]:
        if pid not in self.products:
            return None
        self.products[pid].update(data)
        cache.invalidate_tag("products")
        cache.delete(f"product:{pid}")
        return self.products[pid]

    def delete(self, pid: int) -> bool:
        if pid not in self.products:
            return False
        del self.products[pid]
        cache.invalidate_tag("products")
        cache.delete(f"product:{pid}")
        return True

store = ProductStore()

for name, price in [("Laptop", 999.99), ("Mouse", 29.99), ("Keyboard", 89.99), ("Monitor", 299.99)]:
    store.create({"name": name, "price": price})


# ======================== Cached Operations ========================

def get_all_products_slow():
    return store.all()

def get_all_products_cached():
    cached = cache.get("products:all")
    if cached:
        return cached
    result = store.all()
    cache.set("products:all", result, ttl=30, tags=["products"])
    return result

def get_product_cached(pid: int):
    key = f"product:{pid}"
    cached = cache.get(key)
    if cached:
        return cached
    product = store.get(pid)
    if product:
        cache.set(key, product, ttl=30, tags=["products"])
    return product


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.cache = cache

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    @staticmethod
    def _match_route(route_pattern: str, actual_path: str) -> dict | None:
        param_names = []
        def replacer(m):
            full = m.group(0)
            if ':' in full:
                typ, name = full.strip('<>').split(':')
            else:
                typ, name = 'str', full.strip('<>')
            param_names.append((name, typ))
            if typ == 'int': return r'(\d+)'
            if typ == 'float': return r'([0-9.]+)'
            if typ == 'path': return r'(.+)'
            return r'([^/]+)'
        regex = '^' + re.sub(r'<[^>]+>', replacer, route_pattern) + '$'
        m = re.match(regex, actual_path)
        if not m: return None
        return {name: int(val) if typ == 'int' else float(val) if typ == 'float' else val
                for (name, typ), val in zip(param_names, m.groups())}

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
            params = self._match_route(r["path"], path)
            if method in r["methods"] and params is not None:
                result = r["handler"](**params, **kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Routes ========================

@app.route("/products")
def list_products(**kw):
    use_cache = kw.get("use_cache", "true") != "false"
    if use_cache:
        products = get_all_products_cached()
        source = "cache"
    else:
        products = get_all_products_slow()
        source = "database"
    return {"products": products, "count": len(products), "source": source}

@app.route("/products/<int:product_id>")
def get_product(product_id, **kw):
    product = get_product_cached(product_id)
    if not product:
        return {"error": "Not found"}
    return {"product": product}

@app.route("/products", methods=["POST"])
def create_product(**kw):
    product = store.create({"name": kw.get("name", ""), "price": float(kw.get("price", 0))})
    return {"product": product, "message": "Created (cache invalidated)"}

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id, **kw):
    data = {}
    if "name" in kw: data["name"] = kw["name"]
    if "price" in kw: data["price"] = float(kw["price"])
    product = store.update(product_id, data)
    if not product:
        return {"error": "Not found"}
    return {"product": product, "message": "Updated (cached cleared)"}

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if not store.delete(product_id):
        return {"error": "Not found"}
    return {"message": "Deleted (cache cleared)"}

@app.route("/cache/stats")
def cache_stats():
    return app.cache.stats()

@app.route("/cache/clear", methods=["POST"])
def clear_cache():
    app.cache.clear()
    return {"message": "Cache cleared"}


# ======================== Demo ========================
print("=== Caching Demo ===\n")

print("1. First call (slow, from DB):")
r = app("GET", "/products", use_cache="false")
print(f"   Source: {r['data']['source']}, count: {r['data']['count']}")

print("\n2. Second call (fast, from cache):")
r = app("GET", "/products")
print(f"   Source: {r['data']['source']}, count: {r['data']['count']}\n")

print("3. Cache stats after 2 calls:")
r = app("GET", "/cache/stats")
print(f"   {json.dumps(r['data'], indent=2)}\n")

print("4. Create product (invalidates cache):")
r = app("POST", "/products", name="Tablet", price=499.99)
print(f"   Created: {r['data']['product']['name']}")
print(f"   Cache after create:")
r2 = app("GET", "/cache/stats")
print(f"   Tagged keys: {r2['data']['tagged_keys']}\n")

print("5. Get product by ID (cached after first call):")
print("   First call:")
r = app("GET", "/products/1")
print(f"   {r['data']['product']['name']}")
print("   Second call (cached):")
r = app("GET", "/products/1")
print(f"   {r['data']['product']['name']}")
r3 = app("GET", "/cache/stats")
print(f"   Cache hit rate: {r3['data']['hit_rate']}%\n")

print("6. Update product (clears specific cache entry):")
r = app("PUT", "/products/1", price=899.99)
print(f"   Updated: {r['data']['message']}")
r4 = app("GET", "/cache/stats")
print(f"   Cache size: {r4['data']['size']}\n")

print("7. Cache invalidation on delete:")
r = app("DELETE", "/products/4")
print(f"   {r['data']['message']}")
r5 = app("GET", "/cache/stats")
print(f"   Final cache size: {r5['data']['size']}")
print(f"   Final hit rate: {r5['data']['hit_rate']}%")
