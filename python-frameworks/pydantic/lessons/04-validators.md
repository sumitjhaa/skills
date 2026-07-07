# ✅ Validators
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Field validators, model validators, pre/post validation.

## Field Validators

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email")
        return v.lower()
```

## Multiple Field Validator

```python
@field_validator("name", "email")
@classmethod
def not_empty(cls, v: str) -> str:
    if not v.strip():
        raise ValueError("Cannot be empty")
    return v.strip()
```

## Model Validator

```python
from pydantic import model_validator

class Order(BaseModel):
    items: list[str]
    discount: float = 0.0
    total: float

    @model_validator(mode="after")
    def check_discount(self) -> "Order":
        if self.discount > 0 and len(self.items) < 2:
            raise ValueError("Discount requires 2+ items")
        return self
```

## Pre vs Post Validators

```python
@field_validator("field", mode="before")  # Runs before type coercion
@field_validator("field", mode="after")   # Runs after type coercion (default)
```

<!-- 🧠 Use `mode="before"` to normalize input, `mode="after"` for business rules. -->

## Run the Code

```bash
python code/04-validators.py
```
