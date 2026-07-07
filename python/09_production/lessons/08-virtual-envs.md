# 🎯 Virtual Environments
<!-- ⏱️ 10 min read | 🟢 Core | 🧠 Applied -->

**What You'll Learn:** Create and manage virtual environments with `venv`, understand isolation, and use `requirements.txt` and `pip`.

> 💡 **TL;DR — The whole point:** Virtual environments isolate project dependencies so different projects can use different package versions without conflicts.

## 🔗 Why This Matters
Project A needs Django 4.2, Project B needs Django 5.0. Without virtual environments, you can only have one version installed globally. Virtual environments solve this by giving each project its own package directory.

## The Concept
- `python -m venv .venv` — create an environment
- `source .venv/bin/activate` — activate it (Linux/Mac)
- `.venv\Scripts\activate` — activate (Windows)
- `pip install requests` — install packages inside the environment
- `pip freeze > requirements.txt` — save exact versions
- `pip install -r requirements.txt` — recreate on another machine

## Code Example
```bash
# Create project
mkdir my_ecommerce && cd my_ecommerce

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate

# Check which Python is being used
which python  # Should show: my_ecommerce/.venv/bin/python

# Install dependencies
pip install fastapi uvicorn pydantic httpx

# Save exact versions
pip freeze > requirements.txt

# See what was saved
cat requirements.txt
```

```python
"""my_ecommerce/app.py — This runs inside the virtual environment."""

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    price: float


products_db: list[Product] = []


@app.get("/products")
def list_products() -> list[Product]:
    return products_db


@app.post("/products")
def create_product(product: Product) -> Product:
    products_db.append(product)
    return product


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```python
"""test_app.py — Tests run inside the virtual environment."""

from app import Product, products_db


def test_create_and_list():
    products_db.clear()
    p = Product(name="Laptop", price=1499.99)
    products_db.append(p)
    assert len(products_db) == 1
    assert products_db[0].name == "Laptop"
```

## 🔍 How It Works
- `venv` creates a `.venv/` directory with its own `bin/` (or `Scripts/` on Windows)
- Activation modifies `PATH` so `python` and `pip` point to the environment's versions
- `pip install` puts packages in `.venv/lib/python3.x/site-packages/`
- `deactivate` restores the original `PATH`
- VS Code and PyCharm auto-detect `.venv/` environments
- Never commit `.venv/` to git — add it to `.gitignore`

## ⚠️ Common Pitfall
Forgetting to activate the virtual environment before installing packages. You'll install globally instead. Check `which pip` to verify you're in the environment.

## 🧠 Memory Aid
"venv = `python -m venv .venv && source .venv/bin/activate`. `.venv/` goes in `.gitignore`. `requirements.txt` gets committed."

## 🏃 Try It
Create a new directory, set up a virtual environment, install `requests`, write a script that fetches `https://api.github.com`, and run it. Then `deactivate` and show that `requests` is no longer importable.

## 🔗 Related
- [Project Structure](01-project-structure.md) — organizing packages
- [Docker for Python](11-docker-python.md) — containers as isolated environments

## ➡️ Next
[Mutable, Identity & Copy](09-mutable-identity.md)
