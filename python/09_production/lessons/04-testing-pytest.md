# 🎯 Testing with pytest
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Write cleaner tests with pytest — fixtures, parametrize, conftest.py, monkeypatch, and tmp_path.

> 💡 **TL;DR — The whole point:** pytest makes testing simpler with `assert` statements (no `self.assertEqual`), powerful fixtures, and automatic test discovery.

## 🔗 Why This Matters
pytest is the most popular testing framework in Python. It's used by FastAPI, SQLAlchemy, Pydantic, and most modern projects. It catches more bugs with less code.

## The Concept
- `assert` instead of `self.assertEqual`
- `@pytest.fixture` for reusable test data
- `@pytest.mark.parametrize` for testing multiple cases
- `conftest.py` for shared fixtures across test files
- `monkeypatch` for mocking, `tmp_path` for temp files

## Code Example
```python
"""E-commerce: pytest tests for checkout and discount system."""

import pytest
from dataclasses import dataclass


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int


def checkout_total(items: list[CartItem], coupon: str = "") -> float:
    subtotal = sum(i.price * i.quantity for i in items)
    if coupon == "SAVE10":
        subtotal *= 0.9
    elif coupon == "SAVE20":
        subtotal *= 0.8
    return round(subtotal * 1.08, 2)  # 8% tax


def apply_shipping(total: float) -> float:
    return total + (5.99 if total < 50 else 0)


# ─── Fixtures ───
@pytest.fixture
def sample_cart() -> list[CartItem]:
    return [
        CartItem("Laptop", 1499.99, 1),
        CartItem("Mouse", 29.99, 2),
    ]


@pytest.fixture
def empty_cart() -> list[CartItem]:
    return []


# ─── Basic tests ───
def test_checkout_basic(sample_cart):
    total = checkout_total(sample_cart)
    subtotal = 1499.99 + 29.99 * 2
    assert total == round(subtotal * 1.08, 2)


# ─── Parametrize ───
@pytest.mark.parametrize("coupon,expected_mult", [
    ("", 1.08),
    ("SAVE10", 1.08 * 0.9),
    ("SAVE20", 1.08 * 0.8),
    ("INVALID", 1.08),
])
def test_checkout_coupons(sample_cart, coupon, expected_mult):
    total = checkout_total(sample_cart, coupon)
    subtotal = 1499.99 + 29.99 * 2
    assert total == round(subtotal * expected_mult, 2)


# ─── Edge cases ───
def test_checkout_empty(empty_cart):
    assert checkout_total(empty_cart) == 0.0


def test_checkout_single_item():
    total = checkout_total([CartItem("USB Cable", 15.99, 1)])
    assert total == round(15.99 * 1.08, 2)


# ─── Shipping ───
@pytest.mark.parametrize("total,expected", [
    (30.0, 35.99),   # under $50 + $5.99
    (50.0, 50.0),    # exactly $50, free shipping
    (100.0, 100.0),  # over $50, free shipping
])
def test_shipping(total, expected):
    assert apply_shipping(total) == expected


# ─── Monkeypatch example ───
def test_monkeypatch_shipping(monkeypatch, sample_cart):
    monkeypatch.setattr("sys.platform", "darwin")
    total = checkout_total(sample_cart)
    shipping = apply_shipping(total)
    assert shipping >= total
```

## 🔍 How It Works
- pytest discovers files named `test_*.py` and functions named `test_*`
- Fixtures are injected by name — `test_checkout_basic(sample_cart)` gets `sample_cart`
- `@pytest.mark.parametrize` runs the test once for each tuple of arguments
- Fixtures can be scoped: `function` (default), `class`, `module`, `session`
- `monkeypatch.setattr()` temporarily replaces attributes for testing
- `tmp_path` provides a temporary directory (pathlib.Path) per test

## ⚠️ Common Pitfall
Mutable fixtures are shared across tests if scoped at module/session level. If a test modifies a list fixture, other tests see the modification. Use `function` scope for mutable data.

## 🧠 Memory Aid
"pytest = `assert` + fixtures + parametrize. Fixtures = 'I need this to test.' Parametrize = 'test this many ways.'"

## 🏃 Try It
Add a `@pytest.mark.parametrize` test for `checkout_total` that verifies the 8% tax rate with 5 different subtotals. Also add a test that verifies behavior with `Coupon("SAVE10")` on an empty cart.

## 🔗 Related
- [Testing with unittest](03-testing-unittest.md) — unittest basics
- [Pydantic & Settings](13-pydantic-settings.md) — validating config with pydantic

## ➡️ Next
[Argparse](05-argparse.md)
