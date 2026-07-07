"""Error handling — catching, inspecting, customizing errors."""
from pydantic import BaseModel, Field, field_validator, ValidationError


class User(BaseModel):
    name: str = Field(min_length=2)
    email: str
    age: int = Field(ge=0, le=150)

    @field_validator("email")
    @classmethod
    def check_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Must contain @")
        if "." not in v.split("@")[-1]:
            raise ValueError("Must have valid domain")
        return v.lower()


print("=== Error Handling ===")

inputs = [
    {"name": "", "email": "alice@example.com", "age": 30},
    {"name": "Alice", "email": "not-an-email", "age": 30},
    {"name": "Alice", "email": "alice@example.com", "age": -5},
    {"name": "Alice", "email": "alice@example.com", "age": 200},
]

for i, data in enumerate(inputs, 1):
    try:
        user = User(**data)
        print(f"\nInput {i}: Valid -> {user.name}")
    except ValidationError as e:
        print(f"\nInput {i}: Invalid")
        for err in e.errors():
            field = ".".join(str(x) for x in err["loc"])
            print(f"  {field}: {err['msg']} (type={err['type']})")
