# 🎯 Classes & Objects
<!-- ⏱️ 10 min read | 🟢 Core | 🧠 Core -->

**What You'll Learn:** Define classes, create objects, and distinguish instance attributes from class attributes using an e-commerce domain.

> 💡 **TL;DR — The whole point:** A class is a blueprint; an object is the thing you build from that blueprint.

## 🔗 Why This Matters
You've used strings, lists, and dicts — those are objects too. Now you'll learn to build your own types. Every Python library you'll ever use is built on classes.

## The Concept
A **class** is a blueprint. An **object** is a concrete instance. The `__init__` method runs when you create an object, and `self` is the object itself.

## Code Example
```python
"""E-commerce: Product class with class and instance attributes."""

class Product:
    store_name = "PyMart"  # class attribute — shared by all products

    def __init__(self, sku: str, name: str, price: float):
        self.sku = sku          # instance attribute
        self.name = name        # instance attribute
        self.price = price      # instance attribute


laptop = Product("TECH-001", "Gaming Laptop", 1499.99)
mouse = Product("ACC-002", "Wireless Mouse", 29.99)

print(f"{laptop.name}: ${laptop.price} @ {laptop.store_name}")
print(f"{mouse.name}: ${mouse.price} @ {mouse.store_name}")
print(f"Type: {type(laptop).__name__}")

Product.store_name = "PyMart Pro"
print(f"After rename: {mouse.store_name}")
```

## 🔍 How It Works
- `class Product:` defines the blueprint
- `store_name` is a **class attribute** — one copy shared by all instances
- `self.sku` is an **instance attribute** — each Product gets its own
- `__init__` runs automatically when you call `Product(...)`
- `self` is always the first parameter and refers to the current object

## ⚠️ Common Pitfall
Modifying a mutable class attribute (like a list) through an instance affects all instances. Use instance attributes for per-object data.

## 🧠 Memory Aid
"Class is the cookie cutter, object is the cookie."

## 🏃 Try It
Create a `Customer` class with `customer_id`, `name`, and `email`. Add a class attribute `loyalty_program = "Gold"`. Create two customers and print their info.

## 🔗 Related
- [Methods](02-methods.md) — adding behavior to classes
- [Dataclasses](08-dataclasses.md) — automatic `__init__`

## ➡️ Next
[Methods](02-methods.md)
