# 🎯 Comprehensions Deep
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Nested comprehensions, set/dict comprehensions, generator expressions, and the walrus operator (`:=`) inside comprehensions.

> 💡 **TL;DR — The whole point:** Comprehensions build sequences in one line — clearer and faster than manual loops, but don't sacrifice readability.

## 🔗 Why This Matters
Data transformation is everywhere in Python. Comprehensions turn multi-line loops into single, readable expressions — for filtering lists, building lookups, transforming data, and more.

## The Concept
- `[expr for x in iterable if cond]` — list comprehension
- `{expr for x in iterable}` — set comprehension
- `{key: value for x in iterable}` — dict comprehension
- `(expr for x in iterable)` — generator expression (lazy)

## Code Example
```python
"""E-commerce: Comprehensions for product processing and data transformation."""

from dataclasses import dataclass

products = [
    {"name": "Laptop", "price": 1499.99, "category": "Electronics", "stock": 5},
    {"name": "Mouse", "price": 29.99, "category": "Accessories", "stock": 50},
    {"name": "Keyboard", "price": 89.99, "category": "Accessories", "stock": 0},
    {"name": "Monitor", "price": 399.99, "category": "Electronics", "stock": 10},
    {"name": "Webcam", "price": 79.99, "category": "Electronics", "stock": 0},
    {"name": "Desk", "price": 299.99, "category": "Furniture", "stock": 3},
]

# ─── List comprehension: filter + transform ───
in_stock_names = [p["name"] for p in products if p["stock"] > 0]
print(f"In stock: {in_stock_names}")

discounted = [{"name": p["name"], "sale_price": round(p["price"] * 0.9, 2)} for p in products]
print(f"Sale prices: {discounted[:3]}")

# ─── Dict comprehension: lookup by name ───
price_lookup = {p["name"]: p["price"] for p in products}
print(f"Laptop price: ${price_lookup['Laptop']}")

category_counts = {p["category"]: sum(1 for q in products if q["category"] == p["category"]) for p in products}
print(f"Categories: {category_counts}")

# ─── Set comprehension: unique categories ───
categories = {p["category"] for p in products}
print(f"Unique categories: {categories}")

# ─── Generator expression: lazy computation ───
total_value = sum(p["price"] * p["stock"] for p in products)
print(f"Total inventory value: ${total_value:.2f}")

top_prices = [price for price in (p["price"] for p in products) if price > 100]
print(f"Products over $100: {top_prices}")

# ─── Nested comprehension: flatten ───
order_items = [["Laptop", "Mouse"], ["Keyboard"], ["Monitor", "Webcam", "Cable"]]
all_items = [item for sublist in order_items for item in sublist]
print(f"Flattened: {all_items}")

# ─── Walrus operator (:=): computed once, used twice ───
results = [
    {"name": p["name"], "total": (total := p["price"] * p["stock"]), "status": "high" if total > 1000 else "low"}
    for p in products if p["stock"] > 0
]
print(f"\nWith walrus: {results}")
```

## 🔍 How It Works
- List comprehension: `[expr for var in iterable if condition]` — loop order matches nested `for`
- `{k: v for ...}` builds a dict; duplicates overwrite silently
- `{expr for ...}` builds a set; duplicates are removed
- Generator expression `(expr for ...)` is lazy — doesn't create the full list
- Nested comprehension: `[expr for a in A for b in B]` reads left-to-right, inner-most last
- Walrus: `(total := compute(x))` assigns and returns — use to avoid computing twice

## ⚠️ Common Pitfall
Nested comprehension order: `[expr for a in A for b in B]` equals `for a in A: for b in B: expr`. Read it left-to-right as nested loops, not matrix notation.

## 🧠 Memory Aid
"Square brackets = list, curly braces = dict/set, parentheses = lazy. Reads like math: `[f(x) for x in data if p(x)]`."

## 🏃 Try It
Given a list of transactions `[{"user": "Alice", "amount": 100}, {"user": "Bob", "amount": -50}, ...]`, use comprehensions to: (1) find the total positive amount, (2) build a dict of user→total, (3) find unique users with negative balances.

## 🔗 Related
- [Generators Deep](02-generators-deep.md) — generator expressions
- [itertools](04-itertools.md) — advanced iterator transformation

## ➡️ Next
[Functools Deep](08-functools-deep.md)
