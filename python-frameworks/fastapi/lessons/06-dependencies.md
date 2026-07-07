# 🔗 Dependencies
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** `Depends`, dependency injection, reusable logic, shared resources.

## Basic Dependency

```python
from fastapi import Depends

def common_params(q: str = "", limit: int = 10):
    return {"q": q, "limit": limit}

@app.get("/items")
def read_items(params: dict = Depends(common_params)):
    return params
```

<!-- 🧩 Dependencies are regular functions. FastAPI calls them and injects the result. -->

## Class Dependencies

```python
class Pagination:
    def __init__(self, offset: int = 0, limit: int = 10):
        self.offset = offset
        self.limit = limit

@app.get("/items")
def list_items(pag: Pagination = Depends()):
    return {"offset": pag.offset, "limit": pag.limit}
```

<!-- Classes with `__init__` parameters work as dependencies directly. -->

## Shared Resources (DB Sessions)

```python
def get_db():
    db = DatabaseSession()
    try:
        yield db  # FastAPI yields, then cleans up
    finally:
        db.close()

@app.get("/items")
def read_items(db: DatabaseSession = Depends(get_db)):
    return db.query("SELECT * FROM items")
```

<!-- 🔄 `yield` dependencies enable setup/teardown — perfect for DB connections. -->

## Dependency Tree

```python
def verify_token(token: str = Header(...)):
    return decode_token(token)

def get_current_user(token: dict = Depends(verify_token)):
    return get_user(token["sub"])

@app.get("/me")
def read_me(user: User = Depends(get_current_user)):
    return user
```

Dependencies can depend on other dependencies — FastAPI builds a DAG and resolves it.

## Global Dependencies

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

## Run the Code

```bash
python code/06-dependencies.py
```
