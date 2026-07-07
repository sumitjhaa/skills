"""07-08-dataclasses.py — E-commerce: Product and Order dataclasses."""

from dataclasses import dataclass, field
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


@dataclass(frozen=True, order=True)
class Product:
    name: str
    price: float
    sku: str = field(repr=False, compare=False)
    category: str = "General"
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Order:
    order_id: str
    customer: str
    items: list[Product] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING

    def add_product(self, product: Product) -> None:
        self.items.append(product)

    @property
    def total(self) -> float:
        return sum(p.price for p in self.items)


p1 = Product("Gaming Laptop", 1499.99, "TECH-001", tags=["electronics"])
p2 = Product("Wireless Mouse", 29.99, "ACC-002", category="Accessories")

order = Order("ORD-001", "Alice")
order.add_product(p1)
order.add_product(p2)

print(order)
print(f"Total: ${order.total:.2f}")
print(f"p1 == p2: {p1 == p2}")
print(f"p1 < p2: {p1 < p2}")
