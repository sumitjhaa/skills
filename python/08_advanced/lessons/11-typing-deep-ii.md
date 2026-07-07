# 🎯 Typing Deep II
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Advanced typing — `Protocol` for structural subtyping, `TypeGuard` for narrowing, `Never` for exhaustiveness, `Self` return type, `Unpack`, `TypeVarTuple`, `ParamSpec`, and `Concatenate`.

> 💡 **TL;DR — The whole point:** Advanced types give you compile-time safety for complex patterns — variadic generics, callback parameter types, type narrowing, and self-referencing return types.

## 🔗 Why This Matters
Libraries like FastAPI, Pydantic, and SQLAlchemy use these advanced typing features to provide type-safe APIs. `Protocol` powers structural subtyping (duck typing with safety). `TypeGuard` narrows types after checks. `Self` ensures fluent interfaces return the right type.

## The Concept
- `Protocol` — structural subtyping (nominal vs structural)
- `TypeGuard` — type narrowing function return
- `Never` — exhaustiveness checking (type-safe error handling)
- `Self` — return type of the current class
- `Unpack` / `TypeVarTuple` — variadic generics (multiple type params)
- `ParamSpec` / `Concatenate` — typing decorators and callback parameters

## Code Example
```python
"""E-commerce: Advanced typing for API clients, event system, decorators."""

from typing import (
    Protocol, TypeGuard, Never, Self, Unpack, TypeVarTuple,
    ParamSpec, Concatenate, runtime_checkable, assert_never,
)
from collections.abc import Callable
from functools import wraps
import json


# ─── Protocol: structural subtyping ───
@runtime_checkable
class Loggable(Protocol):
    def to_log(self) -> str: ...


class Order:
    def __init__(self, id: str, total: float):
        self.id = id
        self.total = total

    def to_log(self) -> str:
        return f"Order {self.id}: ${self.total:.2f}"


class User:
    def __init__(self, name: str):
        self.name = name

    def to_log(self) -> str:
        return f"User: {self.name}"


def log_activity(item: Loggable) -> None:
    print(f"[LOG] {item.to_log()}")


log_activity(Order("ORD-1", 150.0))
log_activity(User("Alice"))
print(f"Is loggable? {isinstance(Order('x', 1), Loggable)}")


# ─── TypeGuard: narrow types after checking ───
class CartItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


def is_discounted(item: object) -> TypeGuard[CartItem]:
    return isinstance(item, CartItem) and hasattr(item, "discount")


# ─── Never: exhaustiveness checking ───
class Success:
    def __init__(self, data: str):
        self.data = data


class Failure:
    def __init__(self, error: str):
        self.error = error


Result = Success | Failure


def handle_result(result: Result) -> str:
    match result:
        case Success(data=data):
            return f"OK: {data}"
        case Failure(error=err):
            return f"FAIL: {err}"
        case _:
            assert_never(result)  # type checker ensures all cases handled


# ─── Self: fluent builder pattern ───
class QueryBuilder:
    def __init__(self, table: str):
        self._table = table
        self._where_clauses: list[str] = []
        self._limit_val: int | None = None

    def where(self, condition: str) -> Self:
        self._where_clauses.append(condition)
        return self

    def limit(self, n: int) -> Self:
        self._limit_val = n
        return self

    def build(self) -> str:
        query = f"SELECT * FROM {self._table}"
        if self._where_clauses:
            query += " WHERE " + " AND ".join(self._where_clauses)
        if self._limit_val:
            query += f" LIMIT {self._limit_val}"
        return query


query = QueryBuilder("products").where("price > 100").where("stock > 0").limit(10).build()
print(f"Query: {query}")


# ─── ParamSpec: typing decorators ───
P = ParamSpec("P")


def logged(func: Callable[P, str]) -> Callable[P, str]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
        result = func(*args, **kwargs)
        print(f"[Logged] {func.__name__} -> {result}")
        return result
    return wrapper


@logged
def get_product_price(sku: str) -> str:
    return f"${99.99}"
```

## 🔍 How It Works
- `Protocol` defines structural interface — any object with matching methods satisfies it
- `TypeGuard` tells the type checker "if this returns True, the argument is this type"
- `Never` + `assert_never()` ensures all branches of a union are handled at compile time
- `Self` returns the exact type of the current class (not just the base class)
- `ParamSpec` captures the parameter types of a callable for decorator typing
- `TypeVarTuple` enables variadic generics for functions taking multiple types

## ⚠️ Common Pitfall
`Protocol` members must match exactly (name + signature). Extra methods don't break it, but missing methods do. Use `@runtime_checkable` sparingly — it adds overhead and can give false positives.

## 🧠 Memory Aid
"Protocol = 'interface without inheritance.' TypeGuard = 'trust me, it's this type.' Never = 'this should never happen.' Self = 'returns whatever class I'm in.'"

## 🏃 Try It
Create a `Serializable` Protocol with a `serialize()` method. Implement it for `Product` and `Order` classes. Then use `TypeGuard` to check if an object is `Serializable`.

## 🔗 Related
- [Typing Deep](09-typing-deep.md) — TypeVar, Generic, TypedDict
- [Concurrent Futures](12-concurrent-futures.md) — typing for concurrent code

## ➡️ Next
[Concurrent Futures](12-concurrent-futures.md)
