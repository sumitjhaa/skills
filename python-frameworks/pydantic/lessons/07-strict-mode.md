# 🎯 Type Coercion & Strict Mode
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** How Pydantic coerces types, strict mode, `Strict*` types.

## Default Coercion

```python
class Item(BaseModel):
    name: str
    price: float
    quantity: int
    tags: list[str]

# All of these work by default:
Item(name="Book", price=19.99, quantity=3, tags=["a"])
Item(name="Book", price="19.99", quantity="3", tags=("a",))
Item(name="Book", price=19, quantity=True, tags=["a"])
```

## Strict Mode

```python
from pydantic import BaseModel, ConfigDict

class StrictItem(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str
    price: float
    quantity: int

StrictItem(name="Book", price="19.99", quantity=3)  # ❌ price must be float
```

## Strict Types

```python
from pydantic import BaseModel, StrictInt, StrictFloat, StrictStr

class StrictModel(BaseModel):
    name: StrictStr
    price: StrictFloat
    count: StrictInt
```

## Per-Field Strict

```python
from pydantic import Field

class Model(BaseModel):
    name: str
    id: int = Field(strict=True)  # Only this field is strict
```

| Input | Coerced (default) | Strict |
|-------|-------------------|--------|
| `"42"` → int | ✅ | ❌ |
| `True` → int | ✅ | ❌ |
| `(1,2)` → list | ✅ | ❌ |
| `19.99` → float from int | ✅ | ❌ |

<!-- 🤔 FastAPI uses Pydantic — strict mode prevents unexpected coercion in APIs. -->

## Run the Code

```bash
python code/07-strict-mode.py
```
