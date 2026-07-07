# 🎯 Descriptor Nitty
<!-- ⏱️ 14 min | 🔴 Difficulty | 🧠 Applied -->

**What You'll Learn:** Implement the descriptor protocol (`__get__`, `__set__`, `__set_name__`) to build reusable validation for inventory fields.

> 💡 **TL;DR — The whole point:** Descriptors are reusable property-like objects that intercept attribute access — a `PositiveNumber` descriptor can validate every numeric field in your inventory without repeating the same setter logic.

## 🔗 Why This Matters
An `InventoryItem` has `quantity` and `price` — both must be positive numbers. Writing the same validation setter in every class is tedious. A `PositiveNumber` descriptor encapsulates the rule once and applies it to any field, with logging and type checking built in.

## The Concept
A **data descriptor** is a class that defines `__get__` and `__set__`. When a descriptor instance is a class attribute, Python routes all access through those methods. `__set_name__` is called automatically at class creation, giving the descriptor the attribute name so it can store data as `self._name` on the instance.

## Code Example
```python
"""Descriptor patterns: validation, unit conversion, access logging"""
import logging

logger = logging.getLogger(__name__)

class PositiveNumber:
    def __set_name__(self, owner, name):
        self._name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self._name, 0.0)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self._name[1:]} must be numeric, got {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"{self._name[1:]} must be positive, got {value}")
        logger.info(f"Setting {self._name[1:]} to {value}")
        setattr(obj, self._name, value)

class InventoryItem:
    quantity = PositiveNumber()
    price = PositiveNumber()

    def __init__(self, sku: str, quantity: int, price: float):
        self.sku = sku
        self.quantity = quantity
        self.price = price

item = InventoryItem("LAP-001", 10, 1499.99)
print(f"Qty: {item.quantity}, Price: ${item.price}")
try:
    item.quantity = -5
except ValueError as e:
    print(f"  Caught: {e}")
try:
    item.price = "free"
except TypeError as e:
    print(f"  Caught: {e}")
```

## 🔍 How It Works
- `__set_name__` receives the class and attribute name at definition time — stores `self._name = "_quantity"` and `"_price"`
- `__get__` returns `getattr(obj, self._name)` — the actual value lives as `obj._quantity`
- `__set__` validates type (`int`/`float`) and range (> 0) before calling `setattr(obj, self._name, value)`
- Since `PositiveNumber` defines both `__get__` and `__set__`, it's a **data descriptor** — it takes priority over instance `__dict__`
- Reuse the same descriptor class on `quantity`, `price`, or any positive numeric field

## ⚠️ Common Pitfall
If you forget `__set_name__` (or `__init_subclass__` approach) and hardcode the storage name, all descriptor instances share one name. `__set_name__` is the only way to give each instance its own attribute name automatically.

## 🧠 Memory Aid
"Descriptor = smart bouncer at the club door — `__set_name__` learns the guest list, `__set__` checks ID, `__get__` tells you who's inside."

## 🏃 Try It
Create a `NonEmptyString` descriptor that validates a field is a non-empty string. Use it on an `InventoryItem.description` field. Add `__set_name__` to store the backing attribute.

## 🔗 Related
- [Properties](06-properties.md) — properties are built-in descriptors
- [`__set_name__` / `__class_getitem__`](14-set-name-class-getitem.md) — `__set_name__` deep dive

## ➡️ Next
[`__getattr__` & `__missing__`](24-getattr-missing.md)
