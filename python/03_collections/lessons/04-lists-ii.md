# 🎯 Lists II: Methods & Copying
<!-- ⏱️ 9 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Remove elements, sort and reverse lists, find items, and understand how references and copies work.

> 💡 **TL;DR — The whole point:** `.remove(x)` deletes by value, `.pop()` deletes by index and returns it, `.sort()` orders in place, and `=` creates a reference (not a copy) — use `.copy()` for an independent duplicate.

## 🔗 Why This Matters
You can build lists (Lesson 03). Now learn to manage them — removing expired potion ingredients, sorting a leaderboard, and the critical skill of copying vs referencing. The reference trap is one of Python's most common bugs: changing one list unexpectedly changes another.

## The Concept

Lists have a full suite of management methods:

- **Removal**: `.remove(x)` deletes the first match by value; `.pop(i)` removes and returns item at index `i` (default last); `.clear()` empties the list
- **Ordering**: `.sort()` sorts in place; `.reverse()` reverses in place; `sorted()` and `reversed()` return new versions without modifying the original
- **Search**: `.index(x)` returns the first index of `x`; `.count(x)` counts occurrences
- **Copying**: `.copy()`, `list()`, and `[:]` create **shallow copies** (independent at the top level, but nested objects are shared)

**Critical**: Assigning a list to another variable (`ref = original`) doesn't copy it — both names point to the **same object**. Modifying one affects the other.

## Code Example

```python
"""Inventory management — tracking potion ingredients at Hogwarts"""

# Starting inventory
ingredients = ["Dittany", "Bezoar", "Mandrake Root", "Bezoar", "Wolfsbane"]
print(f"Starting inventory: {ingredients}")

# Remove by value (first occurrence only)
ingredients.remove("Bezoar")
print(f"\nAfter remove('Bezoar'): {ingredients}")

# Pop by index (removes and returns)
last = ingredients.pop()
print(f"Popped last: '{last}' | Remaining: {ingredients}")
second = ingredients.pop(1)
print(f"Popped index 1: '{second}' | Remaining: {ingredients}")

# Sorting
scores = [450, 320, 890, 150, 670]
print(f"\nUnsorted scores: {scores}")
scores.sort()
print(f"Sorted ascending: {scores}")
scores.sort(reverse=True)
print(f"Sorted descending: {scores}")

# Reverse
scores.reverse()
print(f"After reverse: {scores}")

# Search and count
items = ["wand", "robe", "wand", "broom", "wand"]
print(f"\nItems: {items}")
print(f"Index of 'broom': {items.index('broom')}")
print(f"Count of 'wand': {items.count('wand')}")

# Reference vs Copy — the critical difference
print("\n=== Reference vs Copy ===")
original = [1, 2, 3, [4, 5]]
ref = original          # same object!
shallow = original.copy()  # independent top level

original[0] = 99
original[3].append(6)  # nested list is shared

print(f"Original: {original}")
print(f"Reference (changed!): {ref}")
print(f"Shallow copy (top level safe, nested shared): {shallow}")

# Clear
original.clear()
print(f"\nAfter clear: {original}")
```

## 🔍 How It Works

- `.remove("Bezoar")` — scans from the start, removes the first element matching "Bezoar"; raises `ValueError` if not found
- `.pop()` — removes and returns the last element (O(1)); `.pop(1)` removes and returns the element at index 1 (O(n) — shifts elements)
- `.sort()` — sorts in place (modifies the original list); `sorted()` returns a new sorted list without changing the original
- `ref = original` — both variables point to the same list in memory; mutating one mutates the other
- `.copy()` creates a **shallow copy** — the top-level list is independent, but nested objects within it are still shared
- `.clear()` — removes all elements, leaving an empty list

## ⚠️ Common Pitfall

Accidentally aliasing a list with `=` when you meant to copy. `new_list = old_list` doesn't create a new list — it creates a new name for the same list. Use `.copy()`, `list()`, or slicing `[:]` for a shallow copy. For nested lists (like a list of lists), you need `import copy; copy.deepcopy()`.

## 🧠 Memory Aid

**"'=' is like a Horcrux — two names for the same soul. Changing one changes the other. '.copy()' is a Patronus — a perfect copy that lives independently."** When you use `=`, both variables share the same underlying object; `.copy()` creates a new independent object.

## 🏃 Try It

Run the code file:
```bash
python code/03-04-lists-ii.py
```
Then create a list of Quidditch scores, sort them, pop the highest, and verify your reference vs copy understanding.

## 🔗 Related

- [Lists I](03-lists-i.md) — creation, indexing, append/insert/extend
- [Nested Data](09-nested-data.md) — deep copying with nested structures

## ➡️ Next

→ [05 — List Comprehensions](05-list-comprehensions.md)
