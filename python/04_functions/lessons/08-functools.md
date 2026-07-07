# 🧰 Functools Module
<!-- ⏱️ 13 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to use `partial`, `lru_cache`, `singledispatch`, and `reduce` from the functools module.

> 💡 **TL;DR — The whole point:** Functools gives you tools to transform functions — freeze arguments, cache results, dispatch by type, and fold sequences.

## 🔗 Why This Matters
Decorators let you wrap functions. Functools gives you production-ready utilities: cache expensive DB queries, build partial URL builders, create type-dispatching API handlers.

## The Concept
The `functools` module provides higher-order functions that work *with* or *return* other functions:
- `partial` — pre-fill some arguments (like a function with presets)
- `lru_cache` — memoize pure functions (cache results)
- `singledispatch` — call different implementations based on argument type
- `reduce` — fold/accumulate a sequence into a single value
- `total_ordering` — fill in missing comparison operators

## Code Example

```python
"""Functools: caching DB queries, partial URL builders, singledispatch API handlers."""

from functools import partial, lru_cache, singledispatch, reduce
import json


def build_url(base: str, path: str, **params: str) -> str:
    """Build a URL with query parameters."""
    query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    return f"{base}/{path}?{query}" if query else f"{base}/{path}"


# Partial — freeze the base URL for different API versions
api_v1 = partial(build_url, "https://api.example.com/v1")
api_v2 = partial(build_url, "https://api.example.com/v2")

print(api_v1("users", id="123"))        # https://api.example.com/v1/users?id=123
print(api_v2("orders", status="active", page="1"))


# lru_cache — cache database query results
@lru_cache(maxsize=32)
def get_user_by_id(user_id: int) -> dict:
    """Simulate an expensive DB query."""
    print(f"  [DB] Fetching user {user_id}...")
    return {"id": user_id, "name": f"User_{user_id}"}


print(get_user_by_id(1))  # [DB] Fetching...
print(get_user_by_id(1))  # from cache (no [DB] print)


# singledispatch — API response formatter
@singledispatch
def format_response(data) -> str:
    return f"Unknown type: {type(data).__name__}"


@format_response.register(dict)
def _(data: dict) -> str:
    return json.dumps(data, indent=2)


@format_response.register(list)
def _(data: list) -> str:
    return "\n".join(f"- {item}" for item in data)


print(format_response({"user": "alice", "role": "admin"}))
print(format_response(["laptop", "mouse", "keyboard"]))


# reduce — aggregate order values
orders = [("laptop", 1200), ("mouse", 25), ("keyboard", 100)]
total = reduce(lambda acc, item: acc + item[1], orders, 0)
print(f"Total order value: ${total}")
```

## 🔍 How It Works
- `partial(func, *args, **kwargs)` returns a callable with preset arguments
- `lru_cache` caches return values in a dict keyed by arguments; `maxsize=None` = unlimited
- `singledispatch` dispatches to registered implementations based on the first argument's type
- `reduce(func, iterable, initial)` applies `func` cumulatively left-to-right
- `wraps` preserves original function metadata (use inside decorators)

## ⚠️ Common Pitfall
Caching non-hashable arguments with `lru_cache`. Arguments must be hashable (no lists, dicts). Use `functools.cache` (Python 3.9+) for simpler cases.

## 🧠 Memory Aid
**"PARTIAL = PRESET, CACHE = REMEMBER, DISPATCH = CHOOSE, REDUCE = FOLD"**: Each tool does one job — partial pre-fills, cache remembers, dispatch routes by type, reduce collapses.

## 🏃 Try It
Use `partial` to create `get_user = partial(api_v1, "users")`, then call `get_user(id="42")`. Use `lru_cache` to memoize a `fib(n)` function.

## 🔗 Related
- [Decorators →](./07-decorators.md)
- [Error Handling in Functions →](./09-error-handling-functions.md)

## ➡️ Next
[Error Handling in Functions](./09-error-handling-functions.md)
