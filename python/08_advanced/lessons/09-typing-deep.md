# 🎯 Typing Deep
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** `TypeVar`, `Generic`, `TypedDict`, `Literal`, `overload`, `Optional`, `Union`, `Any`, and `Protocol` for structural subtyping.

> 💡 **TL;DR — The whole point:** Type hints make your code self-documenting and enable static analysis (mypy, pyright) to catch bugs before runtime.

## 🔗 Why This Matters
In production codebases, type hints reduce bugs by 15-20%. Editors give better autocomplete, refactoring is safer, and documentation is always up-to-date. Most major Python projects (FastAPI, Pydantic, SQLAlchemy) use them extensively.

## The Concept
- `TypeVar` — generic type variable
- `Generic[T]` — parameterized class
- `TypedDict` — dict with specific keys/types
- `Literal` — exact value constraint
- `overload` — multiple type signatures for one function
- `Protocol` — structural subtyping (duck typing with types)

## Code Example
```python
"""E-commerce: Type hints for a shopping cart and data processing pipeline."""

from typing import TypeVar, Generic, TypedDict, Literal, overload, Protocol, Optional


# ─── TypedDict: structured product data ───
class ProductDict(TypedDict):
    sku: str
    name: str
    price: float
    category: str


# ─── Generic: reusable container ───
T = TypeVar("T")


class ShoppingCart(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def total(self) -> float:
        if not self._items:
            return 0.0
        return sum(i.price for i in self._items)  # type: ignore

    def __len__(self) -> int:
        return len(self._items)


# ─── Protocol: structural typing ───
class PricedItem(Protocol):
    price: float


def total_price(items: list[PricedItem]) -> float:
    return sum(item.price for item in items)


# ─── overload: multiple signatures ───
@overload
def apply_discount(price: float, percent: float) -> float: ...


@overload
def apply_discount(price: list[float], percent: float) -> list[float]: ...


def apply_discount(price: float | list[float], percent: float) -> float | list[float]:
    if isinstance(price, list):
        return [p * (1 - percent / 100) for p in price]
    return price * (1 - percent / 100)


# ─── Literal: exact values ───
def set_shipping(method: Literal["standard", "express", "overnight"]) -> str:
    costs = {"standard": 5.99, "express": 14.99, "overnight": 29.99}
    return f"{method} shipping: ${costs[method]}"


# ─── Usage ───
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


cart: ShoppingCart[Product] = ShoppingCart()
cart.add(Product("Laptop", 1499.99))
cart.add(Product("Mouse", 29.99))
print(f"Cart total: ${cart.total():.2f}")

print(f"Discount: ${apply_discount(100.0, 10):.2f}")
print(f"Bulk discount: {apply_discount([100.0, 200.0, 50.0], 10)}")
print(set_shipping("express"))
```

## 🔍 How It Works
- `TypedDict` lets you specify exact key-value types for dicts at compile time
- `Generic[T]` parameterizes a class — `ShoppingCart[Product]` type-checks item types
- `Protocol` enables structural subtyping: any class with a `price: float` attribute satisfies `PricedItem`
- `overload` defines multiple type signatures; only the implementation body matters at runtime
- `Literal["x", "y"]` constrains a value to exact strings
- `Optional[X]` = `X | None`; `Union[X, Y]` = `X | Y`

## ⚠️ Common Pitfall
`@overload` signatures are just for the type checker. The actual implementation must handle all cases. `overload` only adds type information; it doesn't change runtime behavior.

## 🧠 Memory Aid
"TypeVar = 'some type T.' Generic = 'works with any T.' TypedDict = 'dict with a schema.' Protocol = 'if it walks like a duck.' Literal = 'only these exact values.'"

## 🏃 Try It
Define a `ShippingOption` TypedDict with `method` (Literal["standard", "express"]), `cost` (float), and `days` (int). Create a generic `Process[T]` class that takes a list of T items and processes them.

## 🔗 Related
- [Functools Deep](08-functools-deep.md) — `singledispatch` with types
- [Typing Deep II](11-typing-deep-ii.md) — advanced type features

## ➡️ Next
[Advanced Patterns](10-advanced-patterns.md)
