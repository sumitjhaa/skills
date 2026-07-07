# 🎯 PEP 8 & Code Style
<!-- ⏱️ 10 min read | 🟢 Core | 🧠 Applied -->

**What You'll Learn:** Write clean, PEP 8 compliant Python code — naming conventions, line length, imports, blank lines, and type annotations.

> 💡 **TL;DR — The whole point:** PEP 8 is Python's style guide. Consistent code is readable code — and readable code has fewer bugs.

## 🔗 Why This Matters
Code is read far more often than it's written. PEP 8 ensures that when you read code from any team member, it looks like Python — not "somebody's personal dialect of Python."

## The Concept
- **Indentation:** 4 spaces (no tabs!)
- **Line length:** 79 characters (99 for docstrings/comments)
- **Naming:** `snake_case` for functions/vars, `UPPER_CASE` for constants, `PascalCase` for classes
- **Imports:** standard lib → third-party → local, each group separated by a blank line
- **Blank lines:** two around top-level definitions, one around methods

## Code Example
```python
"""PEP 8 compliant module — e-commerce order processing."""

import json
import os
from typing import Final, Optional

import requests
from pydantic import BaseModel

# Constants use UPPER_CASE
TAX_RATE: Final[float] = 0.08
MAX_ITEMS_PER_ORDER: Final[int] = 100


class OrderItem(BaseModel):
    """One item in an order. PascalCase for classes."""
    sku: str
    name: str
    price: float
    quantity: int


def calculate_total(items: list[OrderItem], discount: float = 0.0) -> float:
    """Calculate order total with tax and discount. snake_case for functions."""
    subtotal = sum(item.price * item.quantity for item in items)
    discounted = subtotal * (1 - discount)
    return round(discounted * (1 + TAX_RATE), 2)


def validate_order(items: list[OrderItem]) -> bool:
    """Ensure order meets business rules."""
    if not items:
        return False
    total_qty = sum(item.quantity for item in items)
    return total_qty <= MAX_ITEMS_PER_ORDER


# Two blank lines before top-level code
if __name__ == "__main__":
    items = [
        OrderItem(sku="LAP-001", name="Laptop", price=1499.99, quantity=1),
        OrderItem(sku="MOU-001", name="Mouse", price=29.99, quantity=2),
    ]

    if validate_order(items):
        total = calculate_total(items)
        print(f"Order total: ${total:.2f}")
    else:
        print("Order validation failed")
```

## 🔍 How It Works
- **Black** and **ruff** auto-format code to PEP 8 — use them in CI/CD
- Continuous line (backslash) vs implied continuation (parentheses): prefer parentheses
- Avoid `from module import *` — it pollutes the namespace
- Type annotations (`: int`, `-> float`) are increasingly expected in production code
- Ruff also enforces `isort` for import ordering

## ⚠️ Common Pitfall
Mixing tabs and spaces. Python 3 rejects inconsistent indentation. Set your editor to "convert tabs to spaces" and use 4-space indentation always.

## 🧠 Memory Aid
"Black formats, Ruff lints, PEP 8 is the rulebook. `snake_case` for functions, `PascalCase` for classes, `UPPER_CASE` for constants."

## 🏃 Try It
Take a poorly formatted snippet (mix of 2-space and 4-space, no blank lines, bad imports) and fix it to PEP 8. Then run `ruff check` on it.

## 🔗 Related
- [Project Structure](01-project-structure.md) — organizing by module
- [Type Checking](07-type-checking.md) — mypy and type annotations

## ➡️ Next
[Testing with unittest](03-testing-unittest.md)
