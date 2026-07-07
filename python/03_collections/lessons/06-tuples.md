# 🎯 Tuples
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Create immutable sequences, unpack values into variables, use `_` for throwaway values, and use `namedtuple` for lightweight objects.

> 💡 **TL;DR — The whole point:** Tuples are immutable ordered sequences; perfect for fixed data like coordinates, RGB colors, or database records; `namedtuple` adds field names for readability.

## 🔗 Why This Matters
Lists (Lessons 03-05) are mutable — you can add, remove, and change elements. But sometimes you want a **fixed** collection that can't be modified — like the RGB values of a color (they shouldn't change mid-program) or coordinates on a Marauder's Map. Tuples guarantee immutability and can be used as dictionary keys (lists can't).

## The Concept

A tuple is an ordered, **immutable** sequence — once created, you can't change it. Write tuples with parentheses: `(1, 2, 3)`. In many contexts the parentheses are optional — commas create tuples.

**Tuple unpacking** is one of Python's most elegant features: `x, y = (1, 2)` assigns 1 to `x` and 2 to `y`. Use `_` when you don't care about a value. **Swapping** `a, b = b, a` uses tuple packing/unpacking under the hood.

`namedtuple` from the `collections` module gives you tuples with named fields — like lightweight objects with less overhead than a full class.

## Code Example

```python
"""Marauder's Map — coordinates, RGB colors, and named tuples"""

from collections import namedtuple

print("=== Creating Tuples ===")

# RGB color as a tuple (immutable by design)
crimson = (220, 20, 60)
gold = (255, 215, 0)
print(f"Crimson RGB: {crimson}")
print(f"Gold RGB: {gold}")

# Coordinates on the Marauder's Map
hogwarts_castle = (51.527, -0.130)  # (latitude, longitude)
print(f"\nHogwarts coordinates: {hogwarts_castle}")

# Single-element tuple needs trailing comma
single = (1,)
print(f"\nSingle-element tuple: {single}")

# Unpacking
print("\n=== Unpacking ===")
r, g, b = crimson
print(f"Red: {r}, Green: {g}, Blue: {b}")

# Ignore with underscore
lat, _ = hogwarts_castle
print(f"Latitude only: {lat}")

# Swapping
a, b = 1, 2
a, b = b, a
print(f"\nSwapped: a={a}, b={b}")

# Tuples as dictionary keys (lists can't do this!)
print("\n=== Tuples as Dict Keys ===")
locations = {
    (51.527, -0.130): "Hogwarts Castle",
    (51.501, -0.142): "Buckingham Palace",
    (51.508, -0.076): "The Shard",
}
for coords, place in locations.items():
    print(f"  {place}: {coords}")

# Named tuple
print("\n=== Named Tuples ===")
Wizard = namedtuple("Wizard", ["name", "house", "year"])
harry = Wizard("Harry Potter", "Gryffindor", 3)
print(f"Named tuple: {harry}")
print(f"Name: {harry.name}")
print(f"House: {harry.house}")
print(f"As regular tuple: {tuple(harry)}")
```

## 🔍 How It Works

- `(220, 20, 60)` — three integers packed into a tuple; immutable by design (colors don't change)
- `(1,)` — required trailing comma for a single-element tuple; `(1)` is just the integer 1 in parentheses
- `r, g, b = crimson` — tuple unpacking: assigns each element to a variable in order
- `lat, _ = hogwarts_castle` — `_` is a convention meaning "I don't need this value"
- `a, b = b, a` — Python evaluates the right side as a tuple `(b, a)`, then unpacks it to `a, b`
- `locations = {(51.527, -0.130): "Hogwarts Castle"}` — tuples are hashable, so they work as dict keys; lists are not hashable and raise `TypeError`
- `namedtuple("Wizard", ["name", "house", "year"])` — creates a tuple subclass with named fields; accessed as `harry.name` instead of `harry[0]`

## ⚠️ Common Pitfall

Forgetting the trailing comma in a single-element tuple: `(1)` is an integer, not a tuple. `(1,)` is a tuple. Also, trying to modify a tuple: `crimson[0] = 230` raises `TypeError`. If you need to change values, use a list instead. And remember: `namedtuple` fields are accessed by name, but the underlying storage is still a tuple — it's immutable.

## 🧠 Memory Aid

**"Tuples are the fixed-point enchantment on the Marauder's Map — once the coordinates are set, they can't be changed by any spell. Lists are the moving staircases of Hogwarts — they change constantly."**

## 🏃 Try It

Run the code file:
```bash
python code/03-06-tuples.py
```
Then create a `namedtuple` called `Spell` with fields for name, incantation, and level, and create a few spell instances.

## 🔗 Related

- [Collections Module](10-collections-module.md) — `namedtuple` and other specialized containers
- [Lists I](03-lists-i.md) — tuples vs lists: immutable vs mutable

## ➡️ Next

→ [07 — Dictionaries](07-dictionaries.md)
