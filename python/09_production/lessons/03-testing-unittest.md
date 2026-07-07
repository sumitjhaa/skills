# 🎯 Testing with unittest
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Write unit tests with `unittest.TestCase`, use setUp/tearDown, assertions, test discovery, and mocking.

> 💡 **TL;DR — The whole point:** Tests catch bugs before users do. `unittest` is Python's built-in testing framework — no extra dependencies needed.

## 🔗 Why This Matters
A pricing calculator with a rounding error will cost money. A bad validation function will let invalid orders through. Tests catch these before production. `unittest` is available everywhere Python is installed.

## The Concept
`TestCase` groups related tests. Each test method starts with `test_`. `setUp()` runs before each test, `tearDown()` after. Assertions like `assertEqual`, `assertRaises`, `assertAlmostEqual` check results.

## Code Example
```python
"""E-commerce: Unit tests for order processing."""

import unittest
from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderItem:
    sku: str
    name: str
    price: float
    quantity: int


def calculate_total(items: list[OrderItem], discount: float = 0.0) -> float:
    if not items:
        raise ValueError("Order must have at least one item")
    subtotal = sum(item.price * item.quantity for item in items)
    discounted = subtotal * (1 - discount)
    return round(discounted * 1.08, 2)  # 8% tax


def validate_order(items: list[OrderItem]) -> bool:
    if not items:
        return False
    total_qty = sum(item.quantity for item in items)
    return 1 <= total_qty <= 100


class TestOrderProcessing(unittest.TestCase):

    def setUp(self):
        self.items = [
            OrderItem("LAP-001", "Laptop", 1499.99, 1),
            OrderItem("MOU-001", "Mouse", 29.99, 2),
        ]

    def test_calculate_total(self):
        total = calculate_total(self.items)
        expected = round((1499.99 * 1 + 29.99 * 2) * 1.08, 2)
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_with_discount(self):
        total = calculate_total(self.items, discount=0.1)
        subtotal = 1499.99 * 1 + 29.99 * 2
        expected = round(subtotal * 0.9 * 1.08, 2)
        self.assertAlmostEqual(total, expected, places=2)

    def test_calculate_total_empty_raises(self):
        with self.assertRaises(ValueError):
            calculate_total([])

    def test_validate_order_valid(self):
        self.assertTrue(validate_order(self.items))

    def test_validate_order_empty(self):
        self.assertFalse(validate_order([]))

    def test_validate_order_over_limit(self):
        too_many = [OrderItem("TST-001", "Test", 1.0, 101)]
        self.assertFalse(validate_order(too_many))

    def test_validate_order_single_item(self):
        single = [OrderItem("TST-001", "Test", 1.0, 1)]
        self.assertTrue(validate_order(single))

    def test_item_dataclass_equality(self):
        a = OrderItem("SKU", "Name", 10.0, 1)
        b = OrderItem("SKU", "Name", 10.0, 1)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
```

## 🔍 How It Works
- `unittest.main()` discovers and runs all `test_` methods
- `setUp()` creates fresh test fixtures before each test (test isolation)
- `assertEqual`, `assertTrue`, `assertFalse`, `assertAlmostEqual` for numeric comparisons
- `assertRaises(ValueError)` checks that the code raises the exception
- Test method names should describe what they test: `test_calculate_total_with_discount`
- `unittest.mock` (patch, MagicMock) replaces external dependencies during tests

## ⚠️ Common Pitfall
Tests that depend on each other. Each test should be independent — don't share mutable state between tests. Use `setUp()` for fresh state every time.

## 🧠 Memory Aid
"unittest = TestCase + test_methods + assertions. `setUp` = fresh start. `assertRaises` = 'this should blow up.'"

## 🏃 Try It
Add a test for `calculate_total` with a `discount=0.5` (50% off). Also add a test that verifies an order with a zero-price item still calculates correctly.

## 🔗 Related
- [Testing with pytest](04-testing-pytest.md) — pytest is unittest on steroids
- [Logging Deep](06-logging-deep.md) — logging for debugging

## ➡️ Next
[Testing with pytest](04-testing-pytest.md)
