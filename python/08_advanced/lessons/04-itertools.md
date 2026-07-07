# 🎯 itertools
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Master `itertools` — infinite iterators, combinatorics, grouping, accumulating, and slicing iterators.

> 💡 **TL;DR — The whole point:** `itertools` is a toolbox for building iterator pipelines — chain, cycle, product, permutations, groupby, accumulate, and more.

## 🔗 Why This Matters
Data processing, A/B testing combinations, analyzing sales trends, generating test data — `itertools` handles these efficiently without filling memory with intermediate lists.

## The Concept
All `itertools` functions return iterators (lazy). They compose like lego blocks: chain iterables, cycle values, compute combinations, group by keys, accumulate running totals.

## Code Example
```python
"""E-commerce: itertools for inventory analysis, recommendations, and pricing."""

from itertools import (
    chain, cycle, islice, product, permutations,
    combinations, groupby, accumulate, count, repeat,
)
from typing import Any


products = {"Laptop": 1200, "Mouse": 25, "Keyboard": 80, "Monitor": 400, "Webcam": 60}

# ─── chain: combine multiple iterables ───
categories = {
    "Electronics": ["Laptop", "Monitor"],
    "Accessories": ["Mouse", "Keyboard", "Webcam"],
}
all_items = list(chain.from_iterable(categories.values()))
print(f"All items: {all_items}")

# ─── accumulate: running total of sales ───
daily_sales = [1200, 800, 1500, 900, 2000]
running_total = list(accumulate(daily_sales))
print(f"Running total: {running_total}")

# ─── product: build all bundle combinations ───
bundle_base = ["Laptop", "Desktop"]
bundle_addons = ["Mouse", "Keyboard"]
bundles = list(product(bundle_base, bundle_addons))
print(f"Bundles: {bundles}")

# ─── permutations / combinations: pricing strategies ───
price_tiers = [19.99, 29.99, 49.99]
combo_prices = list(combinations(price_tiers, 2))
print(f"Price combos: {combo_prices}")

# ─── groupby: group products by price range ───
def price_range(price: float) -> str:
    return "budget" if price < 50 else "mid" if price < 500 else "premium"

sorted_prods = sorted(products.items(), key=lambda x: price_range(x[1]))
for group, items in groupby(sorted_prods, key=lambda x: price_range(x[1])):
    print(f"  {group}: {[name for name, _ in items]}")

# ─── islice + cycle: repeat recommendation carousel ───
recs = cycle(["Laptop", "Mouse", "Keyboard"])
print(f"First 5 recs: {list(islice(recs, 5))}")

# ─── count: auto-incrementing IDs ───
ids = list(islice(count(start=1000, step=2), 5))
print(f"Generated IDs: {ids}")
```

## 🔍 How It Works
- `chain(*iterables)` — concatenate iterables; `chain.from_iterable()` for nested lists
- `accumulate(iterable, func=operator.add)` — running totals with any binary function
- `product(*iterables, repeat=1)` — Cartesian product (nested loops)
- `permutations(iterable, r)` — all orderings; `combinations(iterable, r)` — all subsets
- `groupby(iterable, key)` — group consecutive items by key (must be sorted!)
- `islice(iterable, stop)` / `islice(iterable, start, stop, step)` — lazy slicing
- `cycle(iterable)` — infinite loop; `count(start, step)` — infinite counter
- All are lazy — they produce values on demand

## ⚠️ Common Pitfall
`groupby` only groups *consecutive* items with the same key. If your data isn't sorted by the grouping key, you'll get separate groups for the same key value. Always sort first.

## 🧠 Memory Aid
"itertools = LEGO for iterators. `product` = nested for-loops. `groupby` = sort-then-group. `chain` = flatten. `accumulate` = running total."

## 🏃 Try It
Use `itertools` to generate all possible pizza topping combinations from `["cheese", "pepperoni", "mushrooms", "olives"]`. Start with 2-topping combinations and work up to all-topping.

## 🔗 Related
- [Generators Deep](02-generators-deep.md) — generators power itertools
- [Collections Deep](05-collections-deep.md) — `Counter`, `defaultdict`

## ➡️ Next
[Collections Deep](05-collections-deep.md)
