"""Phase 07 Integration: E-Commerce Order System
Combines: classes, inheritance, ABC, dunders, properties, dataclasses, composition, metaclasses, enums, SOLID.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar


# ─── Enum (Lesson 15) ───
class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()


# ─── Dataclass (Lesson 08) ───
@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: float
    category: str = "General"
    weight_kg: float = 0.0


# ─── Properties (Lesson 06) + Encapsulation (Lesson 07) ───
class ShoppingCart:
    def __init__(self):
        self._items: dict[str, dict] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        sku = product.sku
        if sku in self._items:
            self._items[sku]["qty"] += quantity
        else:
            self._items[sku] = {"product": product, "qty": quantity}

    def remove(self, sku: str) -> None:
        self._items.pop(sku, None)

    @property
    def total(self) -> float:
        return sum(item["product"].price * item["qty"] for item in self._items.values())

    @property
    def item_count(self) -> int:
        return sum(item["qty"] for item in self._items.values())

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())


# ─── ABC (Lesson 04) ───
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str = "USD") -> str:
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float, currency: str = "USD") -> str:
        fee = amount * 0.029
        return f"[Stripe] Charged {currency} ${amount:.2f} (fee: ${fee:.2f})"


class PayPalGateway(PaymentGateway):
    def charge(self, amount: float, currency: str = "USD") -> str:
        fee = amount * 0.039
        return f"[PayPal] Charged {currency} ${amount:.2f} (fee: ${fee:.2f})"


# ─── Composition (Lesson 09) ───
class ShippingService:
    def __init__(self, carrier: str, rate_per_kg: float):
        self.carrier = carrier
        self.rate_per_kg = rate_per_kg

    def calculate(self, total_kg: float) -> float:
        return max(total_kg * self.rate_per_kg, 5.0)  # minimum $5

    def ship(self, total_kg: float) -> str:
        cost = self.calculate(total_kg)
        return f"[{self.carrier}] Shipping {total_kg:.1f}kg for ${cost:.2f}"


# ─── Inheritance (Lesson 03) + Dunders (Lesson 05) ───
class Order:
    def __init__(self, cart: ShoppingCart, payment: PaymentGateway, shipping: ShippingService):
        self._cart = cart
        self._payment = payment
        self._shipping = shipping
        self.status = OrderStatus.PENDING
        self._order_id = id(self)

    @property
    def total_with_shipping(self) -> float:
        shipping_cost = self._shipping.calculate(
            sum(item["product"].weight_kg * item["qty"] for item in self._cart)
        )
        return self._cart.total + shipping_cost

    def place(self) -> str:
        total_weight = sum(
            item["product"].weight_kg * item["qty"] for item in self._cart
        )
        ship_result = self._shipping.ship(total_weight)
        pay_result = self._payment.charge(self.total_with_shipping)
        self.status = OrderStatus.PAID
        return f"{pay_result}\n{ship_result}\nOrder {self._order_id} placed!"

    def __str__(self) -> str:
        return f"Order({self._order_id}): {self.status.name}, ${self.total_with_shipping:.2f}"

    def __repr__(self) -> str:
        return f"Order(id={self._order_id}, status={self.status.name})"


# ─── SOLID: SRP (Lesson 16) — separate notification ───
class NotificationService:
    @staticmethod
    def send_confirmation(order: Order) -> str:
        return f"[Email] Order {order._order_id} confirmed — status: {order.status.name}"


# ─── Main ───
if __name__ == "__main__":
    products = [
        Product("LAP-001", "Gaming Laptop", 1499.99, "Electronics", 2.5),
        Product("MOU-001", "Wireless Mouse", 29.99, "Accessories", 0.2),
        Product("KEY-001", "Mechanical Keyboard", 89.99, "Accessories", 0.8),
    ]

    cart = ShoppingCart()
    cart.add(products[0])
    cart.add(products[1], 2)
    cart.add(products[2])

    print(f"Cart: {cart.item_count} items, total: ${cart.total:.2f}")
    for item in cart:
        p = item["product"]
        print(f"  {p.name} × {item['qty']} @ ${p.price:.2f}")

    order = Order(cart, StripeGateway(), ShippingService("FedEx", 2.50))
    print(f"\n{order.place()}")
    print(order)

    NotificationService.send_confirmation(order)
