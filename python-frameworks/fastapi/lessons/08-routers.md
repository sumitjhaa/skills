# 🗂️ Routers & Modular Organization
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** `APIRouter`, splitting endpoints into modules, prefix/ tags/ dependencies.

## APIRouter

```python
# items.py
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    return [{"id": 1, "name": "Item 1"}]

@router.get("/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

<!-- 📦 Routers keep your code organized. One file per domain. -->

## Include in Main App

```python
# main.py
from fastapi import FastAPI
from items import router as items_router
from users import router as users_router

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)
```

## Router-Level Configuration

```python
router = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
    dependencies=[Depends(verify_token)],
    responses={404: {"detail": "Not found"}},
)
```

| Option | Effect |
|--------|--------|
| `prefix` | Prepends to all routes |
| `tags` | Groups in OpenAPI docs |
| `dependencies` | Applied to every route |
| `responses` | Default error responses |

## Multiple Files Structure

```
app/
├── main.py          # App + includes
├── routers/
│   ├── __init__.py
│   ├── items.py
│   └── users.py
```

## Run the Code

```bash
python code/08-routers.py
```
