"""08-06-context-managers-deep.py — E-commerce: DB connection, timer, ExitStack."""

from contextlib import contextmanager, ExitStack
import time


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
            print(f"[DB] Error: {exc_val}")
        self._connected = False
        return False

    def query(self, sql: str) -> str:
        if not self._connected:
            raise RuntimeError("Not connected")
        return f"[DB] Result for: {sql}"


@contextmanager
def timed_block(name: str):
    start = time.perf_counter()
    print(f"[Timer] Starting '{name}'...")
    yield
    elapsed = time.perf_counter() - start
    print(f"[Timer] '{name}' took {elapsed:.4f}s")


print("=== Basic context manager ===")
with DatabaseConnection("shop_db") as db:
    result = db.query("SELECT * FROM products")
    print(f"  {result}")

print("\n=== Timer ===")
with timed_block("import_products"):
    time.sleep(0.1)
    print("  Imported 1000 products")

print("\n=== ExitStack ===")
with ExitStack() as stack:
    db1 = stack.enter_context(DatabaseConnection("users_db"))
    db2 = stack.enter_context(DatabaseConnection("orders_db"))
    print(f"  {db1.query('SELECT * FROM users')}")
    print(f"  {db2.query('SELECT * FROM orders')}")
