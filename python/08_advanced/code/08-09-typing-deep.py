"""08-09-typing-deep.py — E-commerce: TypedDict, Generic, Protocol, Literal, overload."""

from typing import TypeVar, Generic, TypedDict, Literal, overload, Protocol


class ProductDict(TypedDict):
    sku: str
    name: str
    price: float
    category: str


class PricedItem(Protocol):
    price: float


T = TypeVar("T")


class ShoppingCart(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def remove(self, item: T) -> None:
        self._items.remove(item)

    def total(self) -> float:
        return sum(i.price for i in self._items)

    def __len__(self) -> int:
        return len(self._items)


def total_price(items: list[PricedItem]) -> float:
    return sum(item.price for item in items)


@overload
def apply_discount(price: float, percent: float) -> float: ...


@overload
def apply_discount(price: list[float], percent: float) -> list[float]: ...


def apply_discount(price: float | list[float], percent: float) -> float | list[float]:
    if isinstance(price, list):
        return [p * (1 - percent / 100) for p in price]
    return price * (1 - percent / 100)


def set_shipping(method: Literal["standard", "express", "overnight"]) -> str:
    costs = {"standard": 5.99, "express": 14.99, "overnight": 29.99}
    return f"{method}: ${costs[method]}"


class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


cart: ShoppingCart[Product] = ShoppingCart()
cart.add(Product("Laptop", 1499.99))
cart.add(Product("Mouse", 29.99))
print(f"Cart: ${cart.total():.2f}")

print(f"Discount: ${apply_discount(100.0, 10):.2f}")
print(f"Bulk: {apply_discount([100, 200, 50], 10)}")
print(set_shipping("express"))
