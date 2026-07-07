# 📐 Field Types & Constraints
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** String constraints, numeric ranges, optional fields, defaults.

## Field Constraints

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0, le=99999.99)
    quantity: int = Field(ge=0, default=0)
    description: str | None = Field(None, max_length=500)
```

## Constrained Types

```python
from pydantic import BaseModel
from typing import Annotated
from pydantic import StringConstraints, Field

class Config(BaseModel):
    host: Annotated[str, StringConstraints(min_length=1, pattern=r"^\w+\.\w+$")]
    port: Annotated[int, Field(ge=1024, le=65535)]
```

## Common Field Options

| Option | Purpose |
|--------|---------|
| `default` | Default value |
| `default_factory` | Callable for default |
| `alias` | Alternative name |
| `gt`/`ge`/`lt`/`le` | Numeric bounds |
| `min_length`/`max_length` | String length |
| `pattern` | Regex validation |

## Optional Fields

```python
class Profile(BaseModel):
    nickname: str | None = None
    bio: str = ""
    tags: list[str] = []
```

<!-- 🤔 Python 3.10+ uses `str | None`. Python 3.8/9 uses `Optional[str]`. -->

## Run the Code

```bash
python code/02-field-types.py
```
