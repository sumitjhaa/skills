"""07-11-oop-design.py — E-commerce: SRP-compliant report generation."""

from dataclasses import dataclass
import json


@dataclass
class OrderStats:
    total_orders: int
    total_revenue: float
    avg_order_value: float


class OrderAnalyzer:
    def __init__(self, orders: list[dict]):
        self.orders = orders

    def compute(self) -> OrderStats:
        revenue = sum(o["total"] for o in self.orders)
        return OrderStats(
            total_orders=len(self.orders),
            total_revenue=revenue,
            avg_order_value=revenue / len(self.orders) if self.orders else 0,
        )


class JsonFormatter:
    @staticmethod
    def format(data: OrderStats) -> str:
        return json.dumps(data.__dict__, indent=2)


class ReportPrinter:
    @staticmethod
    def print_report(content: str) -> None:
        print(content)


orders_data = [
    {"id": 1, "total": 150.0},
    {"id": 2, "total": 250.0},
    {"id": 3, "total": 99.99},
]

analyzer = OrderAnalyzer(orders_data)
stats = analyzer.compute()
formatted = JsonFormatter.format(stats)
ReportPrinter.print_report(formatted)
