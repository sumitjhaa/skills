"""08-10-advanced-patterns.py — Registry, pipeline, strategy patterns."""

from abc import ABC, abstractmethod
from functools import wraps
from typing import ClassVar, Any, Callable


class DataExporter(ABC):
    registry: ClassVar[dict[str, type["DataExporter"]]] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fmt = getattr(cls, "format_name", cls.__name__.lower().replace("exporter", ""))
        DataExporter.registry[fmt] = cls

    @abstractmethod
    def export(self, data: list[dict]) -> str:
        pass


class CsvExporter(DataExporter):
    format_name = "csv"

    def export(self, data: list[dict]) -> str:
        if not data:
            return ""
        header = ",".join(data[0].keys())
        rows = [",".join(str(v) for v in row.values()) for row in data]
        return header + "\n" + "\n".join(rows)


class JsonExporter(DataExporter):
    format_name = "json"

    def export(self, data: list[dict]) -> str:
        import json
        return json.dumps(data, indent=2)


def pipeline_stage(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(gen: Any) -> Any:
        return func(gen)
    return wrapper


@pipeline_stage
def filter_expensive(gen: Any) -> Any:
    return (item for item in gen if item["price"] > 100)


@pipeline_stage
def add_tax(gen: Any) -> Any:
    for item in gen:
        item["price_with_tax"] = round(item["price"] * 1.08, 2)
        yield item


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def calculate(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def calculate(self, total: float) -> float:
        return total * (1 - self.percent / 100)


data = [{"name": "Laptop", "price": 1500}, {"name": "Mouse", "price": 25}, {"name": "Monitor", "price": 400}]

fmt = "csv"
exporter_cls = DataExporter.registry.get(fmt)
if exporter_cls:
    print(f"=== {fmt.upper()} ===")
    print(exporter_cls().export(data))

gen = (item for item in data)
pipeline = filter_expensive(add_tax(gen))
print("\n=== Pipeline ===")
for item in pipeline:
    print(f"  {item['name']}: ${item['price_with_tax']}")

strategy = PercentageDiscount(10)
total = sum(item["price"] for item in data)
print(f"\nTotal: ${total:.2f} → ${strategy.calculate(total):.2f}")
