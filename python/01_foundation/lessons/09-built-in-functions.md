# 🎯 Built-in Functions
<!-- ⏱️ 12 min | 🟢 Core | 🧠 Core -->

**What You'll Learn:** Use Python's essential built-in functions — `len()`, `type()`, `range()`, `zip()`, `map()`, `filter()`, `sorted()`, `enumerate()`, `any()`, `all()`, `sum()`, `min()`, `max()`, `abs()`, `round()`, `isinstance()`, `id()`, `repr()`, `hash()`.

> 💡 **TL;DR — The whole point:** Built-in functions are Python's "batteries included" — they handle 80% of data-processing tasks without writing custom logic.

## 🔗 Why This Matters

Spreadsheets have SUM, AVERAGE, MIN, MAX — and so does Python, right out of the box. In real-world code you'll constantly sum totals, find the best/worst values, pair up lists, and filter results. Built-in functions turn what would be a 10-line loop into a single readable call.

## The Concept

Python ships with ~70 built-in functions available without any `import`. They split into categories: **math** (`sum`, `min`, `max`, `abs`, `round`), **iteration** (`zip`, `enumerate`, `sorted`, `reversed`, `range`), **transformation** (`map`, `filter`), **metadata** (`len`, `type`, `id`, `repr`, `hash`), and **boolean checks** (`any`, `all`, `isinstance`). Learn these and you'll write less code, with fewer bugs.

## Code Example

```python
"""Built-in functions: data analysis toolkit — weekly sales"""

products = ["Widget", "Gadget", "Doohickey", "Thingy"]
prices = [12.99, 24.50, 5.75, 8.50]
weekly_sales = [34, 28, 51, 43]

# --- METADATA ---
print("=== Data Overview ===")
print(f"Products: {len(products)} items, type={type(prices)}, id={id(products)}")
print(f"repr(sales)={repr(weekly_sales)}, hash('Widget')={hash('Widget')}")

# --- MATH ---
print("\n=== Sales Summary ===")
total, lo, hi = sum(weekly_sales), min(weekly_sales), max(weekly_sales)
print(f"Total: {total} | Min: {lo} | Max: {hi}")
print(f"Avg price: ${round(sum(prices)/len(prices), 2)}")
print(f"Spread: ${round(abs(max(prices)-min(prices)), 2)}")

# --- SORTING & ORDERING ---
print("\n=== Rankings (high to low) ===")
for rank, (prod, sales) in enumerate(
    sorted(zip(products, weekly_sales), key=lambda x: x[1], reverse=True), 1
):
    print(f"  #{rank}: {prod} ({sales})")

print("Products reversed:", list(reversed(products)))
for i in range(len(products)):
    print(f"  range({i}): {products[i]}")

# --- TRANSFORMATION ---
print("\n=== Data Transformation ===")
price_per_unit = list(map(lambda p, s: round(p / s, 2), prices, weekly_sales))
print(f"Price per unit: {price_per_unit}")

high_volume = list(filter(lambda s: s > 30, weekly_sales))
print(f"Weeks >30 sold: {high_volume}")

# --- BOOLEAN CHECKS ---
print("\n=== Boolean Checks ===")
print(f"Any product >$20? {any(p > 20 for p in prices)}")
print(f"All < $50? {all(p < 50 for p in prices)}")
print(f"prices[0] is float? {isinstance(prices[0], float)}")
```

## 🔍 How It Works

- `len(products)` — counts items in the list (works on strings, dicts, sets too)
- `type(prices)` — returns the type object (`<class 'list'>`)
- `id(products)` — unique memory address of the list object
- `repr(weekly_sales)` — unambiguous string representation (useful for debugging)
- `hash('Widget')` — integer hash for dictionary/set lookups
- `sum()` / `min()` / `max()` — aggregate math in a single call
- `round(..., 2)` — rounds to 2 decimal places (uses banker's rounding)
- `abs(x - y)` — absolute difference (always non-negative)
- `sorted(..., key=..., reverse=True)` — returns a **new** sorted list (original unchanged)
- `enumerate(..., 1)` — pairs each item with a rank starting at 1
- `zip(list_a, list_b)` — pairs items from two lists into tuples
- `reversed(products)` — returns an iterator; wrap in `list()` to materialize
- `range(len(products))` — generates indices 0, 1, 2, ... n-1
- `map(lambda, *iterables)` — applies the function to each element; returns iterator
- `filter(lambda, iterable)` — keeps only elements where the lambda is truthy
- `any(genexpr)` — `True` if **at least one** element is truthy
- `all(genexpr)` — `True` if **every** element is truthy
- `isinstance(value, type)` — checks type safely (handles inheritance unlike `type() ==`)

## ⚠️ Common Pitfall

`round()` uses **banker's rounding**: `round(2.5)` gives `2` (not `3`) because it rounds .5 to the nearest even number. `sorted()` returns a **new list** — it doesn't modify the original (use `list.sort()` for in-place). `map()` and `filter()` return **iterators**, not lists — wrap in `list()` if you need to see or store the results.

## 🧠 Memory Aid

**"Built-in functions are Python's Swiss Army knife — each blade handles one common data task so you don't have to build it from scratch."**

## 🏃 Try It

Run the code file:
```bash
python code/01-09-built-in-functions.py
```
Then add a fifth product `"Gizmo"` with price `19.99` and weekly sales `37` to every list. Re-run and see how the average, rankings, and boolean checks change.

## 🔗 Related

- [Data Types](03-data-types.md) — the types you pass to these functions
- [Operators](04-operators.md) — comparison operators used inside `map`/`filter` lambdas

## ➡️ Next

→ [Phase 02 — Conditionals](../../02_control_flow/lessons/01-conditionals.md)
