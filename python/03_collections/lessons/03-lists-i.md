# 🎯 Lists I: Creation, Indexing, Mutability
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Create lists, access elements by index, modify them in place, and grow lists with `append`, `insert`, and `extend`.

> 💡 **TL;DR — The whole point:** Lists are ordered, mutable sequences; use `[]` to create, `list[index]` to access/assign, `.append()` to add one item, `.extend()` to add many.

## 🔗 Why This Matters
Strings (Lessons 01-02) are sequences of characters. Lists are sequences of *anything* — and they're **mutable**. You can change them, grow them, shrink them. Think of a shopping cart at Honeydukes: you start empty, `.append()` a Chocolate Frog, `.insert()` a Fizzing Whizbee at the top, `.extend()` with a bunch of Bertie Bott's Every Flavour Beans.

## The Concept

A list is Python's workhorse collection — ordered, mutable, and flexible. Create one with square brackets: `[1, 2, 3]`. Unlike strings, you can change elements in place (`my_list[0] = 99`). Lists can hold any mix of types — integers, strings, even other lists.

Indexing and slicing work exactly like strings (both are **sequences**). The key difference is mutability: you can modify a list after creation. `.append()` adds one element to the end, `.insert()` places an element at any index, and `.extend()` merges another iterable into the list.

## Code Example

```python
"""Hogwarts shopping cart — list operations for wizard supplies"""

# Start with an empty cart
cart = []
print(f"Empty cart: {cart}")

# Append — add items one at a time
cart.append("Wand")
cart.append("Cauldron")
cart.append("Broomstick")
print(f"\nAfter append: {cart}")

# Insert — add at a specific position
cart.insert(1, "Robes")  # After Wand
print(f"After insert(1, 'Robes'): {cart}")

# Indexing — access and modify
print(f"\nFirst item: {cart[0]}")
print(f"Last item: {cart[-1]}")
cart[0] = "Holly Wand"  # Lists are mutable!
print(f"After modifying first item: {cart}")

# Slicing works like strings
print(f"\nFirst 3 items: {cart[:3]}")
print(f"Every other item: {cart[::2]}")

# Extend — add multiple items at once
more_items = ["Potion Kit", "Crystal Ball", "Dragon Hide Gloves"]
cart.extend(more_items)
print(f"\nAfter extend: {cart}")

# Lists can hold mixed types
mixed = ["Harry", 17, True, 9.75, None]
print(f"\nMixed list: {mixed}")

# Nested list — a list inside a list
wizards = [["Harry", "Gryffindor"], ["Draco", "Slytherin"]]
print(f"\nNested list: {wizards}")
print(f"First wizard: {wizards[0]}")
print(f"First wizard's name: {wizards[0][0]}")
```

## 🔍 How It Works

- `cart = []` — empty list; `list()` also works but `[]` is preferred
- `cart.append("Wand")` — adds "Wand" at the end; O(1) operation
- `cart.insert(1, "Robes")` — inserts at index 1, shifting everything else right; O(n)
- `cart[0] = "Holly Wand"` — **mutation**: replaces the element at index 0 without creating a new list
- `cart[:3]` — slice returns a new list containing first 3 elements
- `cart.extend(more_items)` — appends each element from `more_items`; equivalent to `for item in more_items: cart.append(item)`
- `wizards[0][0]` — first `[0]` gets the first sublist, second `[0]` gets its first element

## ⚠️ Common Pitfall

Confusing `.append()` with `.extend()`. `cart.append([1, 2])` adds the list `[1, 2]` as a **single element**. `cart.extend([1, 2])` adds 1 and 2 as **separate elements**. Also, slicing with `list[start:stop]` creates a new list — modifying the slice doesn't affect the original.

## 🧠 Memory Aid

**"Append adds one item (one delivery owl). Extend adds many items (a flock of owls). Insert is like squeezing into a packed Hogwarts Express compartment — you pick the spot and everyone shuffles to make room."**

## 🏃 Try It

Run the code file:
```bash
python code/03-03-lists-i.py
```
Then create a list of your favorite spells and use `append()`, `insert()`, and slicing to modify it.

## 🔗 Related

- [Strings I](01-strings-i.md) — same indexing/slicing rules apply
- [Lists II](04-lists-ii.md) — removal, sorting, copying, and references

## ➡️ Next

→ [04 — Lists II: Methods & Copying](04-lists-ii.md)
