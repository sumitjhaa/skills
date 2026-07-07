"""Database connections, file handles, and locks with context managers."""
from contextlib import contextmanager
import sqlite3
import time
import os


class ManagedDatabase:
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
                print(f"[DB] Error: {exc_val} — rolling back")
                self.connection.rollback()
            else:
                self.connection.commit()
                print(f"[DB] Committed")
            self.connection.close()
        return False


@contextmanager
def timer():
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    print(f"[TIMER] {elapsed:.4f}s")


@contextmanager
def atomic_write(filepath: str):
    """Atomic file write — writes to temp, renames on success."""
    tmp_path = filepath + ".tmp"
    try:
        yield tmp_path
        os.replace(tmp_path, filepath)
        print(f"[ATOMIC] Written to {filepath}")
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


db_path = "/tmp/test_app.db"
with ManagedDatabase(db_path) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users (name) VALUES ('Alice')")
    print("[OK] User inserted")

with timer():
    total = sum(range(1_000_000))

with atomic_write("/tmp/atomic_test.txt") as tmp:
    with open(tmp, "w") as f:
        f.write("Hello from atomic write!")

os.remove(db_path)
os.remove("/tmp/atomic_test.txt")
