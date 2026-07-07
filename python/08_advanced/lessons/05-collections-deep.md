# 🎯 Collections Deep
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Master `Counter`, `defaultdict`, `deque`, `OrderedDict`, `ChainMap`, and `UserDict` with real-world data processing.

> 💡 **TL;DR — The whole point:** The `collections` module provides specialized container types that solve common data problems more elegantly than plain dicts and lists.

## 🔗 Why This Matters
Counting product sales, grouping orders by customer, tracking recent activity, merging configuration scopes — these are everyday tasks that `collections` handles with less code and fewer bugs.

## The Concept
- `Counter` — count hashable items (like a dict of counts)
- `defaultdict` — dict with auto-generated default values
- `deque` — double-ended queue with O(1) appends/pops from either end
- `OrderedDict` — dict that remembers insertion order (Python 3.7+ dicts already do this)
- `ChainMap` — view multiple dicts as one (configuration layering)

## Code Example
```python
"""E-commerce: Collections for sales analytics, order tracking, and config."""

from collections import Counter, defaultdict, deque, ChainMap
import json


# ─── Counter: product popularity ───
sales = ["Laptop", "Mouse", "Laptop", "Keyboard", "Laptop", "Mouse", "Monitor"]
popularity = Counter(sales)
print(f"Most common: {popularity.most_common(3)}")
print(f"Laptop sales: {popularity['Laptop']}")

# ─── defaultdict: group orders by customer ───
orders = [
    ("Alice", "Laptop"), ("Bob", "Mouse"), ("Alice", "Keyboard"),
    ("Bob", "Monitor"), ("Alice", "Mouse"),
]
customer_orders: defaultdict[str, list] = defaultdict(list)
for customer, product in orders:
    customer_orders[customer].append(product)
print(f"\nAlice's orders: {customer_orders['Alice']}")

# defaultdict with int for counting
inventory = defaultdict(int)
inventory["Laptop"] += 5
inventory["Laptop"] -= 1
print(f"Laptop stock: {inventory['Laptop']}")

# ─── deque: recent activity log ───
recent_views = deque(maxlen=5)
for action in ["viewed Laptop", "added to cart", "viewed Mouse", "searched Keyboard", "viewed Monitor", "checked out"]:
    recent_views.append(action)
print(f"\nRecent activity: {list(recent_views)}")

# ─── ChainMap: layered configuration ───
defaults = {"theme": "light", "lang": "en", "page_size": 20}
user_prefs = {"theme": "dark", "page_size": 50}
session = {"lang": "fr"}

config = ChainMap(session, user_prefs, defaults)
print(f"\nConfig lookup:")
print(f"  theme: {config['theme']}")      # dark (from user_prefs)
print(f"  lang: {config['lang']}")         # fr (from session)
print(f"  page_size: {config['page_size']}")  # 50 (from user_prefs)
print(f"  debug: {config.get('debug', False)}")  # False (default)

# ChainMap mutations affect only the first mapping
config["lang"] = "de"  # updates session, not defaults!
print(f"  After mutation: session lang = {session['lang']}")
```

## 🔍 How It Works
- `Counter.most_common(n)` returns the n most common elements and their counts
- `defaultdict(factory)` calls `factory()` for missing keys — e.g., `list()`, `int()`, `set()`
- `deque(maxlen=N)` is a fixed-size buffer — pushing a new item evicts the oldest
- `ChainMap` searches mappings in order; mutations go to the first mapping
- `OrderedDict` preserves insertion order — use `move_to_end()` to reorder

## ⚠️ Common Pitfall
`defaultdict` never raises `KeyError` — missing keys get a default value. This can mask bugs. Use a regular dict if you need to know when a key is missing.

## 🧠 Memory Aid
"Counter = tally marks. defaultdict = 'if missing, make one.' deque = 'both ends, fast.' ChainMap = 'look in layers.'"

## 🏃 Try It
Analyze a log file with `Counter` to find the 10 most frequent error messages. Use `deque` to keep the last 100 log entries in memory.

## 🔗 Related
- [itertools](04-itertools.md) — iterator tools that pair well with collections
- [Context Managers Deep](06-context-managers-deep.md) — managing resource lifecycles

## ➡️ Next
[Context Managers Deep](06-context-managers-deep.md)
