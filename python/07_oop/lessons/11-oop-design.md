# 🎯 OOP Design Principles
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Apply Single Responsibility, DRY, Law of Demeter, and know when OOP is overkill using an e-commerce reporting system.

> 💡 **TL;DR — The whole point:** Good OOP design is about managing complexity — each class has one job, code isn't duplicated, and objects only talk to their immediate neighbors.

## 🔗 Why This Matters
Bad OOP creates spaghetti. Good OOP creates lego bricks — replace one piece without breaking the whole thing. These principles are your toolkit for designing maintainable systems.

## The Concept
**SRP:** One class = one responsibility. **DRY:** Don't repeat yourself. **Law of Demeter:** Only talk to your immediate friends. **YAGNI:** You ain't gonna need it (don't over-engineer). **Composition over inheritance.**

## Code Example
```python
"""E-commerce: Report generation — SRP violations and fixes."""

from dataclasses import dataclass, field
from typing import Callable
import json


# ——— Bad: Violates SRP ———
class BadOrderReport:
    def __init__(self, orders: list[dict]):
        self.orders = orders

    def calculate_totals(self) -> dict:
        return {
            "total_orders": len(self.orders),
            "total_revenue": sum(o["total"] for o in self.orders),
            "avg_order_value": sum(o["total"] for o in self.orders) / len(self.orders),
        }

    def format_json(self) -> str:
        return json.dumps(self.calculate_totals(), indent=2)

    def print_report(self) -> None:
        print(self.format_json())

    def save_to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.format_json())
    # Four reasons to change = four times the bugs


# ——— Good: SRP with separate classes ———
@dataclass
class OrderStats:
    total_orders: int
    total_revenue: float
    avg_order_value: float


class OrderAnalyzer:
    """Single responsibility: analyze orders into stats."""
    def __init__(self, orders: list[dict]):
        self.orders = orders

    def compute(self) -> OrderStats:
        revenue = sum(o["total"] for o in self.orders)
        return OrderStats(
            total_orders=len(self.orders),
            total_revenue=revenue,
            avg_order_value=revenue / len(self.orders) if self.orders else 0,
        )


class JsonFormatter:
    """Single responsibility: format data as JSON."""
    @staticmethod
    def format(data: OrderStats) -> str:
        return json.dumps(data.__dict__, indent=2)


class ReportPrinter:
    """Single responsibility: print reports."""
    @staticmethod
    def print_report(content: str) -> None:
        print(content)


# Usage — each piece is swappable
orders_data = [
    {"id": 1, "total": 150.0},
    {"id": 2, "total": 250.0},
    {"id": 3, "total": 99.99},
]

analyzer = OrderAnalyzer(orders_data)
stats = analyzer.compute()
formatted = JsonFormatter.format(stats)
ReportPrinter.print_report(formatted)
print(json.dumps(stats.__dict__))
```

## 🔍 How It Works
- **SRP:** `OrderAnalyzer` only analyzes; `JsonFormatter` only formats; `ReportPrinter` only prints
- If JSON format changes, only `JsonFormatter` changes — not the analyzer or printer
- **Law of Demeter:** `report.compute()` not `report.data.analyzer.compute_again()`
- **DRY:** Shared logic lives in one place (like `OrderStats`)
- **Know when OOP is overkill:** A simple `calculate_stats(orders)` function might suffice

## ⚠️ Common Pitfall
Over-engineering. Not everything needs a class. If a function will do, write a function. Start simple, refactor to classes when you need state or polymorphism.

## 🧠 Memory Aid
"SRP = one job per class. If you can't describe a class in one sentence without 'and', it's doing too much."

## 🏃 Try It
Add a `CsvFormatter` class to the example above that converts `OrderStats` to CSV. Swap `JsonFormatter` for `CsvFormatter` in the main flow.

## 🔗 Related
- [All previous lessons](01-classes-objects.md) — applying design to everything learned
- [Composition](09-composition.md) — has-a relationships

## ➡️ Next
[Metaclasses](12-metaclasses.md)
