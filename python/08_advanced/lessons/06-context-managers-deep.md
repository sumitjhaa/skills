# 🎯 Context Managers Deep
<!-- ⏱️ 15 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Write custom context managers with `__enter__`/`__exit__` and `@contextmanager`, use `contextlib.ExitStack`, and async context managers.

> 💡 **TL;DR — The whole point:** Context managers automate setup and teardown — open/close, connect/disconnect, lock/unlock — using `with` blocks.

## 🔗 Why This Matters
Database connections, file handles, locks, transactions, temporary files, timing — context managers ensure cleanup happens even if exceptions occur. Most Python resources already support `with`.

## The Concept
`__enter__` sets up the resource and returns it. `__exit__` tears it down (always runs, even on exceptions). `@contextmanager` lets you write one using `yield`.

## Code Example
```python
"""E-commerce: Context managers for database connections, timing, and transactions."""

from contextlib import contextmanager, ExitStack
import time


# ─── Class-based context manager ───
class DatabaseConnection:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self._connected = False

    def __enter__(self):
        print(f"[DB] Connecting to {self.db_name}...")
        self._connected = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[DB] Disconnecting from {self.db_name}")
        if exc_type:
            print(f"[DB] Error occurred: {exc_val}")
        self._connected = False
        return False  # Don't suppress exceptions

    def query(self, sql: str) -> str:
        if not self._connected:
            raise RuntimeError("Not connected")
        return f"[DB] Result for: {sql}"


# ─── @contextmanager decorator ───
@contextmanager
def timed_block(name: str):
    start = time.perf_counter()
    print(f"[Timer] Starting '{name}'...")
    yield
    elapsed = time.perf_counter() - start
    print(f"[Timer] '{name}' took {elapsed:.4f}s")


# ─── Nested context managers with ExitStack ───
@contextmanager
def transaction(db_name: str):
    print(f"[TX] Beginning transaction on {db_name}")
    try:
        yield
        print(f"[TX] Committing transaction on {db_name}")
    except Exception:
        print(f"[TX] Rolling back transaction on {db_name}")
        raise


# ─── Usage ───
print("=== Basic context manager ===")
with DatabaseConnection("shop_db") as db:
    result = db.query("SELECT * FROM products")
    print(f"  {result}")

print("\n=== Context manager with exception ===")
try:
    with DatabaseConnection("shop_db") as db:
        raise ValueError("Query failed!")
except ValueError:
    print("  (Caught exception)")

print("\n=== @contextmanager timer ===")
with timed_block("import_products"):
    time.sleep(0.1)
    print("  Imported 1000 products")

print("\n=== ExitStack: multiple resources ===")
with ExitStack() as stack:
    db1 = stack.enter_context(DatabaseConnection("users_db"))
    db2 = stack.enter_context(DatabaseConnection("orders_db"))
    print(f"  {db1.query('SELECT * FROM users')}")
    print(f"  {db2.query('SELECT * FROM orders')}")
```

## 🔍 How It Works
- `__enter__` returns the resource (bound to `as` variable)
- `__exit__` receives exception info (or all `None` if no exception)
- Return `True` from `__exit__` to suppress exceptions (rarely a good idea)
- `@contextmanager` wraps a generator: `yield` is the boundary between setup and teardown
- `ExitStack` lets you manage multiple context managers dynamically
- Async context managers use `__aenter__` / `__aexit__` with `async with`

## ⚠️ Common Pitfall
Suppressing exceptions by returning `True` from `__exit__`. Only do this if you have a very good reason — otherwise you'll hide bugs silently.

## 🧠 Memory Aid
"`with` = 'with this resource, do that; when done, clean up.' `__enter__` = setup. `__exit__` = teardown."

## 🏃 Try It
Write a `@contextmanager` for a file locker: acquire lock on enter, release on exit. Use `threading.Lock`. Demonstrate that two threads can't access the critical section simultaneously.

## 🔗 Related
- [Comprehensions Deep](07-comprehensions-deep.md) — generator expressions
- [Advanced Patterns](10-advanced-patterns.md) — context manager + generator

## ➡️ Next
[Comprehensions Deep](07-comprehensions-deep.md)
