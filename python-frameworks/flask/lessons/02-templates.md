# 🎨 Jinja2 Templates
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Render HTML templates, pass variables, use filters, template inheritance.

## Template Folder

Flask looks for templates in a `templates/` folder.

```python
from flask import render_template

@app.route("/")
def home():
    return render_template("home.html", title="Home", message="Hello!")
```

## Template Variables

```html
<h1>{{ title }}</h1>
<p>{{ message }}</p>
<p>Year: {{ year }}</p>
```

<!-- 🤔 `{{ }}` outputs escaped HTML. Use `|safe` filter for raw HTML. -->

## Filters

```html
{{ name|upper }}
{{ price|round(2) }}
{{ text|truncate(50) }}
{{ created_at|datetimeformat }}
```

## Template Inheritance

**base.html:**
```html
<!DOCTYPE html>
<html><head><title>{% block title %}{% endblock %}</title></head>
<body>
    <nav>{% include 'nav.html' %}</nav>
    {% block content %}{% endblock %}
</body>
</html>
```

**child.html:**
```html
{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block content %}<h1>Hello!</h1>{% endblock %}
```

## Control Flow

```html
{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}

{% if user.is_admin %}
  <a href="/admin">Admin</a>
{% endif %}
```

## Run the Code

```bash
python code/02-templates.py
```
