# 🎯 Functools Deep
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Master `lru_cache`, `singledispatch`, `partial`, `wraps`, `cached_property`, and `reduce`.

> 💡 **TL;DR — The whole point:** `functools` provides higher-order functions that modify or enhance other functions — caching, dispatching, partial application, and more.

## 🔗 Why This Matters
Expensive computations, API calls, database queries — `lru_cache` memoizes results. Processing different data types — `singledispatch` replaces `if-elif` chains. Fixing arguments — `partial` creates specialized functions.

## The Concept
- `lru_cache` / `cache` — memoize function results
- `singledispatch` — dispatch based on first argument type
- `partial` — pre-fill function arguments
- `wraps` — copy function metadata to wrappers
- `cached_property` — lazy cached attribute
- `reduce` — accumulate across iterable

## Code Example
```python
"""E-commerce: functools for pricing, promotions, and data processing."""

from functools import lru_cache, singledispatch, partial, wraps, reduce
import time


# ─── lru_cache: cache expensive computations ───
@lru_cache(maxsize=128)
def compute_shipping_cost(weight_kg: float, distance_km: int, express: bool = False) -> float:
    """Expensive calculation — simulated with sleep."""
    time.sleep(0.05)  # simulate computation
    base = weight_kg * 0.5 + distance_km * 0.01
    return base * 2 if express else base


# First call is slow, subsequent calls are instant
print(f"Shipping: ${compute_shipping_cost(2.5, 1000):.2f}")
print(f"Cached: ${compute_shipping_cost(2.5, 1000):.2f}")  # fast
print(f"Cache info: {compute_shipping_cost.cache_info()}")


# ─── singledispatch: type-based dispatch ───
@singledispatch
def format_price(value) -> str:
    return str(value)


@format_price.register(float)
def _(value: float) -> str:
    return f"${value:.2f}"


@format_price.register(int)
def _(value: int) -> str:
    return f"${value}.00"


@format_price.register(list)
def _(value: list) -> str:
    return ", ".join(format_price(v) for v in value)


print(f"\nFloat: {format_price(49.99)}")
print(f"Int: {format_price(50)}")
print(f"List: {format_price([10, 20.5, 30])}")


# ─── partial: pre-fill arguments ───
def apply_discount(price: float, discount_pct: float, tax_rate: float = 0.08) -> float:
    return price * (1 - discount_pct / 100) * (1 + tax_rate)


ten_percent_off = partial(apply_discount, discount_pct=10)
fifty_percent_off = partial(apply_discount, discount_pct=50)

print(f"\n10% off $100: ${ten_percent_off(100):.2f}")
print(f"50% off $100: ${fifty_percent_off(100):.2f}")

# ─── reduce: accumulate across iterable ───
prices = [10, 20, 30, 40]
total = reduce(lambda a, b: a + b, prices)
print(f"\nTotal (reduce): ${total}")

# Running max
max_price = reduce(lambda a, b: a if a > b else b, prices)
print(f"Max price: ${max_price}")
```

## 🔍 How It Works
- `lru_cache` stores results in a dict keyed by arguments; `maxsize` controls memory
- `cache_info()` returns hits, misses, maxsize, currsize
- `singledispatch` registers type-specific implementations — `register(type)` decorator
- `partial(func, arg)` returns a callable with some args pre-filled
- `reduce(func, iterable, initial)` — apply func cumulatively (left-to-right)
- `wraps` copies `__name__`, `__doc__`, `__module__`, `__dict__` to wrapper functions

## ⚠️ Common Pitfall
`lru_cache` arguments must be hashable. You can't use `list` or `dict` as arguments (convert to tuple/frozenset first). Also, mutable defaults inside cached functions are shared across calls.

## 🧠 Memory Aid
"lru_cache = 'remember this for later.' singledispatch = 'do this for floats, that for ints.' partial = 'preset some knobs.' reduce = 'fold left.'"

## 🏃 Try It
Use `lru_cache` on a recursive Fibonacci function. Compare performance with and without caching for `fib(35)`. Show cache_info().

## 🔗 Related
- [Decorators Deep](01-decorators-deep.md) — `wraps` in practice
- [Typing Deep](09-typing-deep.md) — `@singledispatch` with type hints

## ➡️ Next
[Typing Deep](09-typing-deep.md)
