# 🎯 itertools Recipes: batched, pairwise, islice Pagination
<!-- ⏱️ 12 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `batched`, `pairwise`, `islice`, `zip_longest`, `compress`, and `chain.from_iterable` for data processing pipelines.

> 💡 **TL;DR — The whole point:** `itertools` recipes give you memory-efficient, composable tools — batch records, compute consecutive deltas, paginate without slicing lists, align uneven data, and flatten nested structures.

## 🔗 Why This Matters
Bulk database inserts need batching. Stock price analysis needs consecutive differences. API pagination should be memory-efficient. Importing messy CSV data often has uneven columns.

## The Concept
`batched` (3.12+) splits an iterable into fixed-size tuples. `pairwise` (3.10+) yields consecutive overlapping pairs. `islice` lazily slices iterators without building lists. `zip_longest` zips uneven iterables with a fill value. `compress` filters by a boolean mask. `chain.from_iterable` flattens nested iterables.

## Code Example
```python
"""itertools recipes: batching, pairs, pagination — data processing pipelines"""
from itertools import batched, pairwise, zip_longest, islice, chain, compress, count

# batched: bulk database inserts — 100 records at a time (3.12+)
users = [f"user_{i}" for i in range(10)]
for i, batch in enumerate(batched(users, 3), 1):
    print(f"  Batch {i}: {list(batch)}")

# pairwise: consecutive differences for stock price / temperature deltas (3.10+)
prices = [100, 102, 98, 105, 107]
changes = [b - a for a, b in pairwise(prices)]
print(f"  Price changes: {changes}")

# islice: memory-efficient pagination (no giant list built)
def paginate(items, page_size=3, page=1):
    start = (page - 1) * page_size
    return list(islice(items, start, start + page_size))
print(f"  Page 2 of 100: {paginate(range(100), 3, 2)}")

# zip_longest: align uneven sequences with a fill value
headers = ["name", "age", "email", "phone"]
values = ["Alice", 30, "alice@x.com"]
for h, v in zip_longest(headers, values, fillvalue="N/A"):
    print(f"  {h}: {v}")

# compress: filter one iterable by a boolean selector
data = ["log1", "log2", "log3", "log4"]
errors = [False, True, False, True]
print(f"  Error logs: {list(compress(data, errors))}")

# chain.from_iterable: flatten nested lists
nested = [["a","b"], ["c","d"], ["e"]]
print(f"  Flattened: {list(chain.from_iterable(nested))}")
```

## 🔍 How It Works
- `batched(iterable, n)` yields tuples of size `n` (last batch may be shorter)
- `pairwise(iterable)` yields `(a1, a2), (a2, a3), ...` — one fewer items than input
- `islice(iterable, start, stop)` — lazy slicing without creating intermediate lists
- `zip_longest(*iterables, fillvalue)` pads shorter iterables with `fillvalue`
- `compress(data, selectors)` keeps elements where the corresponding selector is truthy
- `chain.from_iterable(iterable_of_iterables)` — flatten one level

## ⚠️ Common Pitfall
`batched` and `pairwise` materialize the current batch/pair in memory, but if you hold references to the tuples (e.g., appending to a list), you'll accumulate them. Process batches immediately if memory is tight.

## 🧠 Memory Aid
"batched = 'divide into groups of N.' pairwise = 'consecutive pairs.' islice = 'lazy list slice.' compress = 'filter by boolean mask.'"

## 🏃 Try It
Use `batched` to group numbers 1-20 into batches of 5. Use `pairwise` to compute deltas between consecutive temperatures `[72, 75, 71, 68, 73]`.

## 🔗 Related
- [itertools](04-itertools.md) — `chain`, `product`, `groupby`, `accumulate`

## ➡️ Next
[Typing Patterns](23-typing-patterns.md)
