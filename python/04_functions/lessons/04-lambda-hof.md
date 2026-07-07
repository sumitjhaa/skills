# λ Lambda & Higher-Order Functions
<!-- ⏱️ 12 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** How to write anonymous functions with `lambda` and use higher-order functions like `map`, `filter`, `sorted`, and `reduce`.

> 💡 **TL;DR — The whole point:** Lambda lets you write quick throwaway functions; higher-order functions let you process collections without loops.

## 🔗 Why This Matters
Closures showed you functions that create/modify functions. Now see how to pass functions as arguments — like telling a sorting algorithm *how* to sort, or a filter *what* to keep.

## The Concept
A **higher-order function** takes a function as an argument or returns one. `lambda` is a shorthand to create small anonymous functions. Think of it like giving instructions to a worker: "sort these products by price" — the sorting function is the worker, and the lambda is the instruction sheet.

## Code Example

```python
"""E-commerce — sorting products, filtering users, and order processing."""

from functools import reduce

products = [
    {"name": "Laptop", "price": 1200, "rating": 4.5},
    {"name": "Mouse", "price": 25, "rating": 4.8},
    {"name": "Keyboard", "price": 100, "rating": 4.2},
    {"name": "Monitor", "price": 350, "rating": 4.6},
    {"name": "Headphones", "price": 80, "rating": 4.3},
]

# sorted with key=lambda
by_price = sorted(products, key=lambda p: p["price"])
by_rating = sorted(products, key=lambda p: p["rating"], reverse=True)
print("Cheapest:", [p["name"] for p in by_price[:3]])
print("Top rated:", by_rating[0]["name"])

# filter — affordable products under $200
affordable = list(filter(lambda p: p["price"] < 200, products))
print(f"Affordable ({len(affordable)}): {[p['name'] for p in affordable]}")

# map — apply discount
def apply_discount(percent: float):
    return lambda p: {**p, "price": round(p["price"] * (1 - percent), 2)}

discounted = list(map(apply_discount(0.10), products))
print(f"After 10% off: {discounted[0]['name']} ${discounted[0]['price']}")

# reduce — total cart value using a pipeline
def total_cart(cart_items: list) -> float:
    return reduce(lambda acc, item: acc + item["price"], cart_items, 0.0)

print(f"Cart total: ${total_cart(products[:3])}")
```

## 🔍 How It Works
- `lambda args: expression` creates an anonymous function (single expression only)
- `map(f, iterable)` applies `f` to every element (lazy — wrap with `list()`)
- `filter(pred, iterable)` keeps elements where `pred` returns truthy
- `reduce(f, iterable, initial)` accumulates left to right
- `sorted(iterable, key=func)` uses `key` to extract comparison value

## ⚠️ Common Pitfall
Using `lambda` when you need statements. Lambda can only contain a single expression — no `if/else` blocks, no assignments. Use a regular `def` instead.

## 🧠 Memory Aid
**"lambda = one-line def"**. If your function fits on one line without assignments or statements, lambda works. Otherwise, use `def`.

## 🏃 Try It
Given `orders = [{"item": "book", "qty": 3, "price": 15}, {"item": "pen", "qty": 10, "price": 2}]`, use `reduce` to calculate the total order value (sum of qty × price).

## 🔗 Related
- [Scope & Closures →](./03-scope-closures.md)
- [Recursion →](./05-recursion.md)

## ➡️ Next
[Recursion](./05-recursion.md)
