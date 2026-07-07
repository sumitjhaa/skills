# 🔄 Nested Models
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Models within models, lists of models, recursive models.

## Embedding Models

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

user = User(name="Alice", address={"street": "123 Main", "city": "NYC", "zip_code": "10001"})
print(user.address.city)  # "NYC"
```

## Lists of Models

```python
class Order(BaseModel):
    items: list[Item]

order = Order(items=[
    {"name": "Laptop", "price": 999.99, "quantity": 1},
    {"name": "Mouse", "price": 29.99, "quantity": 2},
])
```

## Deep Nesting

```python
class Company(BaseModel):
    name: str
    employees: list[User]
    headquarters: Address
```

## Recursive Models

```python
class Category(BaseModel):
    name: str
    children: list["Category"] = []

Category.model_rebuild()  # Resolve forward refs
```

<!-- 🤔 Dicts are auto-coerced to model instances when assigned to fields. -->

## Run the Code

```bash
python code/03-nested-models.py
```
