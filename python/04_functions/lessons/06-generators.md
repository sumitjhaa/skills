# ⚡ Generators
<!-- ⏱️ 11 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to create lazy sequences with `yield`, generator expressions, and two-way communication with `.send()`.

> 💡 **TL;DR — The whole point:** Generators produce values one at a time on demand — like a streaming service instead of downloading the whole library.

## 🔗 Why This Matters
Recursion showed you sequences generated eagerly. What if the sequence is infinite (user IDs, timestamps) or too large for memory (10M log entries)? Generators produce values lazily — one at a time.

## The Concept
A generator function looks like a regular function but uses `yield` instead of `return`. When called, it returns a generator object that you can iterate over. Each `yield` pauses execution, saves state, and produces a value. The next call resumes from where it paused.

Think of a generator like a page-turner in a book — you never see the whole book at once, just one page at a time.

## Code Example

```python
"""Streaming paginated API results and infinite sequences."""


def paginated_results(data: list, page_size: int = 3):
    """Yield chunks of data as if they were API pages."""
    for i in range(0, len(data), page_size):
        yield {"page": i // page_size + 1, "results": data[i:i + page_size]}


def infinite_counter(start: int = 0, step: int = 1):
    """Generate infinite sequential IDs (like auto-increment)."""
    while True:
        yield start
        start += step


def read_sensor_data(samples: int):
    """Simulate streaming sensor readings."""
    import random
    for _ in range(samples):
        yield round(random.uniform(20.0, 30.0), 1)


# Generator expression — lazy, memory-efficient
squares = (x ** 2 for x in range(10))
print(list(squares))               # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Paginated data
users = [f"user_{i}" for i in range(10)]
for page in paginated_results(users, 3):
    print(f"Page {page['page']}: {page['results']}")

# Infinite — take what you need
counter = infinite_counter()
print([next(counter) for _ in range(5)])  # [0, 1, 2, 3, 4]

# Sensor stream
for reading in read_sensor_data(5):
    print(f"Temp: {reading}°C", end=" | ")  # Temp: 23.5°C | ...
```

## 🔍 How It Works
- `yield` pauses the function, saving its local state; `next()` resumes it
- Generators are **lazy** — they compute values only when requested
- Generator expressions `(x for x in ...)` are like list comprehensions but lazy
- `yield from` delegates iteration to a sub-generator
- `.send(value)` sends a value back into the generator (two-way communication)

## ⚠️ Common Pitfall
Confusing generator expressions with list comprehensions. `(x for x in range(10))` is a generator (lazy, single-use). `[x for x in range(10)]` is a list (eager, reusable).

## 🧠 Memory Aid
**"yield = pause + resume"**: Unlike `return` which exits forever, `yield` is a "be right back" — the function remembers where it was.

## 🏃 Try It
Write a generator `fibonacci(limit)` that yields Fibonacci numbers up to a given limit. Test it with `list(fibonacci(100))`.

## 🔗 Related
- [Recursion →](./05-recursion.md)
- [Decorators →](./07-decorators.md)

## ➡️ Next
[Decorators](./07-decorators.md)
