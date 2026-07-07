"""Performance optimization: N+1 queries, indexing, connection pooling, profiling."""
from typing import Any, Optional, Callable
from functools import wraps
import time
import random
import json


# ======================== Query Tracking ========================

class QueryTracker:
    """Tracks queries for N+1 detection and optimization."""
    def __init__(self):
        self.queries: list[dict] = []

    def log_query(self, query: str, duration: float, source: str = ""):
        self.queries.append({"query": query, "duration": duration, "source": source})

    @property
    def total_queries(self) -> int:
        return len(self.queries)

    @property
    def total_duration(self) -> float:
        return sum(q["duration"] for q in self.queries)

    def summary(self) -> str:
        return f"{self.total_queries} queries in {self.total_duration:.3f}s"

    def detect_n_plus_one(self, threshold: int = 5) -> list[dict]:
        """Detect potential N+1 patterns (same query repeated)."""
        from collections import Counter
        query_texts = [q["query"].split("WHERE")[0].split("ORDER")[0] for q in self.queries]
        repeated = {k: v for k, v in Counter(query_texts).items() if v > threshold}
        return [{"pattern": k, "count": v} for k, v in repeated.items()]


tracker = QueryTracker()


class QuerySet:
    """Simulates Django QuerySet with select_related/prefetch_related."""
    def __init__(self, model_name: str, data: list[dict] = None):
        self.model_name = model_name
        self.data = data or []
        self._prefetch: list[str] = []
        self._select: list[str] = []

    def select_related(self, *fields):
        """JOIN-based eager loading for FK/O2O."""
        self._select = list(fields)
        return self

    def prefetch_related(self, *fields):
        """Separate query-based eager loading for M2M/reverse."""
        self._prefetch = list(fields)
        return self

    def all(self):
        tracker.log_query(f"SELECT * FROM {self.model_name}", 0.01, "all")
        return self.data

    def filter(self, **kwargs):
        cond = " AND ".join(f"{k}={v}" for k, v in kwargs.items())
        tracker.log_query(f"SELECT * FROM {self.model_name} WHERE {cond}", 0.005, "filter")
        result = [item for item in self.data if all(item.get(k) == v for k, v in kwargs.items())]
        return QuerySet(self.model_name, result)

    def get(self, **kwargs):
        cond = " AND ".join(f"{k}={v}" for k, v in kwargs.items())
        tracker.log_query(f"SELECT * FROM {self.model_name} WHERE {cond} LIMIT 1", 0.003, "get")
        for item in self.data:
            if all(item.get(k) == v for k, v in kwargs.items()):
                return item
        return None


# ======================== Data Models ========================

POSTS = [
    {"id": 1, "title": "Hello Django", "author_id": 1, "category_id": 1},
    {"id": 2, "title": "DRF Guide", "author_id": 1, "category_id": 2},
    {"id": 3, "title": "Python Tips", "author_id": 2, "category_id": 1},
]

AUTHORS = [
    {"id": 1, "name": "Alice", "email": "alice@x.com"},
    {"id": 2, "name": "Bob", "email": "bob@x.com"},
]

COMMENTS = [
    {"id": 1, "post_id": 1, "text": "Great!"},
    {"id": 2, "post_id": 1, "text": "Thanks!"},
    {"id": 3, "post_id": 2, "text": "Nice"},
    {"id": 4, "post_id": 1, "text": "Helpful"},
]


# ======================== N+1 Demo ========================

def posts_without_eager_loading() -> list[dict]:
    """N+1 query pattern: query posts, then query author for each."""
    result = []
    posts = QuerySet("posts", POSTS).all()
    for post in posts:
        author = QuerySet("authors", AUTHORS).get(id=post["author_id"])
        result.append({**post, "author_name": author["name"] if author else "?"})
    return result


def posts_with_select_related() -> list[dict]:
    """Optimized: single query with JOIN."""
    data = []
    for post in POSTS:
        author = next((a for a in AUTHORS if a["id"] == post["author_id"]), None)
        data.append({**post, "author_name": author["name"] if author else "?"})
    tracker.log_query(
        "SELECT * FROM posts LEFT JOIN authors ON posts.author_id = authors.id",
        0.008,
        "select_related",
    )
    return data


# ======================== Indexing ========================

class Index:
    """Simulates a database index for faster lookups."""
    def __init__(self, field: str):
        self.field = field
        self._map: dict = {}

    def build(self, data: list[dict]):
        self._map = {}
        for item in data:
            val = item.get(self.field)
            if val is not None:
                if val not in self._map:
                    self._map[val] = []
                self._map[val].append(item)

    def lookup(self, value) -> list[dict]:
        return self._map.get(value, [])


# ======================== Connection Pooling ========================

class ConnectionPool:
    """Simulates database connection pooling."""
    def __init__(self, min_size: int = 2, max_size: int = 10):
        self.min_size = min_size
        self.max_size = max_size
        self._connections: list[int] = []
        self._initialize()

    def _initialize(self):
        for i in range(self.min_size):
            conn_id = random.randint(1000, 9999)
            self._connections.append(conn_id)

    def get_connection(self) -> int:
        if self._connections:
            return self._connections.pop()
        if len(self._connections) < self.max_size:
            conn_id = random.randint(1000, 9999)
            return conn_id
        raise RuntimeError("Connection pool exhausted")

    def return_connection(self, conn_id: int):
        self._connections.append(conn_id)

    @property
    def available(self) -> int:
        return len(self._connections)


# ======================== Profiling ========================

def profile(func: Callable) -> Callable:
    """Simple profiling decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        wrapper._total_time += (t1 - t0)
        wrapper._call_count += 1
        print(f"  [Profile] {func.__name__}: {(t1-t0)*1000:.2f}ms (total: {wrapper._total_time*1000:.2f}ms, calls: {wrapper._call_count})")
        return result
    wrapper._total_time = 0.0
    wrapper._call_count = 0
    return wrapper


@profile
def slow_function():
    time.sleep(0.1)
    return "done"


# ======================== Demo ========================
print("=== Performance Optimization Demo ===\n")

# --- N+1 detection ---
print("1. N+1 Query Pattern (WITHOUT eager loading):")
tracker.queries.clear()
result = posts_without_eager_loading()
print(f"   {tracker.summary()}")
for issue in tracker.detect_n_plus_one(2):
    print(f"   ⚠ Potential N+1: '{issue['pattern']}' repeated {issue['count']} times")

print("\n2. Optimized (WITH select_related):")
tracker.queries.clear()
result = posts_with_select_related()
print(f"   {tracker.summary()} (reduced to 1 query!)")

# --- Indexing ---
print("\n3. Indexing:")
idx = Index("author_id")
idx.build(POSTS)
t0 = time.time()
alice_posts = idx.lookup(1)
t1 = time.time()
print(f"   Lookup by author_id=1: {len(alice_posts)} posts in {(t1-t0)*1000:.3f}ms")

# --- Connection pooling ---
print("\n4. Connection Pooling:")
pool = ConnectionPool(min_size=3, max_size=5)
print(f"   Initial connections: {pool.available}")
conn1 = pool.get_connection()
conn2 = pool.get_connection()
print(f"   After getting 2: {pool.available} available")
pool.return_connection(conn1)
print(f"   After returning 1: {pool.available} available")

# --- Profiling ---
print("\n5. Profiling:")
for _ in range(3):
    slow_function()
print(f"   Average: {(slow_function._total_time / slow_function._call_count * 1000):.2f}ms per call")

# --- Key strategies summary ---
print("\n6. Optimization Strategies Summary:")
strategies = [
    ("select_related()", "JOIN for FK/O2O — reduces queries from N+1 to 2"),
    ("prefetch_related()", "Separate queries for M2M/reverse — reduces N+1 to 2"),
    ("only() / defer()", "SELECT specific columns — less data transfer"),
    ("Database indexes", "Faster WHERE/ORDER BY — O(n) → O(log n)"),
    ("Connection pooling", "Reuse connections — avoids TCP handshake overhead"),
    ("Caching", "Memcached/Redis — skips DB entirely for hot data"),
    ("Bulk operations", "bulk_create / bulk_update — single query vs N"),
]
for name, desc in strategies:
    print(f"   🔸 {name}: {desc}")
