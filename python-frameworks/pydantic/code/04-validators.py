"""Field and model validators."""
from pydantic import BaseModel, field_validator, model_validator, ValidationError


class User(BaseModel):
    name: str
    email: str
    age: int

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Invalid email format")
        return v.lower()

    @field_validator("age")
    @classmethod
    def check_age(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be 0-150")
        return v

    @model_validator(mode="after")
    def check_name_email(self) -> "User":
        if self.name.lower() in self.email.lower():
            raise ValueError("Name should not be in email")
        return self


valid = User(name="Bob", email="alice@domain.com", age=30)
print("=== Validators ===")
print(f"Valid user: {valid.name}, {valid.email}")

try:
    User(name="Bob", email="bob", age=200)
except ValidationError as e:
    print(f"\nValidation errors:")
    for err in e.errors():
        print(f"  {'.'.join(str(x) for x in err['loc'])}: {err['msg']}")
