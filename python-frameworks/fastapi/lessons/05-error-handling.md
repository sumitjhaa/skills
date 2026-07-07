# ❌ Error Handling
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** HTTP exceptions, validation error handling, custom exception handlers, and error responses.

## HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]
```

<!-- 🚨 `raise HTTPException` instantly stops the request and returns a structured error response. -->

## Custom Status Codes & Headers

```python
raise HTTPException(
    status_code=401,
    detail="Invalid credentials",
    headers={"X-Error": "auth"},
)
```

## Validation Errors (422)

FastAPI returns `422` automatically when type validation fails:

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "Input should be a valid number",
      "type": "float_parsing"
    }
  ]
}
```

## Custom Exception Handler

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

<!-- 🎯 Catch domain-specific exceptions and return clean error responses. -->

## Run the Code

```bash
python code/05-error-handling.py
```
