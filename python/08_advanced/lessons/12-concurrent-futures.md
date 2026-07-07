# 🎯 Concurrent Futures
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use `ThreadPoolExecutor` and `ProcessPoolExecutor` for parallel execution, `as_completed`, `wait`, and `map`.

> 💡 **TL;DR — The whole point:** `concurrent.futures` provides a high-level API for running tasks in parallel — threads for I/O, processes for CPU — with a clean future-based interface.

## 🔗 Why This Matters
Fetching 100 product reviews from an API, processing 1000 images, scraping multiple websites — these are embarrassingly parallel tasks. `concurrent.futures` makes them simple without managing threads/processes manually.

## The Concept
- `ThreadPoolExecutor` — for I/O-bound tasks (network, disk, DB)
- `ProcessPoolExecutor` — for CPU-bound tasks (computation, image processing)
- `submit(fn, *args)` — returns a `Future` object
- `as_completed(futures)` — yields futures as they complete
- `wait(futures)` — block until a condition
- `map(fn, iterable)` — apply function to every item in parallel

## Code Example
```python
"""E-commerce: Parallel product price fetching and inventory processing."""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait
import time
import math


# ─── I/O-bound: simulate API calls ───
def fetch_product_price(product_id: int) -> dict:
    time.sleep(0.2)  # simulate network latency
    return {"id": product_id, "price": round(10 + product_id * 1.5, 2), "source": "api"}


def batch_fetch_prices(product_ids: list[int]) -> list[dict]:
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_product_price, pid): pid for pid in product_ids}
        results = []
        for future in as_completed(futures):
            pid = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"  [Done] Product {pid}: ${result['price']}")
            except Exception as e:
                print(f"  [Error] Product {pid}: {e}")
        return results


# ─── CPU-bound: process-intensive task ───
def compute_discount_matrix(prices: list[float]) -> list[list[float]]:
    """Compute pairwise discount interactions (CPU-bound)."""
    N = len(prices)
    matrix = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            matrix[i][j] = round(prices[i] * prices[j] * 0.01, 2)
    return matrix


def parallel_discount_matrix(prices: list[float]) -> list[list[float]]:
    chunk_size = math.ceil(len(prices) / 4)
    chunks = [prices[i:i + chunk_size] for i in range(0, len(prices), chunk_size)]

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(compute_discount_matrix, chunk) for chunk in chunks]
        results = [f.result() for f in futures]

    # Merge results
    merged = []
    for chunk_result in results:
        merged.extend(chunk_result)
    return merged


# ─── map: simple parallel mapping ───
def apply_coupon(price: float) -> float:
    time.sleep(0.05)
    return round(price * 0.9, 2)


# ─── Usage ───
print("=== Fetching prices (I/O-bound) ===")
start = time.perf_counter()
prices_data = batch_fetch_prices(list(range(1, 11)))
seq_time = time.perf_counter() - start

print(f"\nSequential would take ~{len(prices_data) * 0.2:.1f}s, took {seq_time:.2f}s")

print("\n=== Applying coupons (map) ===")
prices = [p["price"] for p in prices_data]
with ThreadPoolExecutor(max_workers=5) as executor:
    discounted = list(executor.map(apply_coupon, prices))
print(f"Discounted prices: {[f'${p:.2f}' for p in discounted[:5]]}...")

print(f"\n=== Parallel matrix computation (CPU-bound) ===")
start = time.perf_counter()
matrix = parallel_discount_matrix(prices)
elapsed = time.perf_counter() - start
print(f"Matrix computed in {elapsed:.2f}s, size {len(matrix)}×{len(matrix)}")
```

## 🔍 How It Works
- `submit()` schedules a callable and returns a `Future` — you can check status, get result, cancel
- `as_completed()` yields futures in completion order (not submission order)
- `wait(futures, return_when=ALL_COMPLETED)` blocks until condition
- `map()` is like built-in `map()` but runs in parallel — results in submission order
- `max_workers` controls parallelism — for I/O, set higher (10-20); for CPU, match cores
- Futures don't start until the executor starts processing; `with` block waits for all to complete

## ⚠️ Common Pitfall
`ProcessPoolExecutor` code must be importable in the main module — use `if __name__ == "__main__"` guard. Pickling errors if the function or its arguments aren't pickleable.

## 🧠 Memory Aid
"ThreadPool = I/O (waiting). ProcessPool = CPU (computing). Future = 'I'll give you the result later'. as_completed = 'tell me when each one finishes.'"

## 🏃 Try It
Write a parallel web scrapper using `ThreadPoolExecutor` that fetches 20 URLs with `urllib.request`. Measure time vs sequential. Handle errors gracefully.

## 🔗 Related
- [Weakref & ContextVars](13-weakref-contextvars.md) — memory management in concurrent code
- [Asyncio Deep](../10_ecosystem/lessons/05-asyncio-deep.md) — async alternative to threads

## ➡️ Next
[Weakref & ContextVars](13-weakref-contextvars.md)
