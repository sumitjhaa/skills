# 🎯 Decorators Deep
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** How decorators work internally, `@wraps`, stacking, argumented decorators, class-based decorators, and built-in decorator internals.

> 💡 **TL;DR — The whole point:** A decorator is a function that takes a function and returns a function — it's syntactic sugar for `func = decorator(func)`.

## 🔗 Why This Matters
Django's `@login_required`, Flask's `@app.route()`, FastAPI's `@app.get()`, pytest's `@pytest.fixture` — most Python web frameworks use decorators extensively. Understanding them demystifies framework magic.

## The Concept
`@decorator` is equivalent to `func = decorator(func)`. The decorator can enhance, log, time, cache, or modify the behavior of the decorated function.

## Code Example
```python
"""E-commerce: Decorators for logging, timing, and caching API calls."""

from functools import wraps
import time


def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  -> {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"  Retry {attempt + 1}/{max_attempts}: {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


class CountCalls:
    def __init__(self, func):
        wraps(func)(self)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


@log_calls
@retry(max_attempts=2)
def fetch_product_price(product_id: int) -> float:
    if product_id < 0:
        raise ValueError("Invalid ID")
    return 99.99


@CountCalls
def discount(price: float, percent: float) -> float:
    return price * (1 - percent / 100)


print(f"Price: ${fetch_product_price(42):.2f}")
print(f"Discounted: ${discount(100, 10):.2f}")
print(f"discount called {discount.count} times")
print(f"Function name preserved: {fetch_product_price.__name__}")
```

## 🔍 How It Works
- `@wraps(func)` copies `__name__`, `__doc__`, `__module__` from original to wrapper
- Stacking: `@log_calls` above `@retry()` means `log_calls(retry()(func))`
- Argumented decorators: `@retry(3)` → `retry(3)` returns a decorator, then `@that_decorator`
- Class-based: `__call__` makes the instance callable, `wraps(func)(self)` preserves metadata
- `@property` internally creates a descriptor: `property(fget, fset, fdel)`

## ⚠️ Common Pitfall
Forgetting `@wraps` — without it, introspection tools show the wrapper function's metadata, not the original's. `help()` and debuggers will lie to you.

## 🧠 Memory Aid
"Decorator = wrapping paper. `@wraps` = keeping the gift tag visible. Stacking = multiple layers of wrapping."

## 🏃 Try It
Write a `@validate_args` decorator that checks all arguments are positive numbers. Use it on a `divide(a, b)` function.

## 🔗 Related
- [Functools Deep](08-functools-deep.md) — `wraps`, `lru_cache`, `singledispatch`
- [Advanced Patterns](10-advanced-patterns.md) — decorator + generator combos

## ➡️ Next
[Generators Deep](02-generators-deep.md)
