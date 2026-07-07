# 📝 Django Templates
<!-- ⏱️ 12 min | 🟡 Applied -->

**What You'll Learn:** Create HTML templates with Django's template language — variables, filters, tags, and inheritance.

## Template Language

```html
<!-- blog/templates/blog/post_list.html -->
{% extends "base.html" %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
<h1>Blog Posts</h1>

{% for post in posts %}
  <article>
    <h2><a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a></h2>
    <p class="meta">
      {{ post.created_at|date:"F j, Y" }}
      | Category: {{ post.category.name }}
    </p>
    <p>{{ post.content|truncatewords:50 }}</p>
  </article>
{% empty %}
  <p>No posts yet.</p>
{% endfor %}
{% endblock %}
```

## Template Inheritance

```html
<!-- blog/templates/base.html -->
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}My Blog{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
  <header>
    <nav>
      <a href="{% url 'home' %}">Home</a>
      <a href="{% url 'post_list' %}">Blog</a>
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>&copy; {% now "Y" %} My Blog</footer>
</body>
</html>
```

## Common Filters

| Filter | Example | Output |
|--------|---------|--------|
| `date` | `{{ post.created_at|date:"F j, Y" }}` | January 15, 2024 |
| `truncatewords` | `{{ text|truncatewords:20 }}` | First 20 words... |
| `default` | `{{ bio|default:"No bio" }}` | "No bio" if bio is empty |
| `lower` | `{{ name|lower }}` | "john" |
| `linebreaks` | `{{ text|linebreaks }}` | Converts newlines to `<p>` |
| `safe` | `{{ html_content|safe }}` | Renders HTML without escaping |

## Code Example

```python
"""Template rendering — pure Python simulation."""
from dataclasses import dataclass
from datetime import datetime
import re

def render_template(template: str, context: dict) -> str:
    """Simple template engine (conceptual)."""
    result = template

    # Variable replacement
    for key, value in context.items():
        result = result.replace(f'{{{{ {key} }}}}', str(value))

    # For loop simulation
    def replace_for(match):
        var_name = match.group(1)
        items = context.get(var_name, [])
        body = match.group(2)
        return '\n'.join(
            render_template(body, {**context, 'item': item}) for item in items
        )
    result = re.sub(r'\{% for (\w+) in (\w+) %\}(.*?)\{% endfor %}', replace_for, result, flags=re.DOTALL)

    # Filters
    result = re.sub(r'{{ (\w+)\|upper }}', lambda m: context.get(m.group(1), '').upper(), result)

    return result


# Template string
template = """
<h1>{{ title }}</h1>
{% for post in posts %}
  <div class="post">
    <h2>{{ item|upper }}</h2>
  </div>
{% endfor %}
"""

context = {
    'title': 'My Blog',
    'posts': ['Hello Django', 'Django Models', 'Django Views'],
}

rendered = render_template(template, context)
print(rendered)
```

## Key Points
- Templates are HTML with Django template language (DTL) tags
- `{% extends %}` + `{% block %}` = template inheritance (DRY)
- `{{ variable|filter }}` = variables with optional filters
- `{% url 'name' arg=value %}` = generate URLs from named patterns
- Use `{% static 'path' %}` for CSS/JS/images
- HTML is auto-escaped — use `|safe` only when you trust the content
