"""Pytest Deep — Advanced patterns for order processing tests.
Run: pytest 09-15-pytest-deep.py -v
"""

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
    yield db
    if db_path.exists():
        db_path.unlink()


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


@pytest.mark.parametrize("order_id,expected_customer", [
    ("ORD-001", "Alice"),
    ("ORD-002", "Bob"),
])
def test_find_orders(db_with_orders, order_id, expected_customer):
    order = db_with_orders.get(order_id)
    assert order is not None
    assert order.customer == expected_customer


def test_monkeypatch_env(monkeypatch, db_with_orders):
    monkeypatch.setenv("DB_PATH", "/tmp/test_orders.json")
    assert Path("/tmp/test_orders.json").name == "test_orders.json"


def test_print_output(capsys):
    print("Order processed successfully")
    captured = capsys.readouterr()
    assert "Order processed" in captured.out


def test_temp_file(tmp_path):
    data_file = tmp_path / "test.json"
    data_file.write_text(json.dumps({"key": "value"}))
    loaded = json.loads(data_file.read_text())
    assert loaded["key"] == "value"
