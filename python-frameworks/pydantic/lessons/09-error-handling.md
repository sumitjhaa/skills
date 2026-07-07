# ⚠️ Error Handling
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Catching ValidationError, accessing error details, custom errors.

## Catching Validation Errors

```python
from pydantic import ValidationError

try:
    User(name="", email="bad", age=-1)
except ValidationError as e:
    print(e.errors())  # List of dicts with error details
```

## Error Structure

```python
[
    {
        "type": "string_too_short",
        "loc": ("name",),
        "msg": "String should have at least 1 character",
        "input": "",
        "ctx": {"min_length": 1},
    },
    {
        "type": "value_error",
        "loc": ("email",),
        "msg": "Value error, Invalid email format",
        "input": "bad",
    },
]
```

## Selective Error Handling

```python
try:
    User(name="", email="bad", age=-5)
except ValidationError as e:
    for error in e.errors():
        field = ".".join(str(x) for x in error["loc"])
        msg = error["msg"]
        print(f"  {field}: {msg}")
```

## Raising From Validators

```python
@field_validator("age")
@classmethod
def check_age(cls, v: int) -> int:
    if v < 0:
        raise ValueError("Age cannot be negative")
    if v > 150:
        raise ValueError("Age seems unrealistic")
    return v
```

## Error Types

| Type | Meaning |
|------|---------|
| `missing` | Required field not provided |
| `string_too_short` | Below min_length |
| `less_than_equal` | Above numeric bound |
| `value_error` | Custom validator failure |
| `json_invalid` | Invalid JSON input |

<!-- 🤔 Use `e.errors(include_url=False)` to omit documentation links. -->

## Run the Code

```bash
python code/09-error-handling.py
```
