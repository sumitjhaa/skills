# 📤 Response Models
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Control response shapes with `response_model`, filter sensitive fields, and use model aliases.

## Response Model

```python
from pydantic import BaseModel

class ItemOut(BaseModel):
    name: str
    price: float

@app.post("/items", response_model=ItemOut)
def create_item(item: Item):
    return item  # Only name + price returned
```

<!-- 🔐 `response_model` strips fields not declared in the output model — hide internal fields automatically. -->

## Filter Sensitive Data

```python
class UserOut(BaseModel):
    username: str
    email: str

class UserInDB(UserOut):
    hashed_password: str  # Omitted from response

@app.post("/users", response_model=UserOut)
def create_user(user: UserInDB):
    save_to_db(user)
    return user  # hashed_password is auto-stripped
```

<!-- 🛡️ Never return passwords. `response_model` acts as your serialization firewall. -->

## Response Status Codes

```python
@app.post("/items", status_code=201)
def create_item(item: Item):
    return save_to_db(item)

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    delete_from_db(item_id)
```

## Multiple Models for One Endpoint

```python
from typing import Union

@app.get("/items/{item_id}", response_model=Union[ItemOut, ErrorOut])
def read_item(item_id: int):
    item = get_from_db(item_id)
    if item is None:
        return ErrorOut(detail="Not Found")
    return item
```

<!-- ⚡ `Union[ModelA, ModelB]` — FastAPI picks the first matching schema for the response. -->

## Run the Code

```bash
python code/04-response-models.py
```
