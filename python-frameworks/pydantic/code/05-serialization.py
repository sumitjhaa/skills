"""Serialization: model_dump, JSON, include/exclude, aliases."""
from pydantic import BaseModel, Field
from datetime import datetime


class User(BaseModel):
    full_name: str = Field(alias="fullName")
    email: str
    age: int
    roles: list[str] = []
    created_at: datetime | None = None


user = User(**{
    "fullName": "Alice Johnson",
    "email": "alice@example.com",
    "age": 30,
    "roles": ["admin", "user"],
    "created_at": "2025-01-15T10:30:00",
})

print("=== Serialization ===")
print(f"Default dump:")
print(f"  {user.model_dump()}")

print(f"\nWith alias:")
print(f"  {user.model_dump(by_alias=True)}")

print(f"\nInclude only (name, email):")
print(f"  {user.model_dump(include={'full_name', 'email'})}")

print(f"\nExclude roles:")
print(f"  {user.model_dump(exclude={'roles'})}")

print(f"\nJSON (indented):")
print(f"  {user.model_dump_json(indent=2)}")

print(f"\nExclude None:")
print(f"  {user.model_dump(exclude_none=True)}")
