# 🎯 Generators Deep
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Generator functions, `send/throw/close`, `yield from`, infinite generators, and pipeline patterns.

> 💡 **TL;DR — The whole point:** Generators produce values lazily — one at a time on demand — instead of computing everything upfront.

## 🔗 Why This Matters
Processing a 10GB log file, streaming sensor data, or generating infinite sequences — generators handle these with constant memory. They're the foundation of Python's async/await and power libraries like `pathlib` and `itertools`.

## The Concept
A generator function uses `yield` instead of `return`. Each call to `next()` resumes from the last `yield`. The function's state is preserved between calls.

## Code Example
```python
"""E-commerce: Generator pipelines for processing orders and inventory."""

from typing import Generator


def read_orders(file_path: str) -> Generator[str, None, None]:
    """Simulates reading a large CSV line by line."""
    lines = [
        "ORD-001,Alice,150.00",
        "ORD-002,Bob,250.00",
        "ORD-003,Charlie,99.99",
        "ORD-004,Alice,300.00",
    ]
    for line in lines:
        yield line


def parse_orders(lines: Generator[str, None, None]) -> Generator[dict, None, None]:
    for line in lines:
        order_id, customer, total = line.strip().split(",")
        yield {"id": order_id, "customer": customer, "total": float(total)}


def filter_high_value(orders: Generator[dict, None, None], min_total: float = 200):
    for order in orders:
        if order["total"] >= min_total:
            yield order


def accumulate_totals(orders: Generator[dict, None, None]) -> Generator[dict, None, None]:
    running = 0
    for order in orders:
        running += order["total"]
        order["running_total"] = round(running, 2)
        yield order


# Generator with send() — a two-way generator
def tax_calculator() -> Generator[float, float, None]:
    """Receives amounts, yields amounts after tax."""
    tax_rate = 0.08
    amount = yield
    while True:
        yield round(amount * (1 + tax_rate), 2)
        amount = yield


# Pipeline
lines = read_orders("orders.csv")
parsed = parse_orders(lines)
high_value = filter_high_value(parsed, 200)
with_totals = accumulate_totals(high_value)

print("=== Order Pipeline ===")
for order in with_totals:
    print(f"  {order['id']}: {order['customer']} — ${order['total']} (running: ${order['running_total']})")

# Two-way generator
calc = tax_calculator()
next(calc)  # prime the generator
result1 = calc.send(100.0)
print(f"\nAfter tax on $100: ${result1}")
result2 = calc.send(200.0)
print(f"After tax on $200: ${result2}")
calc.close()
```

## 🔍 How It Works
- Each `yield` pauses execution; `next()` / `send()` resumes it
- `gen.send(value)` sends a value back into the generator (received by `yield` expression)
- `gen.throw(exc)` raises an exception inside the generator
- `gen.close()` raises `GeneratorExit` inside the generator
- `yield from subgen` delegates to another generator — like flattening
- Pipeline: each generator is a processing stage, connected by function calls

## ⚠️ Common Pitfall
Generators are single-use. Once exhausted, they're empty. Call `list(gen)` only once, or re-create the generator.

## 🧠 Memory Aid
"Generator = a paused function. `yield` = 'I'll be right back with the next value.' `send()` = 'here's something to work with.'"

## 🏃 Try It
Create a `fibonacci()` infinite generator, then build a pipeline that filters even Fibonacci numbers and takes the first 10.

## 🔗 Related
- [Iterators](03-iterators.md) — the protocol `yield` implements
- [itertools](04-itertools.md) — generator-based tools

## ➡️ Next
[Iterators](03-iterators.md)
