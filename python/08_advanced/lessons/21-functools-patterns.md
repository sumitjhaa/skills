# 🎯 functools Patterns: cached_property, singledispatchmethod, cache
<!-- ⏱️ 13 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `cached_property`, `singledispatchmethod`, `cache`, and `partial` for efficient ML data pipelines and API wrappers.

> 💡 **TL;DR — The whole point:** `functools` optimizes repeated work — `cache` memoizes function calls, `cached_property` computes once per instance, `singledispatchmethod` dispatches by type on methods, and `partial` freezes arguments for reusable specialized functions.

## 🔗 Why This Matters
ML data pipelines normalize expensive transformations once. API wrappers cache responses to avoid redundant HTTP calls. Processing different data types without `if-elif` chains keeps code clean and extensible.

## The Concept
`@cache` memoizes pure function results (unbounded). `@cached_property` computes an attribute once per instance and caches it for its lifetime. `@singledispatchmethod` routes method calls based on the first argument's type. `partial` pre-fills arguments to create specialized functions from general ones.

## Code Example
```python
"""functools patterns: caching, partials, singledispatch — real API/ML pipelines"""
from functools import cache, cached_property, partial, singledispatchmethod, reduce
import time

class DataAnalyzer:
    """ML data analysis with cached computations and dispatch by type"""
    def __init__(self, data):
        self._data = data

    @cached_property
    def normalized(self):
        """Computed once, cached for life — like @property but auto-cached.
           Use when value is expensive to compute and won't change."""
        print("  [Compute] Normalizing...")  # Would be real ML preprocessing
        return [x / max(self._data) for x in self._data]

    @singledispatchmethod  # Dispatch on FIRST argument type
    def analyze(self, arg):
        raise NotImplementedError(f"No handler for {type(arg)}")

    @analyze.register
    def _(self, arg: int):
        return f"Count: {arg} items"

    @analyze.register
    def _(self, arg: list):
        return f"List: {sum(arg)} total, {len(arg)} items"

# @cache: memoize pure function results (unbounded, unlike lru_cache)
@cache
def api_fetch(endpoint: str) -> dict:
    print(f"  Fetching {endpoint}...")  # Simulates HTTP request
    return {"status": "ok", "data": endpoint}

# partial: freeze arguments to create specialized functions
def send_email(to: str, subject: str, body: str) -> str:
    return f"To: {to} | Subject: {subject} | Body: {body[:20]}..."
send_alert = partial(send_email, to="ops@company.com", subject="URGENT: System Alert")

# Usage
obj = DataAnalyzer([10, 20, 30, 40, 50])
print(f"Normalized: {obj.normalized}")
print(f"Cached: {obj.normalized}")  # No [Compute] — uses cached value
print(f"Int: {obj.analyze(100)}")
print(f"List: {obj.analyze([1,2,3])}")
print(api_fetch("/users"))   # Prints [Compute]
print(api_fetch("/users"))   # Cached — no print
print(send_alert(body="Database is down on server-01"))
```

## 🔍 How It Works
- `@cached_property` replaces the attribute with its cached value after first access (no recomputation)
- `@singledispatchmethod` inspects the type of the first argument after `self` and calls the matching `@register`-ed handler
- `@cache` stores return values in a dict keyed by arguments — unbounded memory, use only for finite argument spaces
- `partial(func, arg=val)` returns a new callable with some arguments already bound
- `reduce` is imported but not shown in usage — it accumulates values left-to-right

## ⚠️ Common Pitfall
`@cache` is unbounded — unlike `lru_cache(maxsize=128)`, it never evicts entries. If your function can receive millions of distinct arguments, use `lru_cache` with a `maxsize` instead to avoid memory leaks.

## 🧠 Memory Aid
"cached_property = 'compute once, keep forever.' cache = 'same inputs, same outputs, skip work.' singledispatchmethod = 'method overloading for Python.' partial = 'preset some knobs.'"

## 🏃 Try It
Add a `@cache`-ed function `fib(n)` that computes the nth Fibonacci number recursively. Call it with values 0-50 and see how many calls are saved.

## 🔗 Related
- [Functools Deep](08-functools-deep.md) — `lru_cache`, `wraps`, `reduce`

## ➡️ Next
[itertools Recipes](22-itertools-recipes.md)
