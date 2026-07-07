# 🏗️ Project Setup & First Endpoint
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create a FastAPI project, understand the structure, write the first endpoint, and run with Uvicorn.

## Install & Setup

```bash
pip install fastapi uvicorn
```

Minimal app (`main.py`):

```python
from fastapi import FastAPI

app = FastAPI(title="My First API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

<!-- 🤔 FastAPI reads return values as JSON automatically — no `json.dumps()` needed. -->

## Run the Server

```bash
uvicorn main:app --reload
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs
```

`main:app` = file `main.py`, variable `app`. `--reload` = auto-restart on code changes.

## Auto-generated Docs

FastAPI generates two API docs UIs from your code:

| URL | Tool | When to Use |
|-----|------|-------------|
| `/docs` | Swagger UI | Interactive testing |
| `/openapi.json` | Raw spec | CI, client generation |

<!-- 🧠 OpenAPI schema is built from your type annotations — zero extra work. -->

## Your First Endpoints

```python
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}
```

<!-- ⚡ Path parameters like `{item_id}` are automatically validated and type-converted. -->

## Project Structure

```
myapi/
├── main.py           # App instance + routes
├── requirements.txt  # fastapi[standard]
└── .gitignore
```

## Run the Code

```bash
python code/01-project-setup.py
```
