# 🎯 Dataclasses & Namedtuple
<!-- ⏱️ 12 min read | 🟢 Core | 🧠 Core -->

**What You'll Learn:** Generate boilerplate automatically with `@dataclass`, customize with `field()`, and compare with `namedtuple`.

> 💡 **TL;DR — The whole point:** Dataclasses auto-generate `__init__`, `__repr__`, `__eq__`, and more — so you write less boilerplate and focus on data.

## 🔗 Why This Matters
E-commerce models need `Product`, `Customer`, `Order` — each with constructors, string representations, and equality checks. Dataclasses give you all that for free.

## The Concept
`@dataclass` reads your type annotations and generates `__init__`, `__repr__`, `__eq__`, and optionally `__hash__`, `__lt__`, etc. `field()` provides fine-grained control per field.

## Code Example
```python
"""E-commerce: Product and Order dataclasses with validation."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass(frozen=True, order=True)
class Product:
    name: str
    price: float
    sku: str = field(repr=False, compare=False)
    category: str = "General"
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Order:
    order_id: str
    customer: str
    items: list[Product] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING

    def add_product(self, product: Product) -> None:
        self.items.append(product)

    @property
    def total(self) -> float:
        return sum(p.price for p in self.items)


p1 = Product("Gaming Laptop", 1499.99, "TECH-001", tags=["electronics"])
p2 = Product("Wireless Mouse", 29.99, "ACC-002", category="Accessories")

order = Order("ORD-001", "Alice")
order.add_product(p1)
order.add_product(p2)

print(order)
print(f"Total: ${order.total:.2f}")
print(f"p1 == p2: {p1 == p2}")
print(f"p1 < p2: {p1 < p2}")  # True — price comparison
```

## 🔍 How It Works
- `frozen=True` makes instances immutable — like `namedtuple` but more flexible
- `order=True` generates comparison methods (uses fields in order, `price` first here)
- `field(repr=False)` excludes from `__repr__`; `default_factory=list` avoids mutable default pitfall
- `__post_init__` runs after auto-generated `__init__` — perfect for validation
- `namedtuple` is lighter (tuple subclass) but can't have methods beyond what you define

## ⚠️ Common Pitfall
Mutable default values: `items: list = []` creates one list shared by all instances. Always use `default_factory=list`.

## 🧠 Memory Aid
"Dataclass = write the fields, get the methods free. Like a carpenter bringing a nail gun."

## 🏃 Try It
Create a `Customer` dataclass with `name`, `email`, `loyalty_points` (default 0). Make it frozen. Add `__post_init__` to validate email contains `@`.

## 🔗 Related
- [Classes & Objects](01-classes-objects.md) — manual `__init__`
- [Dunder Methods](05-dunder-methods.md) — what dataclasses auto-generate

## ➡️ Next
[Composition](09-composition.md)
