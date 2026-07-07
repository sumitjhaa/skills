# 🧭 Path & Query Parameters
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Path parameters with types, query parameters, defaults, optional params, and validation.

## Path Parameters

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

<!-- 🔢 Type-annotated path params are auto-validated. `item_id: int` rejects non-integer input with 422. -->

Multiple path params:

```python
@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}
```

## Query Parameters

Function parameters *not* in the path become query parameters:

```python
@app.get("/search")
def search_items(q: str = "", limit: int = 10, offset: int = 0):
    return {"results": [f"Result {i}" for i in range(limit)]}
```

<!-- Hit `/search?q=python&limit=5&offset=0` to test. -->

| Type | Behavior |
|------|----------|
| `str` = `""` | Optional, default empty |
| `int` = `10` | Optional, default `10` |
| `int` | Required (no default) |
| `bool` | `true`/`1`/`yes` accepted |

## Type Coercion

FastAPI automatically converts strings from the URL to declared Python types. Invalid conversions return a `422` validation error.

```python
@app.get("/products")
def list_products(category: str = "", min_price: float = 0.0, max_price: float = 999999.0, in_stock: bool = True):
    return {"category": category, "in_stock": in_stock}
```

<!-- 🛡️ `float` params like `min_price=abc` → `422`. Always test edge cases. -->

## Run the Code

```bash
python code/02-path-query-params.py
```
