"""Request body, Pydantic models, field validation."""
from typing import Any, Optional
from datetime import datetime
import json
import re


# ======================== Pydantic-like Validation ========================

class Field:
    """Simulates Pydantic's Field with validation."""
    def __init__(self, default=None, *, ge=None, le=None, min_length=None, max_length=None, regex=None, description=""):
        self.default = default
        self.ge = ge
        self.le = le
        self.min_length = min_length
        self.max_length = max_length
        self.regex = regex
        self.description = description

    def validate(self, value, name: str) -> list[str]:
        errors = []
        if value is None and self.default is not None:
            return errors
        if isinstance(value, (int, float)):
            if self.ge is not None and value < self.ge:
                errors.append(f"{name}: ensure this value >= {self.ge}")
            if self.le is not None and value > self.le:
                errors.append(f"{name}: ensure this value <= {self.le}")
        if isinstance(value, str):
            if self.min_length is not None and len(value) < self.min_length:
                errors.append(f"{name}: ensure this value has at least {self.min_length} characters")
            if self.max_length is not None and len(value) > self.max_length:
                errors.append(f"{name}: ensure this value has at most {self.max_length} characters")
            if self.regex is not None and not re.match(self.regex, value):
                errors.append(f"{name}: string does not match regex {self.regex}")
        return errors


class BaseModel:
    """Simulates Pydantic's BaseModel."""
    def __init__(self, **data):
        self._errors: list[str] = []
        for name, field_info in self._fields().items():
            value = data.get(name, field_info.default)
            setattr(self, name, value)
            errs = field_info.validate(value, name)
            self._errors.extend(errs)

    @classmethod
    def _fields(cls) -> dict[str, Field]:
        fields = {}
        for name in dir(cls):
            attr = getattr(cls, name, None)
            if isinstance(attr, Field):
                fields[name] = attr
        return fields

    def is_valid(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> list[str]:
        return self._errors

    def dict(self) -> dict:
        return {k: getattr(self, k) for k in self._fields()}


# ======================== Pydantic Models ========================

class Item(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(default="", max_length=200)
    price: float = Field(ge=0.0, le=100000.0)
    tax: float = Field(default=0.0, ge=0.0, le=0.5)


class User(BaseModel):
    username: str = Field(min_length=3, max_length=20, regex=r"^[a-zA-Z0-9_]+$")
    email: str = Field(regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    age: int = Field(ge=0, le=150)
    is_active: bool = Field(default=True)


class Order(BaseModel):
    item_id: int = Field(ge=1)
    quantity: int = Field(ge=1, le=100)
    shipping_address: str = Field(min_length=10, max_length=200)
    notes: str = Field(default="")


# ======================== Validation Demo ========================
print("=== Pydantic Validation Demo ===\n")

# --- Valid item ---
print("1. Valid item:")
item = Item(name="Laptop", description="Gaming laptop", price=999.99, tax=0.08)
print(f"   Valid: {item.is_valid()}")
print(f"   Data: {item.dict()}")

# --- Invalid item ---
print("\n2. Invalid item (short name, negative price):")
item2 = Item(name="AB", price=-100.0)
print(f"   Valid: {item2.is_valid()}")
print(f"   Errors: {item2.errors}")

# --- Valid user ---
print("\n3. Valid user:")
user = User(username="alice_01", email="alice@example.com", age=30)
print(f"   Valid: {user.is_valid()}")
print(f"   Data: {user.dict()}")

# --- Invalid user ---
print("\n4. Invalid user (bad email, bad username):")
user2 = User(username="a b", email="not-an-email", age=200)
print(f"   Valid: {user2.is_valid()}")
print(f"   Errors: {user2.errors}")

# --- Valid order ---
print("\n5. Valid order:")
order = Order(item_id=42, quantity=3, shipping_address="123 Main St, City, Country")
print(f"   Valid: {order.is_valid()}")
print(f"   Data: {order.dict()}")

# --- Invalid order ---
print("\n6. Invalid order:")
order2 = Order(item_id=0, quantity=200, shipping_address="Short")
print(f"   Valid: {order2.is_valid()}")
print(f"   Errors: {order2.errors}")

# --- JSON serialization ---
print("\n7. JSON serialization:")
print(json.dumps(item.dict(), indent=2))
