"""Integration: settings + API schema + validation pipeline."""
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from typing import Literal
import json


class Settings(BaseModel):
    app_name: str = "PydanticDemo"
    debug: bool = False
    database_url: str = "sqlite:///dev.db"
    max_items_per_page: int = Field(default=100, ge=1, le=1000)

    @field_validator("database_url")
    @classmethod
    def check_url(cls, v: str) -> str:
        if not v.startswith(("sqlite://", "postgresql://", "mysql://")):
            raise ValueError("Unsupported database scheme")
        return v


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    role: Literal["admin", "user"] = "user"

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower()


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime


settings = Settings()
print("=== Integration: Settings & API Client ===")
print(f"Settings: {settings.model_dump()}")

try:
    Settings(database_url="bad://localhost/db")
except ValidationError as e:
    print(f"Settings error: {e.errors()[0]['msg']}")

input_data = {"name": "Alice", "email": "alice@example.com", "role": "admin"}
try:
    request = CreateUserRequest(**input_data)
    print(f"\nValidated request: {request.model_dump()}")

    response = UserResponse(
        id=1,
        name=request.name,
        email=request.email,
        role=request.role,
        created_at=datetime.now(),
    )
    print(f"API response: {response.model_dump_json(indent=2)}")
except ValidationError as e:
    print(f"Request error: {e.errors()}")

try:
    CreateUserRequest(name="", email="bad", role="superadmin")
except ValidationError as e:
    print(f"\nInvalid request errors:")
    for err in e.errors():
        field = ".".join(str(x) for x in err["loc"])
        print(f"  {field}: {err['msg']}")
