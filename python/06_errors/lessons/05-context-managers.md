# 📦 Context Managers
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to use `with` statements, implement `__enter__`/`__exit__`, use `@contextmanager`, and utilities from `contextlib`.

> 💡 **TL;DR — The whole point:** Context managers automate setup and cleanup — open a file, use it, auto-close. Never forget to close again.

## 🔗 Why This Matters
Custom exceptions defined *what* can go wrong. Context managers ensure resources are *always* cleaned up, even when exceptions happen. Database connections, file handles, locks — all need guaranteed cleanup.

## The Concept
A context manager is an object that defines `__enter__` (setup) and `__exit__` (cleanup) methods. The `with` statement calls `__enter__`, runs your code, then calls `__exit__` — even if your code raises an exception.

Think of context managers like a hotel room: `__enter__` = check in (get the key), `__exit__` = check out (return the key, clean up).

## Code Example

```python
"""Database connections, file handles, and locks with context managers."""

from contextlib import contextmanager
import sqlite3


class ManagedDatabase:
    """Context manager for SQLite database connections."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        print(f"[DB] Connected to {self.db_path}")
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type:
                print(f"[DB] Error occurred: {exc_val} — rolling back")
                self.connection.rollback()
            else:
                self.connection.commit()
                print(f"[DB] Committed changes")
            self.connection.close()
            print(f"[DB] Connection closed")
        return False  # Don't suppress exceptions


@contextmanager
def timer():
    """Context manager that times a code block."""
    import time
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[TIMER] Block took {elapsed:.4f}s")


# Using the database context manager
db_path = "/tmp/test_app.db"

with ManagedDatabase(db_path) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users (name) VALUES ('Alice')")
    conn.execute("INSERT INTO users (name) VALUES ('Bob')")
    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    print(f"[OK] {row[0]} users inserted")

with timer():
    total = sum(range(1_000_000))
    print(f"[SUM] Total: {total}")

import os
os.remove(db_path)
```

## 🔍 How It Works
- `with expr as var:` calls `expr.__enter__()` → assigns to `var`
- `__exit__` receives `(exc_type, exc_val, exc_tb)` from any exception
- Return `True` from `__exit__` to suppress the exception
- `@contextmanager` turns a generator into a context manager (yield once)
- `contextlib.suppress(Exception)` ignores specified exceptions

## ⚠️ Common Pitfall
Forgetting to `return False` from `__exit__`. If `__exit__` returns `True`, the exception is silently swallowed. Only return `True` when you intentionally handle the error.

## 🧠 Memory Aid
**"with = get it, use it, lose it"**: The three phases of every context manager: acquire the resource, use it, automatically release it.

## 🏃 Try It
Write a context manager `atomic_write(filepath)` that writes to a temp file, and on `__exit__` renames the temp to the target path (atomic write). If an exception occurs, delete the temp file.

## 🔗 Related
- [Custom Exceptions →](./04-custom-exceptions.md)
- [Logging →](./06-logging.md)

## ➡️ Next
[Logging](./06-logging.md)
