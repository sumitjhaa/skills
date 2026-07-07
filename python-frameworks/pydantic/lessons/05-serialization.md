# 📦 Serialization
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** model_dump, model_dump_json, include/exclude, aliases.

## Dumping to Dict

```python
user = User(name="Alice", age=30, roles=["admin", "user"])

data = user.model_dump()
# {"name": "Alice", "age": 30, "roles": ["admin", "user"]}

data = user.model_dump(include={"name", "age"})
# {"name": "Alice", "age": 30}

data = user.model_dump(exclude={"roles"})
# {"name": "Alice", "age": 30}
```

## Dumping to JSON

```python
json_str = user.model_dump_json()
json_str = user.model_dump_json(indent=2)
json_str = user.model_dump_json(exclude_none=True)
```

## Aliases

```python
class User(BaseModel):
    full_name: str = Field(alias="fullName")
    is_active: bool = Field(alias="isActive", default=True)

user = User(**{"fullName": "Alice", "isActive": True})
user.model_dump(by_alias=True)  # {"fullName": "Alice", "isActive": True}
```

## Serialization Options

| Option | Effect |
|--------|--------|
| `include` | Fields to include |
| `exclude` | Fields to exclude |
| `by_alias` | Use alias names |
| `exclude_unset` | Omit unset defaults |
| `exclude_none` | Omit None values |
| `round_trip` | Dump → load roundtrip |

<!-- 🤔 Use `by_alias=True` when serializing for external APIs. -->

## Run the Code

```bash
python code/05-serialization.py
```
