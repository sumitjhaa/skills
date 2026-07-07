# 🎯 Advanced Patterns
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Combine decorators, generators, context managers, and registries into powerful production patterns.

> 💡 **TL;DR — The whole point:** Advanced patterns combine Python features — decorator + generator, context manager + generator, registry + plugin system — to solve real architectural problems.

## 🔗 Why This Matters
Real production code rarely uses decorators in isolation. The most powerful patterns emerge when you combine them: a decorator that wraps a generator in a context manager, a registry that auto-discovers plugins, a strategy pattern using singletons.

## The Concept
- **Decorator + Generator** — decorate generators for preprocessing/postprocessing
- **Context Manager + Generator** — generators that manage their own lifecycle
- **Registry Pattern** — auto-register subclasses via `__init_subclass__`
- **Strategy Pattern** — pluggable algorithms via protocols/ABCs
- **Singleton** — one instance to rule them all

## Code Example
```python
"""E-commerce: Advanced patterns — plugin registry, pipeline, strategy."""

from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, ClassVar, Callable


# ─── Registry Pattern: auto-register export formats ───
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


# ─── Decorator + Generator: pipeline stage ───
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


# ─── Strategy Pattern ───
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


# ─── Usage ───
data = [
    {"name": "Laptop", "price": 1500},
    {"name": "Mouse", "price": 25},
    {"name": "Monitor", "price": 400},
]

# Registry
fmt = "csv"
exporter_cls = DataExporter.registry.get(fmt)
if exporter_cls:
    print(f"=== {fmt.upper()} Export ===")
    print(exporter_cls().export(data))

# Pipeline
gen = (item for item in data)
pipeline = filter_expensive(add_tax(gen))
print("\n=== Pipeline ===")
for item in pipeline:
    print(f"  {item['name']}: ${item['price_with_tax']}")

# Strategy
strategy = PercentageDiscount(10)
total = sum(item["price"] for item in data)
print(f"\nTotal: ${total:.2f} → after 10% off: ${strategy.calculate(total):.2f}")
```

## 🔍 How It Works
- **Registry**: `__init_subclass__` automatically registers every subclass by format name
- **Decorator + Generator**: `@pipeline_stage` marks a function that takes and returns a generator — each stage is a composable transformation
- **Strategy**: `DiscountStrategy` ABC defines the interface; concrete strategies implement it
- The pipeline pattern lets you chain stages: `filter → transform → accumulate`
- Registry + Strategy = find the right algorithm by name at runtime

## ⚠️ Common Pitfall
Over-engineering. Not every problem needs a pattern. Start with simple functions, refactor to patterns when you have 3+ variations of the same thing.

## 🧠 Memory Aid
"Patterns aren't goals — they're solutions to recurring problems. Registry = 'find me by name.' Strategy = 'swap algorithms.' Pipeline = 'chain transformations.'"

## 🏃 Try It
Add an `XmlExporter` to the registry pattern above. Create a `pipeline_stage` called `filter_category(gen, category)` that filters by category.

## 🔗 Related
- [Decorators Deep](01-decorators-deep.md) — decorator fundamentals
- [Generators Deep](02-generators-deep.md) — generator fundamentals
- [SOLID Principles](../07_oop/lessons/16-oop-solid.md) — OCP and DIP underpin these patterns

## ➡️ Next
[Typing Deep II](11-typing-deep-ii.md)
