"""Pydantic & Settings — E-commerce order validation with Pydantic v2.
Run: python 09-13-pydantic-settings.py
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum


class Settings(BaseSettings):
    app_name: str = "E-Commerce API"
    debug: bool = False
    database_url: str = "sqlite:///./ecommerce.db"
    redis_url: Optional[str] = None
    jwt_secret: str = Field(default="change-me-change-me", min_length=16)
    api_key: str = ""

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith(("sqlite", "postgresql", "mysql")):
            raise ValueError("Unsupported database URL scheme")
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
print(f"App: {settings.app_name}, DB: {settings.database_url}")


class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class Address(BaseModel):
    street: str = Field(min_length=5)
    city: str
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")


class OrderItem(BaseModel):
    sku: str = Field(pattern=r"^[A-Z]{3,4}-\d{3}$")
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, le=100_000)
    quantity: int = Field(default=1, ge=1, le=100)


class CreateOrderRequest(BaseModel):
    customer_email: str
    items: list[OrderItem] = Field(min_length=1)
    shipping_address: Address
    coupon: Optional[str] = None

    @field_validator("customer_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()

    @model_validator(mode="after")
    def check_order_total(self) -> "CreateOrderRequest":
        total = sum(item.price * item.quantity for item in self.items)
        if total > 10_000:
            raise ValueError("Order exceeds $10,000 limit")
        return self


try:
    order = CreateOrderRequest(
        customer_email="alice@example.com",
        items=[
            OrderItem(sku="LAP-001", name="Laptop", price=1499.99),
            OrderItem(sku="MOU-001", name="Mouse", price=29.99, quantity=2),
        ],
        shipping_address=Address(street="123 Main St", city="Portland", zip_code="97201"),
    )
    print(f"Valid order: {order.customer_email}, {len(order.items)} items")
except Exception as e:
    print(f"Validation error: {e}")

try:
    CreateOrderRequest(
        customer_email="bad-email",
        items=[OrderItem(sku="BAD", name="", price=-1)],
        shipping_address=Address(street="1", city="", zip_code="abc"),
    )
except Exception as e:
    print(f"Validation error: {e}")
