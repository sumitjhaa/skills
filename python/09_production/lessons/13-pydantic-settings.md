# 🎯 Pydantic & Settings
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Use Pydantic for data validation, `BaseSettings` for configuration, `.env` loading, and custom validators.

> 💡 **TL;DR — The whole point:** Pydantic validates your data at runtime. `BaseSettings` loads config from environment variables, `.env` files, and defaults — with type coercion and validation.

## 🔗 Why This Matters
API request bodies need validation — is the email valid? Is the price positive? Pydantic catches invalid data early with clear error messages. `BaseSettings` manages environment config without `os.getenv()` clutter.

## The Concept
- `BaseModel` — validates data and converts types
- `BaseSettings` — loads from env vars, `.env` files, with priority layering
- `Field()` — add constraints (min, max, description, alias)
- `validator` / `field_validator` — custom validation logic
- `model_config` — Pydantic v2 configuration

## Code Example
```python
"""E-commerce: Pydantic models for API requests and config."""

from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum


# ─── Settings ───
class Settings(BaseSettings):
    app_name: str = "E-Commerce API"
    debug: bool = False
    database_url: str = "sqlite:///./ecommerce.db"
    redis_url: Optional[str] = None
    jwt_secret: str = Field(default="change-me", min_length=16)
    api_key: str = ""

    @field_validator("database_url")
    @classmethod
    def validate_db_url(cls, v: str) -> str:
        if not v.startswith(("sqlite", "postgresql", "mysql")):
            raise ValueError("Unsupported database URL scheme")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
print(f"App: {settings.app_name}, DB: {settings.database_url}")


# ─── Request Models ───
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


# ─── Usage ───
try:
    order = CreateOrderRequest(
        customer_email="alice@example.com",
        items=[
            OrderItem(sku="LAP-001", name="Laptop", price=1499.99),
            OrderItem(sku="MOU-001", name="Mouse", price=29.99, quantity=2),
        ],
        shipping_address=Address(street="123 Main St", city="Portland", zip_code="97201"),
    )
    print(f"\nValid order: {order.customer_email}, {len(order.items)} items")
except Exception as e:
    print(f"Validation error: {e}")

# Invalid order
try:
    CreateOrderRequest(
        customer_email="bad-email",  # no @
        items=[OrderItem(sku="BAD", name="", price=-1)],  # invalid field
        shipping_address=Address(street="1", city="", zip_code="abc"),  # too short
    )
except Exception as e:
    print(f"\nValidation error: {e}")
```

## 🔍 How It Works
- `BaseSettings` reads from: `.env` file → environment variables → defaults
- `Field(gt=0)` adds constraints — Pydantic validates these automatically
- `@field_validator` runs after type coercion for a single field
- `@model_validator(mode="after")` runs after all fields are validated
- `pattern=r"^\d{5}"` validates regex patterns
- Invalid data produces a detailed `ValidationError` with field paths

## ⚠️ Common Pitfall
Exposing `Settings()` as a module global that reads `.env` at import time. If the `.env` file isn't available during import (e.g., in tests), you get `ValidationError`. Use `lazy_settings` or a factory function.

## 🧠 Memory Aid
"Pydantic = data validator. `BaseModel` = schema + validation. `BaseSettings` = env config. `Field` = constraints. `validator` = custom logic."

## 🏃 Try It
Create a `UserRegistration` model with `username` (3-30 chars, alphanumeric), `email` (valid email), `password` (min 8 chars, must contain a number). Add a `model_validator` that checks password != username.

## 🔗 Related
- [Testing with pytest](04-testing-pytest.md) — testing models
- [FastAPI Deep](../10_ecosystem/lessons/09-fastapi-deep.md) — FastAPI + Pydantic

## ➡️ Next
[HTTPX & Requests Deep](14-httpx-requests-deep.md)
