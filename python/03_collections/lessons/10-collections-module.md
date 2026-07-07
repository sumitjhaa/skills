# 🎯 Collections Module
<!-- ⏱️ 10 min read | 🔴 Advanced | 🧠 Applied (Python 3.10+) -->

**What You'll Learn:** Supercharge your collections with `defaultdict`, `Counter`, `deque`, `OrderedDict`, and `ChainMap` from the standard library.

> 💡 **TL;DR — The whole point:** `defaultdict` auto-creates missing keys, `Counter` tallies items, `deque` gives fast appends/pops from both ends, `OrderedDict` tracks insertion order with extra methods, and `ChainMap` merges multiple dicts into one view.

## 🔗 Why This Matters
Regular dicts and lists (Lessons 01-09) handle most cases. But the `collections` module handles the *edge* cases more elegantly — counting spell frequencies without manual tallying, tracking URL visit history with `deque`, merging configuration layers with `ChainMap`, or auto-grouping students by house with `defaultdict`.

## The Concept

The `collections` module provides specialized container types:

- **`defaultdict`** — like a dict but calls a factory function for missing keys. `defaultdict(list)` auto-creates an empty list when you access a missing key. Perfect for grouping items.
- **`Counter`** — a dict subclass for counting hashable items. `.most_common(n)` returns the top n items. Ideal for frequency analysis.
- **`deque`** (double-ended queue) — O(1) appends and pops from either end. `deque(maxlen=N)` keeps only the N most recent items — perfect for URL history or recent activity logs.
- **`OrderedDict`** — remembers insertion order (regular dicts do this since Python 3.7, but `OrderedDict` has `.move_to_end()` for explicit reordering).
- **`ChainMap`** — groups multiple dicts into a single view. Lookups search left-to-right. Perfect for layered configuration (defaults + overrides).

## Code Example

```python
"""Hogwarts administration — collections module in action"""

from collections import defaultdict, Counter, deque, OrderedDict, ChainMap

print("=== defaultdict — Auto-group Students by House ===")
students = [
    ("Harry", "Gryffindor"), ("Ron", "Gryffindor"),
    ("Draco", "Slytherin"), ("Luna", "Ravenclaw"),
    ("Hermione", "Gryffindor"), ("Cedric", "Hufflepuff"),
]
houses = defaultdict(list)
for name, house in students:
    houses[house].append(name)
for house, members in sorted(houses.items()):
    print(f"  {house}: {', '.join(members)}")

print("\n=== Counter — Spell Frequency ===")
spells = [
    "Expelliarmus", "Lumos", "Expelliarmus", "Accio",
    "Lumos", "Expelliarmus", "Protego", "Accio", "Lumos",
]
spell_counts = Counter(spells)
print(f"  All counts: {dict(spell_counts)}")
print(f"  Top 3: {spell_counts.most_common(3)}")
print(f"  Total spells cast: {sum(spell_counts.values())}")

print("\n=== deque — Recent Spell History ===")
recent = deque(maxlen=3)
for spell in ["Accio", "Lumos", "Expelliarmus", "Protego", "Stupefy"]:
    recent.append(spell)
    print(f"  Cast {spell:15} | Recent: {list(recent)}")

print("\n=== OrderedDict — Priority Queue ===")
tasks = OrderedDict()
tasks["Find Horcruxes"] = "Critical"
tasks["Practice Occlumency"] = "High"
tasks["Brew Polyjuice"] = "Medium"
tasks["Write Potions Essay"] = "Low"
tasks.move_to_end("Write Potions Essay", last=False)  # Move to front
for task, priority in tasks.items():
    print(f"  [{priority:8}] {task}")

print("\n=== ChainMap — Configuration Layers ===")
defaults = {"theme": "dark", "lang": "en", "font_size": 14}
user_prefs = {"lang": "fr", "font_size": 16}
session = {"lang": "de"}
config = ChainMap(session, user_prefs, defaults)
print(f"  Theme: {config['theme']}")        # from defaults
print(f"  Language: {config['lang']}")       # from session (first match)
print(f"  Font size: {config['font_size']}") # from user_prefs
```

## 🔍 How It Works

- `defaultdict(list)` — when you access `houses["Hufflepuff"]` and it doesn't exist, the dict automatically calls `list()` → creates an empty list, then appends the student name
- `Counter(spells)` — iterates through all spells, counting occurrences. `.most_common(3)` returns the 3 most frequent
- `deque(maxlen=3)` — when full, adding a new item on one end automatically removes the oldest item from the other end. Perfect for "recent items" tracking
- `OrderedDict().move_to_end(task, last=False)` — moves a key to the front (last=False) or end (last=True) of the ordered dict
- `ChainMap(session, user_prefs, defaults)` — lookups check `session` first, then `user_prefs`, then `defaults`. Mutations only affect the first dict

## ⚠️ Common Pitfall

Forgetting that `defaultdict`'s factory function is called with no arguments — `defaultdict(list)` works, but `defaultdict([])` crashes because `[]` isn't callable. Also, `Counter` only works with **hashable** items (like strings and numbers, not lists). And `ChainMap` mutations (assignments, deletions) only affect the *first* dict in the chain, not the merged view.

## 🧠 Memory Aid

**"Defaultdict is the Room of Requirement — you ask for a room, and it creates one for you. Counter is the house points counter — it tallies every spell cast. Deque is a Time-Turner — you can add to either end and only remember the last few moments."**

## 🏃 Try It

Run the code file:
```bash
python code/03-10-collections-module.py
```
Then use `Counter` to count the letters in your name and print the top 3 most common letters.

## 🔗 Related

- [Dictionaries](07-dictionaries.md) — the foundation `defaultdict`, `Counter`, and `OrderedDict` build on
- [Tuples](06-tuples.md) — `namedtuple` is also in collections

## ➡️ Next

→ Back to [Phase Overview](../README.md) — you've completed Phase 03!
