"""Nested models and lists of models."""
from pydantic import BaseModel


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class Item(BaseModel):
    name: str
    price: float
    quantity: int = 1


class Order(BaseModel):
    order_id: int
    customer: str
    shipping: Address
    items: list[Item]


order = Order(
    order_id=1001,
    customer="Alice",
    shipping={"street": "123 Main St", "city": "Portland", "zip_code": "97201"},
    items=[
        {"name": "Widget", "price": 9.99, "quantity": 3},
        {"name": "Gadget", "price": 24.99, "quantity": 1},
    ],
)

print("=== Nested Models ===")
print(f"Order {order.order_id} for {order.customer}")
print(f"Ship to: {order.shipping.street}, {order.shipping.city}")
print(f"Items:")
for item in order.items:
    print(f"  {item.quantity}x {item.name} @ ${item.price:.2f}")
total = sum(i.price * i.quantity for i in order.items)
print(f"Total: ${total:.2f}")
