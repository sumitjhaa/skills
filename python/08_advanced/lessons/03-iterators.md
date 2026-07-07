# 🎯 Iterators
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** The iterator protocol, building custom iterators, understanding iterable vs iterator, and lazy evaluation patterns.

> 💡 **TL;DR — The whole point:** Iterators are objects that produce values one at a time via `__next__()`. Iterables are objects that can produce iterators via `__iter__()`.

## 🔗 Why This Matters
`for` loops, list comprehensions, `map()`, `filter()`, and `zip()` all use the iterator protocol. Understanding iterators means understanding how Python traverses data — and how to make your own objects iterable.

## The Concept
- **Iterable**: has `__iter__()` returning an iterator (e.g., list, str, dict)
- **Iterator**: has `__next__()` returning the next item or raising `StopIteration`

## Code Example
```python
"""E-commerce: Custom iterator for paginated API results and product catalog."""

from typing import Optional


class PaginatedAPI:
    """Simulates a paginated e-commerce product API."""
    def __init__(self, page_size: int = 3):
        self._all_products = [
            {"id": 1, "name": "Laptop", "price": 1499.99},
            {"id": 2, "name": "Mouse", "price": 29.99},
            {"id": 3, "name": "Keyboard", "price": 89.99},
            {"id": 4, "name": "Monitor", "price": 399.99},
            {"id": 5, "name": "Headphones", "price": 149.99},
            {"id": 6, "name": "Webcam", "price": 79.99},
            {"id": 7, "name": "Microphone", "price": 59.99},
        ]
        self.page_size = page_size

    def __iter__(self):
        """Return an iterator that pages through all products."""
        return _ProductIterator(self._all_products, self.page_size)


class _ProductIterator:
    def __init__(self, products: list[dict], page_size: int):
        self._products = products
        self._page_size = page_size
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> list[dict]:
        if self._index >= len(self._products):
            raise StopIteration
        page = self._products[self._index:self._index + self._page_size]
        self._index += self._page_size
        return page


# Iterable that lazily computes
class ProductSearch:
    """Iterable search results — lazy, no pre-computed list."""
    def __init__(self, products: list[dict], query: str):
        self._products = products
        self._query = query.lower()

    def __iter__(self):
        for product in self._products:
            if self._query in product["name"].lower():
                yield product  # generator is an iterator!


api = PaginatedAPI(page_size=3)
print("=== Paginated Products ===")
for page in api:
    print(f"  Page: {[p['name'] for p in page]}")

print("\n=== Lazy Search (e) ===")
search = ProductSearch(PaginatedAPI()._all_products, "e")
for product in search:
    print(f"  {product['name']}: ${product['price']}")
```

## 🔍 How It Works
- `for x in obj:` calls `iter(obj)` which calls `obj.__iter__()`, then calls `next()` on the iterator
- An iterator must implement `__next__()` and raise `StopIteration` when done
- A generator function is an easy way to create an iterator
- Iterables can be re-used (call `__iter__` multiple times); iterators are single-use
- Lazy iteration = compute values on demand, not ahead of time

## ⚠️ Common Pitfall
An iterator consumed once is empty. `list(iterator)` exhausts it. If you need to iterate multiple times, make your object an iterable (not just an iterator).

## 🧠 Memory Aid
"Iterable = vending machine (has a button). Iterator = the dispensing mechanism (gives one item at a time)."

## 🏃 Try It
Create a `Fibonacci` class that implements the iterator protocol: `__init__(self, limit)`, `__iter__(self)`, `__next__(self)`. Yield Fibonacci numbers up to `limit`.

## 🔗 Related
- [Generators Deep](02-generators-deep.md) — generators are iterators
- [itertools](04-itertools.md) — iterator building blocks

## ➡️ Next
[itertools](04-itertools.md)
