"""Performance tuning: profiling, caching, connection pooling, query optimization."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import time
import functools


# ======================== Profiler ========================

class Profiler:
    """Simple profiling decorator and collector."""
    def __init__(self):
        self.profiles: dict[str, list[float]] = {}

    def profile(self, name: str | None = None):
        def decorator(func):
            func_name = name or func.__name__
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                if func_name not in self.profiles:
                    self.profiles[func_name] = []
                self.profiles[func_name].append(elapsed)
                return result
            return wrapper
        return decorator

    def stats(self, func_name: str | None = None) -> dict:
        if func_name:
            times = self.profiles.get(func_name, [])
            return {
                "name": func_name,
                "calls": len(times),
                "total": round(sum(times), 4),
                "avg": round(sum(times) / len(times), 4) if times else 0,
                "min": round(min(times), 4) if times else 0,
                "max": round(max(times), 4) if times else 0,
            }
        return {
            name: self.stats(name) for name in self.profiles
        }

    def summary(self) -> str:
        lines = ["Profiling Summary:"]
        for name, times in sorted(self.profiles.items()):
            avg = sum(times) / len(times)
            total = sum(times)
            lines.append(f"  {name:30s} calls={len(times):4d} avg={avg*1000:.1f}ms total={total*1000:.1f}ms")
        return "\n".join(lines)


profiler = Profiler()


# ======================== Cache ========================

class Cache:
    """In-memory cache with TTL."""
    def __init__(self):
        self._data: dict[str, tuple[Any, float]] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Any | None:
        if key in self._data:
            value, expiry = self._data[key]
            if expiry > time.time():
                self._hits += 1
                return value
            else:
                del self._data[key]
        self._misses += 1
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 60):
        self._data[key] = (value, time.time() + ttl_seconds)

    def delete(self, key: str):
        self._data.pop(key, None)

    def clear(self):
        self._data.clear()

    def stats(self) -> dict:
        return {
            "size": len(self._data),
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(self._hits / (self._hits + self._misses) * 100, 1) if (self._hits + self._misses) > 0 else 0,
        }

    def cached(self, ttl_seconds: int = 60):
        """Decorator: cache function results."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                result = self.get(key)
                if result is not None:
                    return result
                result = func(*args, **kwargs)
                self.set(key, result, ttl_seconds)
                return result
            return wrapper
        return decorator


cache = Cache()


# ======================== Connection Pool Monitor ========================

class ConnectionPool:
    """Simulated connection pool with monitoring."""
    def __init__(self, min_size: int = 2, max_size: int = 10):
        self.min_size = min_size
        self.max_size = max_size
        self._active = 0
        self._idle = min_size
        self._total_created = min_size
        self._total_acquired = 0
        self._total_released = 0
        self._wait_times: list[float] = []

    def acquire(self) -> "Connection":
        self._total_acquired += 1
        start = time.time()

        if self._idle > 0:
            self._idle -= 1
        elif self._active < self.max_size:
            self._total_created += 1
        else:
            time.sleep(0.01)  # Simulate wait

        self._active += 1
        self._wait_times.append(time.time() - start)
        return Connection(self)

    def release(self, conn: "Connection"):
        self._active -= 1
        self._idle += 1
        self._total_released += 1

    def stats(self) -> dict:
        return {
            "active": self._active,
            "idle": self._idle,
            "total_created": self._total_created,
            "total_acquired": self._total_acquired,
            "total_released": self._total_released,
            "min_size": self.min_size,
            "max_size": self.max_size,
            "utilization": round(self._active / self.max_size * 100, 1),
        }


class Connection:
    def __init__(self, pool: ConnectionPool):
        self.pool = pool

    def close(self):
        self.pool.release(self)


pool = ConnectionPool(min_size=2, max_size=5)


# ======================== Simulated Slow/Fast Operations ========================

@profiler.profile("slow_query")
def slow_database_query(query: str):
    """Simulate a slow database query (no index)."""
    time.sleep(0.05)
    return f"Result of: {query}"

@profiler.profile("fast_query")
def fast_database_query(query: str):
    """Simulate a fast query (with index)."""
    time.sleep(0.005)
    return f"Result of: {query}"

@profiler.profile("cached_query")
@cache.cached(ttl_seconds=10)
def cached_database_query(query: str):
    """Simulate a query with caching."""
    time.sleep(0.05)
    return f"Cached result of: {query}"

@profiler.profile("serial_work")
def do_serial_work(n: int):
    """Do work serially."""
    for i in range(n):
        slow_database_query(f"serial_query_{i}")

@profiler.profile("n+1_query")
def n_plus_one_query(user_ids: list[int]):
    """Simulate N+1 query problem."""
    results = []
    for uid in user_ids:
        user = slow_database_query(f"SELECT * FROM users WHERE id={uid}")
        posts = slow_database_query(f"SELECT * FROM posts WHERE user_id={uid}")
        results.append({"user": user, "posts": posts})
    return results

@profiler.profile("optimized_query")
def optimized_query(user_ids: list[int]):
    """Simulate optimized query (JOIN)."""
    result = slow_database_query(f"SELECT * FROM users JOIN posts ON users.id=posts.user_id WHERE users.id IN ({','.join(map(str, user_ids))})")
    return result


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


@app.get("/benchmark/slow")
def benchmark_slow():
    slow_database_query("SELECT * FROM users")
    slow_database_query("SELECT * FROM posts")
    return {"message": "Slow queries done"}

@app.get("/benchmark/fast")
def benchmark_fast():
    fast_database_query("SELECT * FROM users")
    fast_database_query("SELECT * FROM posts")
    return {"message": "Fast queries done"}

@app.get("/benchmark/cached")
def benchmark_cached():
    cached_database_query("SELECT * FROM users")
    cached_database_query("SELECT * FROM users")  # Second call hits cache
    cached_database_query("SELECT * FROM users")  # Third call hits cache
    return {"message": "Cached queries done"}

@app.get("/performance/profile")
def performance_profile():
    return profiler.stats()

@app.get("/performance/cache")
def performance_cache():
    return cache.stats()

@app.get("/performance/pool")
def performance_pool():
    return pool.stats()


# ======================== Demo ========================
print("=" * 60)
print("  PERFORMANCE TUNING DEMO")
print("=" * 60)

# 1. Compare slow vs fast queries
print("\n1. Slow query vs Fast query:")
for i in range(5):
    slow_database_query("SELECT * FROM users")
    fast_database_query("SELECT * FROM users")

slow_stats = profiler.stats("slow_query")
fast_stats = profiler.stats("fast_query")
print(f"   Slow:  avg={slow_stats['avg']*1000:.1f}ms  ({slow_stats['calls']} calls)")
print(f"   Fast:  avg={fast_stats['avg']*1000:.1f}ms  ({fast_stats['calls']} calls)")
print(f"   Speedup: {slow_stats['avg']/fast_stats['avg']:.0f}x")

# 2. Caching benefit
print("\n2. Caching benefit:")
for i in range(3):
    cached_database_query("SELECT * FROM users")

cache_result = cache.stats()
print(f"   Cache: {cache_result}")

# 3. N+1 vs optimized
print("\n3. N+1 query problem:")
n_plus_one_query([1, 2, 3, 4, 5])
n1_stats = profiler.stats("n+1_query")
print(f"   N+1: {n1_stats['calls']} call, avg={n1_stats['avg']*1000:.1f}ms")

optimized_query([1, 2, 3, 4, 5])
opt_stats = profiler.stats("optimized_query")
print(f"   OPTIMIZED: {opt_stats['calls']} call, avg={opt_stats['avg']*1000:.1f}ms")
print(f"   Improvement: {n1_stats['avg']/opt_stats['avg']:.0f}x")

# 4. Connection pool
print("\n4. Connection pool behavior:")
conns = []
for i in range(8):
    conn = pool.acquire()
    conns.append(conn)
    print(f"   Acquire {i+1}: active={pool.stats()['active']}, idle={pool.stats()['idle']}")

for conn in conns:
    conn.close()

print(f"   After release: active={pool.stats()['active']}, idle={pool.stats()['idle']}")
print(f"   Pool utilization: {pool.stats()['utilization']}%")

# 5. Full profile summary
print(f"\n5. {profiler.summary()}")
