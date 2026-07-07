# 📨 Request Handling
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Access query params, form data, headers; handle different HTTP methods.

## The Request Object

Flask's `request` object gives access to all incoming data.

```python
from flask import request

@app.route("/search")
def search():
    q = request.args.get("q", "")
    limit = request.args.get("limit", 10, type=int)
    return {"query": q, "limit": limit}
```

## Query Parameters

`request.args` — parsed URL query string.

```
/search?q=flask&limit=20&page=1
```

```python
q = request.args.get("q")
page = request.args.get("page", 1, type=int)
```

## Form Data

`request.form` — parsed POST form data.

```python
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form.get("email")
```

## Headers

`request.headers` — HTTP headers as a dict-like object.

```python
user_agent = request.headers.get("User-Agent")
content_type = request.headers.get("Content-Type")
```

## Method Dispatch

```python
@app.route("/items", methods=["GET", "POST"])
def items():
    if request.method == "POST":
        return create_item()
    return list_items()
```

<!-- 🤔 `request.method` is always available. Use it for simple method-based branching. -->

## JSON Data

```python
data = request.get_json()
name = data.get("name")
```

<!-- 🧠 For JSON APIs, use `request.get_json()` which parses the body automatically. -->

## Run the Code

```bash
python code/04-request-handling.py
```
