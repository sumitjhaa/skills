# 🎯 Weakref & ContextVars
<!-- ⏱️ 15 min run | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Use `weakref` to prevent memory leaks and `contextvars` for async-safe context (request IDs, tracing).

> 💡 **TL;DR — The whole point:** `weakref` allows references that don't prevent garbage collection (solves circular reference leaks). `contextvars` provides per-context state that's safe across async tasks.

## 🔗 Why This Matters
Caches that hold references to objects can cause memory leaks if they prevent garbage collection. `WeakValueDictionary` solves this. In async code, global variables are thread-unsafe and async-unsafe — `contextvars` provides clean per-request state.

## The Concept
- `WeakRef` — reference that doesn't keep the object alive
- `WeakValueDictionary` — dict where values are weak references
- `WeakSet` — set with weak references
- `ContextVar` — variable that maintains different values per async context

## Code Example
```python
"""E-commerce: weakref for cache, contextvars for request tracing."""

from weakref import WeakValueDictionary
from contextvars import ContextVar
import gc
import asyncio


# ─── WeakValueDictionary: cache that doesn't leak ───
class Product:
    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"Product({self.sku}, {self.name})"


class ProductCache:
    """Cache with weak references — products can be GC'd when no one else references them."""
    def __init__(self):
        self._cache: WeakValueDictionary[str, Product] = WeakValueDictionary()

    def add(self, product: Product) -> None:
        self._cache[product.sku] = product

    def get(self, sku: str) -> Product | None:
        return self._cache.get(sku)

    @property
    def size(self) -> int:
        return len(self._cache)


cache = ProductCache()
p = Product("LAP-001", "Gaming Laptop", 1499.99)
cache.add(p)

print(f"Before delete: cache size = {cache.size}")
print(f"  Found: {cache.get('LAP-001')}")

del p  # Remove the strong reference
gc.collect()  # Force garbage collection

print(f"After delete: cache size = {cache.size}")
print(f"  Found: {cache.get('LAP-001')}")


# ─── ContextVars: request tracing in async code ───
request_id_var: ContextVar[str] = ContextVar("request_id", default="unknown")
user_var: ContextVar[str] = ContextVar("user", default="anonymous")


async def handle_request(request_id: str, user: str) -> None:
    token1 = request_id_var.set(request_id)
    token2 = user_var.set(user)

    print(f"  [Handler] {request_id_var.get()} — {user_var.get()}")
    await process_order()
    print(f"  [Handler done] {request_id_var.get()}")

    request_id_var.reset(token1)
    user_var.reset(token2)


async def process_order() -> None:
    # Automatically inherits the context from the caller
    print(f"  [Process] Request {request_id_var.get()}, user {user_var.get()}")
    await apply_discount()


async def apply_discount() -> None:
    print(f"  [Discount] For request {request_id_var.get()}")
    # Simulate work
    await asyncio.sleep(0.05)


async def main() -> None:
    print("\n=== ContextVars: concurrent request tracing ===")
    await asyncio.gather(
        handle_request("REQ-001", "Alice"),
        handle_request("REQ-002", "Bob"),
        handle_request("REQ-003", "Charlie"),
    )


asyncio.run(main())
```

## 🔍 How It Works
- `WeakValueDictionary` stores values as weak references — when only weak refs remain, the object is garbage collected
- `WeakRef(obj)` creates a weak reference — call `ref()` to get the object (or `None` if collected)
- `WeakSet` behaves like a set but with weak references to its elements
- `ContextVar` creates a variable that's local to an async context (task/coroutine)
- `.set(value)` returns a token; `.reset(token)` restores the previous value
- Child tasks inherit parent context automatically (copy-on-behave)

## ⚠️ Common Pitfall
`WeakValueDictionary` values that are only referenced by the dict will be immediately GC'd. Always keep a strong reference outside the cache. Also, `weakref` doesn't work with some built-in types like `int`, `str`, `list` (use a wrapper class).

## 🧠 Memory Aid
"Weakref = 'I can see it, but I won't keep it alive.' ContextVar = 'global variable that's polite in async code.'"

## 🏃 Try It
Create a `WeakSet`-based `EventListener` registry that automatically removes listeners when they're garbage collected. Add listeners, delete one, collect, and show the remaining.

## 🔗 Related
- [Advanced importlib & inspect](14-advanced-importlib-inspect.md) — runtime introspection
- [Concurrent Futures](12-concurrent-futures.md) — parallel execution

## ➡️ Next
[Advanced importlib & inspect](14-advanced-importlib-inspect.md)
