# 🧰 Custom Types & Generics
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** TypeAdapter, custom types with `__get_pydantic_core_schema__`, generic models.

## TypeAdapter

Validate single values without a full model:

```python
from pydantic import TypeAdapter

positive_int = TypeAdapter(int).validate_python("42")
emails = TypeAdapter(list[str]).validate_python(["a@b.com", "c@d.com"])
```

## Custom Validated Type

```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

class PositiveInt:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: type, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        schema = handler(int)
        return core_schema.no_info_after_validator_function(
            cls.validate, schema
        )

    @classmethod
    def validate(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Must be positive")
        return v
```

## Generic Models

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    status: str
    data: T
    message: str = ""

user_resp = Response[User](status="ok", data={"name": "Alice", "age": 30})
order_resp = Response[Order](status="ok", data={"total": 99.99})
```

<!-- 🧠 Generics preserve type information through serialization and validation. -->

## Run the Code

```bash
python code/08-custom-types.py
```
