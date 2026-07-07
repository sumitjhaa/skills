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
