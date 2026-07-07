# ⏱️ Profiling & Optimization
<!-- ⏱️ 16 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Find bottlenecks in Python code using `cProfile`, interpret profiling output, and apply optimization patterns for real performance gains.

> 💡 **TL;DR — The whole point:** Don't guess what's slow — measure it. `cProfile` tells you exactly which functions consume the most time. Optimize only after profiling, and always measure before/after.

## 🔗 Why This Matters
Python is fast enough for most production workloads — but only when you avoid the common traps: wrong data structures, unnecessary loops, excessive attribute lookups, and unaware I/O patterns. Profiling turns guesswork into data.

## The Concept

| Tool | When to Use |
|------|------------|
| `timeit` | Micro-benchmark a single expression |
| `cProfile` | Profile an entire program (function-level) |
| `pstats` | Analyze/sort cProfile output |
| `snakeviz` | Visualize profiles as icicle charts |
| `py-spy` | Profile running production processes (no code change) |
| `time` / `perf_counter` | Quick wall-clock measurements |

## Code Example

```python
"""Profiling with cProfile, pstats, and optimization patterns."""
import cProfile
import pstats
import io
import time
from functools import lru_cache

# --- Slow code to profile ---

def slow_way(n: int) -> list[int]:
    result = []
    for i in range(n):
        if is_prime_slow(i):
            result.append(i)
    return result

def is_prime_slow(x: int) -> bool:
    if x < 2:
        return False
    for d in range(2, x):
        if x % d == 0:
            return False
    return True

# --- Optimized version ---

def fast_way(n: int) -> list[int]:
    result = []
    for i in range(n):
        if is_prime_fast(i):
            result.append(i)
    return result

def is_prime_fast(x: int) -> bool:
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for d in range(3, int(x ** 0.5) + 1, 2):
        if x % d == 0:
            return False
    return True

print("=== Profiling with cProfile ===")
pr = cProfile.Profile()
pr.enable()
slow_way(5000)
pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats("cumtime")
ps.print_stats(10)
print(s.getvalue())

print("\n=== Before vs After optimization ===")
for label, func in [("Slow", slow_way), ("Fast", fast_way)]:
    start = time.perf_counter()
    result = func(10000)
    elapsed = time.perf_counter() - start
    print(f"  {label}: {len(result)} primes in {elapsed:.4f}s")

print("\n=== lru_cache optimization ===")
call_count = 0

@lru_cache(maxsize=None)
def cached_prime(x: int) -> bool:
    global call_count
    call_count += 1
    if x < 2:
        return False
    if x == 2:
        return True
    if x % 2 == 0:
        return False
    for d in range(3, int(x ** 0.5) + 1, 2):
        if x % d == 0:
            return False
    return True

start = time.perf_counter()
for n in range(10000):
    _ = cached_prime(n)
elapsed = time.perf_counter() - start
print(f"  Cached: 10000 calls, {call_count} unique, {elapsed:.4f}s")

print("\n=== Top optimization tips ===")
tips = [
    "Profile before optimizing — don't guess",
    "Prefer local variables over global lookups",
    "Use comprehensions over manual loops",
    "Use `in` with sets, not lists (O(1) vs O(n))",
    "`lru_cache` memoizes expensive pure functions",
    "`__slots__` reduces memory per object",
    "Batch I/O instead of line-by-line",
    "Use `threading`/`asyncio` for I/O-bound, `multiprocessing` for CPU-bound",
]
for i, tip in enumerate(tips, 1):
    print(f"  {i}. {tip}")
```

## 🔍 How It Works
- `cProfile.Profile().enable()` / `.disable()` captures function call counts and timing
- `pstats.Stats.sort_stats("cumtime")` sorts by cumulative time (most useful)
- Common sort keys: `"cumtime"` (total time including children), `"tottime"` (self time), `"ncalls"` (call count)
- `is_prime_fast` checks divisibility only up to `sqrt(x)` and skips even numbers — ~1000x faster for `n=10000`
- `lru_cache` stores results of previous calls — trades memory for CPU

## ⚠️ Common Pitfall
- Optimizing before profiling — you'll optimize the wrong thing
- Using `timeit` for full programs — it's for micro-benchmarks only
- Forgetting `__pycache__` / `.pyc` files in benchmarks (they vary first-run vs subsequent)
- Profiling in debug mode — debug assertions and logging skew results

## 🧠 Memory Aid
"Profile first, optimize second, measure third. If you can't measure it, you can't improve it."

## 🏃 Try It
Write a program that processes a 10MB CSV file (~100K rows). Profile it with `cProfile`, identify the slowest function, optimize it, and report the speedup factor.

## 🔗 Related
- [timeit](../05_modules_io/lessons/11-stdlib-more.md) — micro-benchmarking
- [Decorators](../04_functions/lessons/07-decorators.md) — wrap profiling around any function
- [GC & `__slots__`](../07_oop/lessons/10-slots-new.md) — memory optimization
- [Logging Deep](06-logging-deep.md) — production observability alongside profiling

## ➡️ Next
Phase 10 — Ecosystem
