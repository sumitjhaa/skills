# 🎯 Encapsulation
<!-- ⏱️ 11 min read | 🟡 Core | 🧠 Core -->

**What You'll Learn:** Protect internal state with `_` convention and `__` name mangling using a gaming inventory system.

> 💡 **TL;DR — The whole point:** Encapsulation hides implementation details. In Python, it's a convention (not enforcement) that says "this is internal, don't touch."

## 🔗 Why This Matters
When you build a `Inventory` class, you want users to call `inventory.add_item()` — not monkey with `inventory._items` directly. Encapsulation communicates which parts are safe to use and which are implementation details.

## The Concept
- **Public**: `self.name` — anyone can access
- **Protected** (convention): `self._name` — "please don't touch this directly"
- **Private** (name mangling): `self.__name` — Python renames to `_ClassName__name`

## Code Example
```python
"""Gaming: Inventory system with encapsulated internals."""

class Inventory:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self._items: list[dict] = []       # protected — internal storage
        self.__gold = 0                     # name mangled

    def add_item(self, name: str, quantity: int = 1) -> bool:
        if len(self._items) >= self.capacity:
            return False
        self._items.append({"name": name, "qty": quantity})
        return True

    def remove_item(self, name: str) -> bool:
        for i, item in enumerate(self._items):
            if item["name"] == name:
                self._items.pop(i)
                return True
        return False

    @property
    def gold(self) -> int:
        return self.__gold

    def add_gold(self, amount: int) -> None:
        if amount > 0:
            self.__gold += amount

    def spend_gold(self, amount: int) -> bool:
        if 0 < amount <= self.__gold:
            self.__gold -= amount
            return True
        return False

    @property
    def item_count(self) -> int:
        return len(self._items)

    @property
    def is_full(self) -> bool:
        return len(self._items) >= self.capacity


inv = Inventory(capacity=5)
inv.add_item("Health Potion", 3)
inv.add_item("Mana Potion", 2)

print(f"Items: {inv.item_count}")
print(f"Gold: {inv.gold}")
inv.add_gold(100)
inv.spend_gold(30)
print(f"Gold after spending: {inv.gold}")

# These "work" but violate encapsulation:
print(f"Protected access (don't do this): {inv._items}")

try:
    print(inv.__gold)  # AttributeError!
except AttributeError:
    print("Cannot access __gold directly")
    print(f"But can via: {inv._Inventory__gold}")  # name mangled form
```

## 🔍 How It Works
- `_items` says "I'm internal" — linters will warn if you access it externally
- `__gold` becomes `_Inventory__gold` internally (name mangling)
- Name mangling prevents accidental access but isn't true privacy
- Properties and methods provide the "public API" — safe, documented, intentional

## ⚠️ Common Pitfall
Using `__double_underscore` for every internal attribute. Use `_single` for most cases; `__` is rare and mostly for avoiding name collisions in inheritance.

## 🧠 Memory Aid
"_ = 'please don't', __ = 'really please don't'. Python trusts you."

## 🏃 Try It
Add a `_calculate_weight()` protected method and a `total_weight` property to `Inventory`. Add a `__max_weight` private attribute with validation.

## 🔗 Related
- [Properties](06-properties.md) — controlled access via `@property`
- [Dataclasses](08-dataclasses.md) — `field(repr=False)` for hiding fields

## ➡️ Next
[Dataclasses](08-dataclasses.md)
