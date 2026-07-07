"""08-02-generators-deep.py — E-commerce: generator pipelines for orders."""

from typing import Generator


def read_orders() -> Generator[str, None, None]:
    lines = [
        "ORD-001,Alice,150.00",
        "ORD-002,Bob,250.00",
        "ORD-003,Charlie,99.99",
        "ORD-004,Alice,300.00",
    ]
    for line in lines:
        yield line


def parse_orders(lines: Generator[str, None, None]) -> Generator[dict, None, None]:
    for line in lines:
        oid, customer, total = line.strip().split(",")
        yield {"id": oid, "customer": customer, "total": float(total)}


def filter_high_value(orders: Generator[dict, None, None], min_total: float = 200):
    for order in orders:
        if order["total"] >= min_total:
            yield order


def accumulate_totals(orders: Generator[dict, None, None]) -> Generator[dict, None, None]:
    running = 0.0
    for order in orders:
        running += order["total"]
        order["running_total"] = round(running, 2)
        yield order


def tax_calculator() -> Generator[float, float, None]:
    """Two-way generator: receive pre-tax, yield post-tax."""
    tax_rate = 0.08
    while True:
        amount = yield  # receive via send()
        yield round(amount * (1 + tax_rate), 2)


lines = read_orders()
parsed = parse_orders(lines)
high_value = filter_high_value(parsed, 200)
with_totals = accumulate_totals(high_value)

print("=== Order Pipeline ===")
for order in with_totals:
    print(f"  {order['id']}: {order['customer']} — ${order['total']} (running: ${order['running_total']})")

calc = tax_calculator()
next(calc)  # prime — stops at first yield
amounts = [100.0, 200.0, 50.0]
for amt in amounts:
    result = calc.send(amt)  # send to first yield, get result from second yield
    next(calc)               # advance past second yield for next send
    print(f"Pre-tax: ${amt:.2f} → After tax: ${result:.2f}")
calc.close()
