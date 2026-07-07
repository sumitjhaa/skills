"""07-16-oop-solid.py — SOLID principles with e-commerce discount system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


@dataclass
class Order:
    items: list[tuple[str, float]]

    def total(self) -> float:
        return sum(price for _, price in self.items)


class OrderRepository:
    @staticmethod
    def save(order: Order) -> None:
        print(f"[DB] Saving order: ${order.total():.2f}")


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, total: float) -> float:
        return total * (1 - self.percent / 100)


class BogoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.5


class OrderProcessor:
    def __init__(self, discount: DiscountStrategy):
        self.discount = discount

    def process(self, order: Order) -> float:
        total = self.discount.apply(order.total())
        OrderRepository.save(order)
        return total


class Shippable(Protocol):
    def weight_kg(self) -> float: ...


class Trackable(Protocol):
    def tracking_info(self) -> str: ...


class PhysicalProduct:
    def weight_kg(self) -> float:
        return 2.5

    def tracking_info(self) -> str:
        return "TRACK-123"


class DigitalProduct:
    def weight_kg(self) -> float:
        return 0.0


order = Order([("Laptop", 1500), ("Mouse", 30)])
processor = OrderProcessor(PercentageDiscount(10))
final = processor.process(order)
print(f"Final total: ${final:.2f}")
