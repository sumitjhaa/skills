"""Type coercion and strict mode."""
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class Relaxed(BaseModel):
    name: str
    price: float
    count: int
    tags: list[str]


class Strict(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    price: float
    count: int


class MixedStrict(BaseModel):
    name: str
    count: int = Field(strict=True)


print("=== Type Coercion & Strict Mode ===")

r = Relaxed(name="Book", price="19.99", count="3", tags=("fiction",))
print(f"Relaxed: {r.model_dump()}")

try:
    s = Strict(name="Book", price="19.99", count=3)
except ValidationError as e:
    print(f"\nStrict mode errors:")
    for err in e.errors():
        print(f"  {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")

m = MixedStrict(name="Book", count=3)
print(f"\nMixed strict: {m.model_dump()}")

try:
    MixedStrict(name="Book", count="3")
except ValidationError as e:
    print(f"Mixed strict error (count as str): {e.errors()[0]['msg']}")
