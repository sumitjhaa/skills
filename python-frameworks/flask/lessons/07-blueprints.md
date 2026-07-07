# 🔵 Blueprints & Modular Apps
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Organize large apps with Blueprints, separate concerns, URL prefixes.

## What are Blueprints?

Blueprints let you split your app into modules, each with its own routes, templates, and static files.

```python
from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
```

## Defining Blueprint Routes

```python
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return {"message": "Login page"}

@auth_bp.route("/logout")
def logout():
    return {"message": "Logged out"}
```

## Registering Blueprints

```python
from auth import auth_bp
from api import api_bp
from admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
```

## Blueprint URL Prefixes

All routes inside a blueprint are prefixed automatically:

| Blueprint | Prefix | Route | Full Path |
|-----------|--------|-------|-----------|
| auth | `/auth` | `/login` | `/auth/login` |
| api | `/api/v1` | `/items` | `/api/v1/items` |
| admin | `/admin` | `/` | `/admin/` |

## Blueprint Templates & Static

```python
admin = Blueprint("admin", __name__,
    template_folder="templates/admin",
    static_folder="static/admin")
```

## URL Generation with Blueprints

```python
url_for("auth.login")           # /auth/login
url_for("api.list_items")       # /api/v1/items
url_for("admin.admin_dashboard") # /admin/
```

<!-- 🤔 Use `Blueprint.name` as the prefix when generating URLs with `url_for()`. -->

## Why Blueprints?

- Organize large codebases
- Reusable modules across projects
- Separate testing per module
- Team-friendly parallel development

## Run the Code

```bash
python code/07-blueprints.py
```
