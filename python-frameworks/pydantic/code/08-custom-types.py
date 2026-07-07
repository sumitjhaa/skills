"""Custom types, TypeAdapter, generic models."""
from pydantic import BaseModel, TypeAdapter, GetCoreSchemaHandler, ValidationError
from pydantic_core import core_schema
from typing import Generic, TypeVar


class PositiveInt:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        schema = handler(int)
        return core_schema.no_info_after_validator_function(cls.validate, schema)

    @classmethod
    def validate(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Must be positive")
        return v


class Product(BaseModel):
    name: str
    quantity: PositiveInt


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    status: str
    data: T
    message: str = ""


class UserOut(BaseModel):
    id: int
    name: str
    email: str


print("=== Custom Types & Generics ===")

p = Product(name="Widget", quantity=5)
print(f"Custom type: {p.model_dump()}")

try:
    Product(name="Widget", quantity=-1)
except ValidationError as e:
    print(f"PositiveInt error: {e.errors()[0]['msg']}")

adapter = TypeAdapter(list[int])
result = adapter.validate_python(["1", "2", "3"])
print(f"TypeAdapter: {result}")

resp = ApiResponse[UserOut](
    status="ok",
    data={"id": 1, "name": "Alice", "email": "a@b.com"},
)
print(f"Generic response: {resp.model_dump()}")
