"""Pydantic basics — BaseModel, validation, model_dump."""
from pydantic import BaseModel, ValidationError


class User(BaseModel):
    name: str
    email: str
    age: int


user = User(name="Alice", email="alice@test.com", age=30)
print("=== Pydantic Basics ===")
print(f"User: {user.name}, {user.email}, {user.age}")
print(f"Dict: {user.model_dump()}")
print(f"JSON: {user.model_dump_json()}")

try:
    User(name="", email="bad", age=-5)
except ValidationError as e:
    print(f"\nValidation error: {e.errors()}")
