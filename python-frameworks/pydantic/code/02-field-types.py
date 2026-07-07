"""Field types and constraints."""
from pydantic import BaseModel, Field, ValidationError


class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0, le=99999.99)
    quantity: int = Field(ge=0, default=0)
    description: str | None = Field(None, max_length=500)


valid = Product(name="Laptop", price=999.99, quantity=5, description="A nice laptop")
print("=== Field Types & Constraints ===")
print(f"Valid: {valid.model_dump()}")

try:
    Product(name="AB", price=-1, quantity=-3)
except ValidationError as e:
    print(f"\nErrors:")
    for err in e.errors():
        print(f"  {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")
