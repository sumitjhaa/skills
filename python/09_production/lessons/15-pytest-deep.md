# 🎯 Pytest Deep
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Advanced pytest — fixture scopes, `conftest.py`, `parametrize`, fixture `yield` for setup/teardown, `monkeypatch`, `tmp_path`, `capsys`, and mocking.

> 💡 **TL;DR — The whole point:** pytest fixtures are powerful dependency injection. This lesson covers everything you need for production test suites — scoped fixtures, parametrized tests, mocking, and I/O capture.

## 🔗 Why This Matters
Real-world tests need database cleanup, temporary files, mocked API responses, and capturing logs. Mastering these patterns means your test suite is fast, reliable, and catches real bugs.

## The Concept
- **Fixture scopes:** `function` (default), `class`, `module`, `session`
- **`conftest.py`:** shared fixtures across multiple test files
- **Fixture `yield`:** set up before test, tear down after (context manager pattern)
- **`monkeypatch`:** temporarily replace objects/functions/env vars
- **`tmp_path`:** temporary directory per test
- **`capsys`:** capture stdout/stderr

## Code Example
```python
"""E-commerce: Advanced pytest patterns for order processing."""

import json
import pytest
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Order:
    id: str
    customer: str
    items: list[dict]
    total: float
    paid: bool = False


class OrderDB:
    def __init__(self, path: Path):
        self.path = path
        self._orders: dict[str, Order] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self._orders = {k: Order(**v) for k, v in data.items()}

    def _save(self) -> None:
        data = {k: asdict(v) for k, v in self._orders.items()}
        self.path.write_text(json.dumps(data, indent=2))

    def add(self, order: Order) -> None:
        self._orders[order.id] = order
        self._save()

    def get(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)

    def mark_paid(self, order_id: str) -> None:
        if order_id in self._orders:
            self._orders[order_id].paid = True
            self._save()


# ─── conftest.py (shared) ───
# @pytest.fixture
# def db_path(tmp_path) -> Path:
#     return tmp_path / "orders.json"
#
# @pytest.fixture
# def db(db_path) -> OrderDB:
#     return OrderDB(db_path)


# ─── Fixture with yield (setup/teardown) ───
@pytest.fixture
def sample_orders() -> list[Order]:
    return [
        Order("ORD-001", "Alice", [{"sku": "LAP-001", "price": 1499.99}], 1499.99),
        Order("ORD-002", "Bob", [{"sku": "MOU-001", "price": 29.99}], 29.99),
    ]


@pytest.fixture
def db_with_orders(tmp_path, sample_orders) -> OrderDB:
    db_path = tmp_path / "orders.json"
    db = OrderDB(db_path)
    for order in sample_orders:
        db.add(order)
    yield db  # Test uses this
    # Teardown: clean up if needed
    if db_path.exists():
        db_path.unlink()


# ─── Basic tests ───
def test_db_add_and_get(db_with_orders: OrderDB):
    order = db_with_orders.get("ORD-001")
    assert order is not None
    assert order.customer == "Alice"
    assert round(order.total, 2) == 1499.99


def test_db_mark_paid(db_with_orders: OrderDB):
    db_with_orders.mark_paid("ORD-001")
    order = db_with_orders.get("ORD-001")
    assert order is not None
    assert order.paid is True


def test_db_get_nonexistent(db_with_orders: OrderDB):
    assert db_with_orders.get("NONEXISTENT") is None


# ─── Parametrize ───
@pytest.mark.parametrize("order_id,expected_customer", [
    ("ORD-001", "Alice"),
    ("ORD-002", "Bob"),
])
def test_find_orders(db_with_orders, order_id, expected_customer):
    order = db_with_orders.get(order_id)
    assert order is not None
    assert order.customer == expected_customer


# ─── Monkeypatch ───
def test_monkeypatch_env(monkeypatch, db_with_orders):
    monkeypatch.setenv("DB_PATH", "/tmp/test_orders.json")
    assert Path("/tmp/test_orders.json").name == "test_orders.json"


# ─── Capsys ---
def test_print_output(capsys):
    print("Order processed successfully")
    captured = capsys.readouterr()
    assert "Order processed" in captured.out


# ─── tmp_path ───
def test_temp_file(tmp_path):
    data_file = tmp_path / "test.json"
    data_file.write_text(json.dumps({"key": "value"}))
    loaded = json.loads(data_file.read_text())
    assert loaded["key"] == "value"
```

## 🔍 How It Works
- **`tmp_path`** — creates a unique temp directory per test (pathlib.Path)
- **Fixture `yield`** — code before `yield` is setup, after `yield` is teardown
- **`conftest.py`** — place shared fixtures here; pytest discovers them in the directory tree
- **`monkeypatch`** — restores original values after the test (no cleanup needed)
- **`capsys`** — captures all stdout/stderr; `readouterr()` returns `(out, err)`
- **Fixtures can use other fixtures** — `db_with_orders` uses `tmp_path` and `sample_orders`

## ⚠️ Common Pitfall
Fixture teardown code after `yield` runs even if the test fails (that's good!), but if the setup code raises, the teardown never runs. Handle exceptions in setup with try/finally if needed.

## 🧠 Memory Aid
"Fixture yield = context manager for tests. `conftest.py` = shared fixtures. `monkeypatch` = temporary override. `tmp_path` = short-lived files."

## 🏃 Try It
Create a fixture `api_client` that uses `monkeypatch` to mock `httpx.Client.post()` and returns a simulated payment response. Write a test for the `PaymentGatewayClient.charge()` method.

## 🔗 Related
- [Testing with pytest](04-testing-pytest.md) — pytest basics
- [HTTPX & Requests Deep](14-httpx-requests-deep.md) — mocking HTTP

## ➡️ Next
Review and practice with [Exercises](../practice/exercises.md)
