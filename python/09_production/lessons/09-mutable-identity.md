# 🎯 Mutable, Identity & Copy
<!-- ⏱️ 13 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Understand mutable vs immutable objects, `==` vs `is`, shallow copy vs deep copy, and avoid common bugs.

> 💡 **TL;DR — The whole point:** `==` checks value equality, `is` checks identity (same object). Mutable objects can change in place — copying is sometimes necessary to avoid unintended side effects.

## 🔗 Why This Matters
A function that modifies a passed list (expecting a copy) will alter the original data — a classic source of bugs in e-commerce cart and inventory operations.

## The Concept
- **Immutable:** `int`, `str`, `tuple`, `frozenset` — can't be changed in place
- **Mutable:** `list`, `dict`, `set`, custom objects — can be modified in place
- `==` compares values; `is` compares memory addresses
- **Shallow copy:** copies the container but not the nested objects
- **Deep copy:** recursively copies everything

## Code Example
```python
"""E-commerce: Mutable vs immutable in order and inventory operations."""

import copy
from dataclasses import dataclass


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int


# ─── Mutable default pitfall ───
def add_item_bad(item: str, cart: list[str] = []) -> list[str]:
    cart.append(item)  # BUG: default list is shared across calls!
    return cart


print("Shared default list:")
print(f"  {add_item_bad('Laptop')}")
print(f"  {add_item_bad('Mouse')}")  # ['Laptop', 'Mouse'] — not ['Mouse']!


def add_item_good(item: str, cart: list[str] | None = None) -> list[str]:
    if cart is None:
        cart = []
    cart.append(item)
    return cart


print("\nNone default (correct):")
print(f"  {add_item_good('Laptop')}")
print(f"  {add_item_good('Mouse')}")


# ─── Shallow vs Deep copy ───
original_cart: list[CartItem] = [
    CartItem("Laptop", 1499.99, 1),
    CartItem("Mouse", 29.99, 2),
]

shallow = copy.copy(original_cart)
deep = copy.deepcopy(original_cart)

# Modifying a nested item
original_cart[0].quantity = 5

print("\nAfter modifying original_cart[0].quantity = 5:")
print(f"  Original: {original_cart[0].quantity}")  # 5
print(f"  Shallow:  {shallow[0].quantity}")         # 5 — shared reference!
print(f"  Deep:     {deep[0].quantity}")             # 1 — independent copy


# ─── == vs is ───
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(f"\na == b: {a == b}")  # True (same values)
print(f"a is b: {a is b}")   # False (different objects)
print(f"a is c: {a is c}")   # True (same object)


# ─── Immutable trick ───
x = 256
y = 256
print(f"\nx is y for 256: {x is y}")   # True (CPython caches small ints)

x = 1000
y = 1000
print(f"x is y for 1000: {x is y}")   # May be False (depends on CPython)
```

## 🔍 How It Works
- **Mutable:** `list.append()`, `dict[key] = val`, `set.add()` — modify in place
- **Immutable:** `a += 1` creates a new `int` object, doesn't modify the old one
- **Shallow copy:** `copy.copy(obj)` — new container, same nested objects
- **Deep copy:** `copy.deepcopy(obj)` — new container, new nested objects (recursive)
- **`is`:** checks `id()` — use for `None` checks: `x is None` (not `x == None`)
- **`==`:** checks `__eq__` — use for value comparison

## ⚠️ Common Pitfall
Mutable default arguments. `def func(items=[])` creates one list at definition time, shared by all calls. Use `items=None` and create a new list inside the function.

## 🧠 Memory Aid
"'==' = do these look the same? 'is' = are these literally the same object? Mutable = can change in place. Immutable = must create new. Copy = 'just in case.'"

## 🏃 Try It
Write a function `apply_bulk_discount(cart, discount)` that takes a list of CartItem and applies a discount to all prices. Show the difference between modifying the original list (side effect) vs working on a deep copy.

## 🔗 Related
- [Slots & New](../07_oop/lessons/10-slots-new.md) — memory optimization
- [Dataclasses](../07_oop/lessons/08-dataclasses.md) — `frozen=True` for immutability

## ➡️ Next
[Packaging & Distribution](10-packaging.md)
