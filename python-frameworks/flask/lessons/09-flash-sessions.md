# 💬 Flash Messages & Sessions
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Session storage, flash messages, temporary data across requests.

## Sessions

Flask sessions are client-side (cookie-based) dicts.

```python
from flask import session

app.secret_key = "your-secret-key"

@app.route("/login", methods=["POST"])
def login():
    session["user"] = request.form["username"]
    session["role"] = "admin"
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
```

## Session Operations

```python
# Set
session["key"] = value

# Get
session.get("key", default)
session["key"]  # KeyError if missing

# Check
"key" in session

# Delete
session.pop("key", None)

# Clear all
session.clear()
```

## Flash Messages

Flash messages persist for one request — perfect for status feedback.

```python
from flask import flash

@app.route("/login", methods=["POST"])
def login():
    if valid:
        flash("Welcome back!", "success")
        return redirect(url_for("dashboard"))
    flash("Invalid credentials", "error")
    return render_template("login.html")
```

## Displaying Flash Messages

```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
  {% endif %}
{% endwith %}
```

## Flash Categories

```python
flash("Info message", "info")
flash("Success!", "success")
flash("Warning!", "warning")
flash("Error!", "error")
```

<!-- 🤔 Categories let you style different message types via CSS classes. -->

## Session-Based Cart Example

```python
@app.route("/cart/add")
def add_to_cart():
    item = request.args.get("item")
    cart = session.get("cart", [])
    cart.append(item)
    session["cart"] = cart
    flash(f"Added '{item}' to cart", "success")
    return redirect(url_for("view_cart"))
```

<!-- 🧠 Session data is signed (not encrypted) — never store secrets. For sensitive data, use server-side sessions. -->

## Run the Code

```bash
python code/09-flash-sessions.py
```
