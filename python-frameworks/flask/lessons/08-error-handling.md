# ⚠️ Error Handling
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Error pages, `abort()`, custom error handlers, exception handling.

## Standard HTTP Errors

Use `abort()` to return HTTP errors:

```python
from flask import abort

@app.route("/admin")
def admin():
    abort(403)

@app.route("/item/<int:id>")
def get_item(id):
    item = get_item_or_none(id)
    if item is None:
        abort(404, description="Item not found")
```

## Custom Error Handlers

```python
@app.errorhandler(404)
def not_found(error):
    return {"error": "not_found", "message": str(error)}, 404

@app.errorhandler(403)
def forbidden(error):
    return {"error": "forbidden", "message": "Access denied"}, 403

@app.errorhandler(500)
def server_error(error):
    return {"error": "internal_error", "message": "Something went wrong"}, 500
```

## Custom Error Pages (HTML)

```python
@app.errorhandler(404)
def not_found(error):
    return render_template("errors/404.html"), 404
```

## Raising HTTP Errors

```python
@app.route("/validate")
def validate():
    name = request.args.get("name")
    if not name:
        abort(400, "Name parameter is required")
    age = request.args.get("age", type=int)
    if age and age < 0:
        abort(400, "Age must be positive")
    return {"message": f"Hello {name}!"}
```

<!-- 🤔 Always return the status code as the second value when returning custom error responses. -->

## Try/Except with abort

```python
@app.route("/divide")
def divide():
    try:
        result = 1 / 0
    except ZeroDivisionError:
        abort(500, "Division by zero")
```

## Run the Code

```bash
python code/08-error-handling.py
```
