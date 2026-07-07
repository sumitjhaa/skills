# 🎀 Decorators
<!-- ⏱️ 12 min read | 🔴 Hard | 🧠 Applied -->

**What You'll Learn:** How to wrap functions to add behavior (logging, timing, rate limiting) using the `@decorator` syntax.

> 💡 **TL;DR — The whole point:** A decorator is a function that takes a function and returns an enhanced version — like adding express shipping to a standard order.

## 🔗 Why This Matters
Generators produce values lazily; decorators modify behavior lazily. Instead of adding logging code inside every function, you write a logger decorator once and apply it with `@logger`.

## The Concept
A decorator is a callable (usually a function) that takes a function as input and returns a new function with extended behavior. Python's `@decorator` syntax is sugar for `func = decorator(func)`.

Think of decorators like app filters on a smartphone camera — the camera function stays the same, but the filter wraps it to add effects before/after.

## Code Example

```python
"""Decorators for logging, timing, rate limiting, and authentication."""

import functools
import time
import hashlib


def log_calls(func):
    """Log every call to the decorated function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper


def timeit(func):
    """Time how long a function takes."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def rate_limit(max_calls: int, per_seconds: float = 60.0):
    """Decorator factory: limit calls to max_calls per time window."""
    def decorator(func):
        calls = []

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [t for t in calls if now - t < per_seconds]
            if len(calls) >= max_calls:
                raise RuntimeError(f"Rate limit exceeded: {max_calls} calls per {per_seconds}s")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_auth(token: str):
    """Decorator factory: check auth token before running."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if token != "valid-secret-123":
                raise PermissionError("Invalid auth token")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log_calls
@timeit
def process_order(order_id: str, items: list) -> dict:
    """Process a customer order."""
    time.sleep(0.05)  # simulate work
    return {"order_id": order_id, "status": "confirmed", "items": items}


@rate_limit(max_calls=5, per_seconds=10)
def api_request(endpoint: str) -> str:
    return f"Data from {endpoint}"


print(process_order("ORD-123", ["laptop", "mouse"]))
print(api_request("/users"))
```

## 🔍 How It Works
- `@decorator` is syntactic sugar for `func = decorator(func)`
- `@functools.wraps` copies metadata (`__name__`, `__doc__`, `__module__`) from the original to the wrapper
- Decorators can accept arguments via an extra level of nesting (decorator factory)
- Stacked decorators run bottom-up: `@a @b func` → `a(b(func))`

## ⚠️ Common Pitfall
Forgetting `@functools.wraps`. Without it, the decorated function loses its name, docstring, and signature — making debugging confusing.

## 🧠 Memory Aid
**"Wrap, not replace"**: A decorator wraps the original function in a new one, preserving the original inside the closure.

## 🏃 Try It
Write a decorator `@retry(max_attempts=3)` that retries a function if it raises an exception, waiting 0.1s between attempts.

## 🔗 Related
- [Generators →](./06-generators.md)
- [Functools Module →](./08-functools.md)

## ➡️ Next
[Functools Module](./08-functools.md)
