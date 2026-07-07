"""Profiling with cProfile, pstats, and optimization patterns."""
import cProfile
import pstats
import io
import time
from functools import lru_cache


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
