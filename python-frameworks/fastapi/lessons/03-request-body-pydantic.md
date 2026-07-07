# 📦 Request Body & Pydantic Models
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Define Pydantic models, receive JSON request bodies, and validate fields.

## Pydantic Models

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = ""
    price: float
    tax: float = 0.0
```

<!-- Pydantic is FastAPI's validation engine. Each field type is enforced at runtime. -->

## Using in Endpoints

```python
@app.post("/items")
def create_item(item: Item):
    return {"name": item.name, "price": item.price, "id": 42}
```

FastAPI reads the JSON body, validates it against the model, and passes the instance.

<!-- 🔄 Request body → validated model → handler. One step, zero boilerplate. -->

## Field Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    price: float = Field(ge=0.0, le=100000.0)
    tax: float = Field(default=0.0, ge=0.0, le=0.5)
```

| Constraint | Applies To | Example |
|------------|-----------|---------|
| `min_length` / `max_length` | `str` | `Field(min_length=3)` |
| `ge` / `le` | `int`, `float` | `Field(ge=0)` |
| `regex` | `str` | `Field(regex=r"^\w+$")` |
| `default` | Any | `Field(default=False)` |

## Nested Models

```python
class Tag(BaseModel):
    name: str
    color: str

class Item(BaseModel):
    name: str
    tags: list[Tag] = []
```

<!-- 📦 Models can nest arbitrarily deep. FastAPI validates the full tree. -->

## Run the Code

```bash
python code/03-request-body-pydantic.py
```
