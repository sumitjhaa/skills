"""Model configuration: frozen, extra fields, populate_by_name."""
from pydantic import BaseModel, Field, ConfigDict, ValidationError


class FrozenUser(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    age: int


class ExtraAllowed(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str


class ExtraForbid(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str


class ByName(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_name: str = Field(alias="username")


print("=== Model Configuration ===")

try:
    user = FrozenUser(name="Alice", age=30)
    user.name = "Bob"
except ValidationError as e:
    print(f"Frozen error: {e.errors()[0]['msg']}")

extra_user = ExtraAllowed(name="Alice", role="admin", active=True)
print(f"Extra allowed: {extra_user.model_dump()}")

try:
    ExtraForbid(name="Alice", role="admin")
except ValidationError as e:
    print(f"Extra forbid error: {e.errors()[0]['msg']}")

by_name = ByName(username="alice")
print(f"Populate by name: {by_name.model_dump()}")
