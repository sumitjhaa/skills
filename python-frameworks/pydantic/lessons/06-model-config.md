# ⚙️ Model Configuration
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** ConfigDict, frozen models, extra fields, arbitrary types.

## Frozen Models

```python
from pydantic import BaseModel, ConfigDict

class ImmutableUser(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    age: int

user = ImmutableUser(name="Alice", age=30)
user.name = "Bob"  # ❌ ValidationError: Frozen instance
```

## Extra Fields

```python
class StrictUser(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str

class AllowExtra(BaseModel):
    model_config = ConfigDict(extra="allow")
    name: str

user = AllowExtra(name="Alice", role="admin")
user.extra_role  # "admin" — stored on the model
```

## Populate by Name

```python
class Model(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    user_name: str = Field(alias="username")
```

## Arbitrary Types

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Event(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str
    timestamp: datetime
```

<!-- 🤔 `extra="forbid"` is recommended for API schemas to catch typos. -->

## Run the Code

```bash
python code/06-model-config.py
```
