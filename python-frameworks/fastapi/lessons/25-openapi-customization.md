# 📖 OpenAPI Customization
<!-- ⏱️ 10 min | 🟢 Supplement -->

**What You'll Learn:** Custom schema metadata, operation IDs, tags, examples, servers.

## App-Level Metadata

```python
app = FastAPI(
    title="My API",
    description="Full API documentation",
    version="2.0.0",
    contact={"name": "Dev Team", "email": "dev@example.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
```

## Per-Operation Metadata

```python
@app.get(
    "/items",
    summary="List all items",
    description="Returns a paginated list with optional filtering",
    operation_id="listItems",
    tags=["items"],
    responses={200: {"description": "List of items"}},
)
def list_items():
    ...
```

## Tags

```python
@app.get("/users", tags=["users"])
def get_users(): ...

@app.post("/users", tags=["users"])
def create_user(): ...
```

Tags group endpoints in the Swagger UI.

## Custom Responses

```python
from fastapi import status
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
    code: int

@app.get(
    "/items/{id}",
    responses={
        404: {"model": ErrorResponse, "description": "Item not found"},
        403: {"model": ErrorResponse, "description": "Not authorized"},
    },
)
def get_item(id: int): ...
```

## Servers

```python
app = FastAPI(servers=[
    {"url": "https://api.example.com", "description": "Production"},
    {"url": "https://staging.example.com", "description": "Staging"},
])
```

## Run the Code

```bash
python code/25-openapi-customization.py
```
