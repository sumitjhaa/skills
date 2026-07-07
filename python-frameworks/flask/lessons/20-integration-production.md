# 🏁 Integration: Full Production App
<!-- ⏱️ 30 min | 🔴 Advanced -->

**What You'll Learn:** Combine auth, API, uploads, email, tasks, caching, and Docker into one production-grade app.

## Features

- User auth with password hashing
- Role-based access (admin/user)
- Product CRUD with caching
- Order placement with stock management
- Background email notifications
- Cache with tag-based invalidation
- Admin dashboard with stats
- Health check & route listing

## Models

```python
class User(Model):
    username = Col("s", unique=True)
    email = Col("s", unique=True)
    pw = Col("s")
    role = Col("s", default="user")

class Product(Model):
    name = Col("s")
    price = Col("f")
    category = Col("s", default="general")
    stock = Col("i", default=0)

class Order(Model):
    user_id = Col("i")
    product_id = Col("i")
    quantity = Col("i", default=1)
    status = Col("s", default="pending")
```

## Architecture

```
┌──────────┐     ┌──────────┐     ┌─────────┐
│  Nginx   │────▶│ Gunicorn │────▶│ Flask   │
│ (proxy)  │     │ (workers)│     │ (app)   │
└──────────┘     └──────────┘     └─────────┘
                                       │
                          ┌────────────┼────────────┐
                          ▼            ▼            ▼
                     ┌────────┐  ┌────────┐  ┌────────┐
                     │Postgres│  │ Redis  │  │  Mail  │
                     │  (DB)  │  │(cache) │  │(SMTP)  │
                     └────────┘  └────────┘  └────────┘
```

## Routes Overview

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/auth/register` | - | Register |
| POST | `/auth/login` | - | Login |
| GET | `/auth/logout` | - | Logout |
| GET | `/auth/me` | user | Current user |
| GET | `/products` | - | List (cached) |
| POST | `/products` | admin | Create |
| GET | `/products/<id>` | - | Detail |
| POST | `/orders` | user | Place order |
| GET | `/orders` | user | My orders |
| GET | `/admin/users` | admin | User list |
| GET | `/admin/stats` | admin | Statistics |
| GET | `/health` | - | Health check |

## Key Pattern: Role Decorators

```python
def login_required(f):
    def wrapper(**kw):
        if not current_user:
            return {"error": "Unauthorized"}
        return f(**kw)
    return wrapper

def admin_required(f):
    def wrapper(**kw):
        if not current_user or current_user.get("role") != "admin":
            return {"error": "Admin required"}
        return f(**kw)
    return wrapper
```

## Key Pattern: Cache + DB

```python
@app.route("/products")
def list_products():
    cached = cache.get("products:all")
    if cached:
        return {"products": cached, "source": "cache"}
    prods = [{"id": p.id, "name": p.name, ...} for p in Product.all()]
    cache.set("products:all", prods, ttl=30, tags=["products"])
    return {"products": prods, "source": "db"}
```

## Run the Code

```bash
python code/20-integration-production.py
```

The demo registers users, logs in, creates products, places orders with background email, tests admin access, and verifies auth guards.
