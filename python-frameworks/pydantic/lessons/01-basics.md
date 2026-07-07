# 🏗️ Pydantic Basics
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create your first Pydantic model, validate fields, handle errors.

## BaseModel

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@test.com", age=30)
print(user)  # name='Alice' email='alice@test.com' age=30
```

## Automatic Validation

```python
user = User(name="Bob", email="bob@test.com", age="25")  # str → int coercion
user = User(name="Charlie", email="not-email", age=20)   # Try it — what happens?
```

## ValidationError

```python
from pydantic import ValidationError

try:
    User(name="X", email="bad", age=-5)
except ValidationError as e:
    print(e)
```

## Field Access

```python
user.name      # "Alice"
user.email     # "alice@test.com"
user.age       # 30
user.model_dump()    # {"name": "Alice", "email": "alice@test.com", "age": 30}
user.model_dump_json()  # JSON string
```

<!-- 🤔 Fields are type-validated on instantiation. Wrong types raise ValidationError. -->

## Run the Code

```bash
python code/01-basics.py
```
