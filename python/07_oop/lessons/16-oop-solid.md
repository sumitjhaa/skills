# 🎯 SOLID Principles in Python
<!-- ⏱️ 20 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Apply SOLID principles with real-world Python examples — SRP, OCP, LSP, ISP, and DIP.

> 💡 **TL;DR — The whole point:** SOLID makes your code maintainable, testable, and extensible. Each principle prevents a specific kind of design rot.

## 🔗 Why This Matters
SOLID is the foundation of production-grade OOP. Frameworks like Django, FastAPI, and SQLAlchemy all follow these principles. Understanding them separates "writes code" from "designs systems."

## The Concept
- **S**ingle Responsibility — one class, one job
- **O**pen/Closed — open for extension, closed for modification
- **L**iskov Substitution — subclasses must work wherever parent works
- **I**nterface Segregation — many small interfaces > one big interface
- **D**ependency Inversion — depend on abstractions, not concretions

## Code Example
```python
"""SOLID principles with an e-commerce discount system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

# ——— S: Single Responsibility ———
# Each class has exactly one job

@dataclass
class Order:
    items: list[tuple[str, float]]  # (name, price)

    def total(self) -> float:
        return sum(price for _, price in self.items)


class OrderRepository:
    def save(self, order: Order) -> None:
        print(f"[DB] Saving order: ${order.total():.2f}")


class InvoicePrinter:
    @staticmethod
    def print_invoice(order: Order) -> str:
        lines = [f"{name}: ${price:.2f}" for name, price in order.items]
        return "\n".join(lines) + f"\nTotal: ${order.total():.2f}"


# ——— O: Open/Closed ———
# New discount types = new class, no modifications to existing code

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)


class BogoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.5  # buy one get one free


class OrderProcessor:
    def __init__(self, discount: DiscountStrategy):
        self.discount = discount  # DIP: depends on abstraction

    def process(self, order: Order) -> float:
        total = self.discount.apply(order.total())
        OrderRepository().save(order)
        return total


# ——— L: Liskov Substitution ———
# All DiscountStrategy subclasses work interchangeably

def apply_discount(discount: DiscountStrategy, amount: float) -> float:
    original = discount.apply(100.0)
    assert original <= 100.0, f"LSP violation: {original} > {100.0}"
    return original

assert apply_discount(NoDiscount(), 100) <= 100
assert apply_discount(PercentageDiscount(10), 100) <= 100
assert apply_discount(BogoDiscount(), 100) <= 100


# ——— I: Interface Segregation ———
# Protocol classes define minimal interfaces

class Shippable(Protocol):
    def weight_kg(self) -> float: ...


class Trackable(Protocol):
    def tracking_info(self) -> str: ...


class PhysicalProduct:
    def weight_kg(self) -> float:
        return 2.5

    def tracking_info(self) -> str:
        return "TRACK-123"


class DigitalProduct:
    def weight_kg(self) -> float:
        return 0.0  # digital products are light!


# ——— Usage ———
order = Order([("Laptop", 1500), ("Mouse", 30)])
processor = OrderProcessor(PercentageDiscount(10))
final = processor.process(order)
print(f"Order total after 10% discount: ${final:.2f}")
```

## 🔍 How It Works
- **SRP:** `Order` holds data, `OrderRepository` persists, `InvoicePrinter` formats, `OrderProcessor` orchestrates
- **OCP:** New discount = new subclass of `DiscountStrategy`. No need to modify `OrderProcessor`
- **LSP:** All `DiscountStrategy` subclasses can be swapped without breaking the caller
- **ISP:** `Shippable` and `Trackable` are focused protocols vs a giant `PhysicalProduct` interface
- **DIP:** `OrderProcessor` depends on `DiscountStrategy` (abstract), not on `PercentageDiscount` (concrete)

## ⚠️ Common Pitfall
Violating LSP by strengthening preconditions or weakening postconditions in subclasses. A subclass that raises new exceptions the parent didn't is an LSP violation.

## 🧠 Memory Aid
"SOLD + I = SOLID. Single job, Open for new, Liskov swap, Interface small, Dependency flipped."

## 🏃 Try It
Add a `FreeShippingDiscount` class that applies a $10 discount when total > $50. Make it a new `DiscountStrategy` subclass — don't modify existing code (proving OCP).

## 🔗 Related
- [OOP Design](11-oop-design.md) — foundational design principles
- [Composition](09-composition.md) — has-a vs is-a

## ➡️ Next
Review and practice with [Exercises](../practice/exercises.md)
