# 🎯 Sets
<!-- ⏱️ 8 min read | 🟡 Medium | 🧠 Core -->

**What You'll Learn:** Store unique elements, perform set math (union, intersection, difference), test membership at lightning speed, and meet `frozenset`.

> 💡 **TL;DR — The whole point:** Sets store unique items (no duplicates); `|` = union, `&` = intersection, `-` = difference; membership testing is O(1) — instant, even with millions of items.

## 🔗 Why This Matters
Dictionaries (Lesson 07) store key-value pairs. Sets are like dictionary keys without the values — unordered, unique, and blazingly fast for membership checks. Use sets for deduplication, finding common friends between wizards, tracking unique visitors to a website, or analyzing which tags overlap between blog posts.

## The Concept

A set is an unordered collection of **unique** elements. Create one with `{}` or `set()`. Warning: `{}` creates an empty **dict**, not a set — use `set()` for an empty set.

Sets shine at **deduplication** (remove duplicates from a list) and **membership testing** (O(1) average vs O(n) for lists).

Set operations follow math:
- `|` **Union** — all elements from both sets
- `&` **Intersection** — elements in both
- `-` **Difference** — elements in first but not second
- `^` **Symmetric difference** — elements in either, but not both

`frozenset` is an immutable, hashable set — usable as a dictionary key.

## Code Example

```python
"""Hogwarts class rosters — set operations for student analysis"""

# Students in each class
potions = {"Harry", "Ron", "Hermione", "Draco", "Neville", "Seamus"}
charms = {"Ron", "Hermione", "Luna", "Neville", "Ginny", "Harry"}
defense = {"Harry", "Hermione", "Ron", "Draco", "Luna", "Cedric"}

print("=== Class Rosters ===")
print(f"Potions ({len(potions)}): {potions}")
print(f"Charms ({len(charms)}): {charms}")
print(f"Defense ({len(defense)}): {defense}")

# Deduplication — remove duplicates from a list
all_students_list = ["Harry", "Ron", "Harry", "Hermione", "Ron", "Luna"]
unique_students = set(all_students_list)
print(f"\n=== Deduplication ===")
print(f"  List with duplicates: {all_students_list}")
print(f"  Unique students: {unique_students}")

# Union — all students across classes
all_enrolled = potions | charms | defense
print(f"\n=== Union (all enrolled) ===")
print(f"  Total unique students: {len(all_enrolled)}")
print(f"  {sorted(all_enrolled)}")

# Intersection — students in both Potions and Charms
both_potions_charms = potions & charms
print(f"\n=== Intersection (Potions ∩ Charms) ===")
print(f"  Students in both: {both_potions_charms}")

# Difference — students in Potions but not Defense
only_potions = potions - defense
print(f"\n=== Difference (Potions − Defense) ===")
print(f"  Only in Potions: {only_potions}")

# Symmetric difference — in Potions or Charms but not both
exclusive = potions ^ charms
print(f"\n=== Symmetric Difference ===")
print(f"  In one class only: {exclusive}")

# Membership testing — fast!
print("\n=== Membership ===")
print(f"  Is Harry in Defense? {'Harry' in defense}")
print(f"  Is Malfoy in Charms? {'Draco' in charms}")

# Frozenset — immutable set
print("\n=== Frozenset ===")
fs = frozenset(["Harry", "Ron", "Hermione"])
print(f"  Frozenset: {fs}")
print(f"  Hashable: {hash(fs) is not None}")
```

## 🔍 How It Works

- `{"Harry", "Ron", "Hermione"}` — set literal with curly braces, no colons (unlike dicts)
- `set(all_students_list)` — creates a set from a list, automatically removing duplicates
- `potions | charms` — union: all students in either class (the `|` operator)
- `potions & charms` — intersection: students taking both classes (`&` operator)
- `potions - defense` — difference: students in Potions but not Defense (`-` operator)
- `potions ^ charms` — symmetric difference: in exactly one of the two (`^` operator)
- `"Harry" in defense` — O(1) membership test, regardless of set size
- `frozenset([...])` — immutable, hashable set; can be used as a dict key

## ⚠️ Common Pitfall

Using `{}` for an empty set — this creates an empty **dict**. Use `set()` for an empty set. Also, sets are **unordered** — don't rely on element position. And sets can only contain **hashable** (immutable) elements: you can have a set of tuples but not a set of lists.

## 🧠 Memory Aid

**"Sets are like the Sorting Hat's list of students — each wizard appears only once (no duplicates), and the Hat instantly knows if a name is on the list (instant membership check)."**

## 🏃 Try It

Run the code file:
```bash
python code/03-08-sets.py
```
Then create three sets of Quidditch team members and find players who play on more than one team using intersection.

## 🔗 Related

- [Dictionaries](07-dictionaries.md) — `{}` overlap in syntax; sets are like keys without values
- [Lists II](04-lists-ii.md) — membership: O(1) in sets vs O(n) in lists

## ➡️ Next

→ [09 — Nested Data](09-nested-data.md)
