# 🎯 Methods
<!-- ⏱️ 12 min read | 🟢 Core | 🧠 Core -->

**What You'll Learn:** Instance methods, `@classmethod`, and `@staticmethod` — and when to use each in a real-world app.

> 💡 **TL;DR — The whole point:** Instance methods work on object data, class methods work on the class itself, static methods are just functions parked inside a class.

## 🔗 Why This Matters
Methods give objects behavior. Choosing the right type makes your API cleaner and more Pythonic — like having `Order.from_cart()` instead of a clunky helper function.

## The Concept
- **Instance methods** take `self` and read/write object state
- **Class methods** take `cls` and are used for alternative constructors
- **Static methods** take neither — utility functions namespaced in the class

## Code Example
```python
"""E-commerce: Order class with instance, class, and static methods."""

class Order:
    tax_rate = 0.08  # class attribute

    def __init__(self, items: list[tuple[str, float]]):
        self.items = items  # list of (name, price)

    def subtotal(self) -> float:
        """Instance method — computes total from instance data."""
        return sum(price for _, price in self.items)

    def total(self) -> float:
        """Instance method — applies tax."""
        return self.subtotal() * (1 + self.tax_rate)

    @classmethod
    def from_cart(cls, cart_items: list[str], prices: dict[str, float]):
        """Class method — alternative constructor from a cart."""
        items = [(item, prices[item]) for item in cart_items if item in prices]
        return cls(items)

    @staticmethod
    def is_valid_item(name: str, price: float) -> bool:
        """Static method — validation utility."""
        return bool(name) and price > 0


order = Order([("Laptop", 1200), ("Mouse", 25)])
print(f"Subtotal: ${order.subtotal():.2f}")
print(f"Total: ${order.total():.2f}")

cart_order = Order.from_cart(["Laptop", "Mouse", "Keyboard"], {"Laptop": 1200, "Mouse": 25, "Keyboard": 80})
print(f"Cart total: ${cart_order.total():.2f}")

print(f"Valid? {Order.is_valid_item('Headphones', 50)}")
```

## 🔍 How It Works
- `self` is the instance — Python passes it automatically
- `cls` is the class — also passed automatically to `@classmethod`
- `@classmethod` can be called on the class (`Order.from_cart(...)`) or an instance
- `@staticmethod` works like a plain function but lives in the class namespace

## ⚠️ Common Pitfall
Using `self` in a `@staticmethod` — it won't error, but it'll be the first argument, not the instance. Use instance methods when you need `self`.

## 🧠 Memory Aid
"Instance = I (self), Class = we (cls), Static = just a function in a trench coat."

## 🏃 Try It
Add a `@classmethod` called `from_csv_row` to `Order` that takes a CSV string like `"Laptop:1200,Mouse:25"` and returns an `Order`.

## 🔗 Related
- [Classes & Objects](01-classes-objects.md) — `self` and `__init__`
- [Inheritance](03-inheritance.md) — method overriding

## ➡️ Next
[Inheritance](03-inheritance.md)
