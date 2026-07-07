"""07-02-methods.py — E-commerce: Order with instance, class, and static methods."""

class Order:
    tax_rate = 0.08

    def __init__(self, items: list[tuple[str, float]]):
        self.items = items

    def subtotal(self) -> float:
        return sum(price for _, price in self.items)

    def total(self) -> float:
        return self.subtotal() * (1 + self.tax_rate)

    @classmethod
    def from_cart(cls, cart_items: list[str], prices: dict[str, float]):
        items = [(item, prices[item]) for item in cart_items if item in prices]
        return cls(items)

    @staticmethod
    def is_valid_item(name: str, price: float) -> bool:
        return bool(name) and price > 0


order = Order([("Laptop", 1200), ("Mouse", 25)])
print(f"Subtotal: ${order.subtotal():.2f}")
print(f"Total: ${order.total():.2f}")

cart_order = Order.from_cart(
    ["Laptop", "Mouse", "Keyboard"],
    {"Laptop": 1200, "Mouse": 25, "Keyboard": 80},
)
print(f"Cart total: ${cart_order.total():.2f}")
print(f"Valid? {Order.is_valid_item('Headphones', 50)}")
