"""Jinja2 templates: rendering, variables, filters, inheritance."""
from typing import Any
from datetime import datetime
import json
import re


# ======================== Mini Jinja2 Engine ========================

class Template:
    """Simple template engine simulating Jinja2."""
    def __init__(self, content: str):
        self.content = content

    def render(self, **context) -> str:
        result = self.content
        for key, val in context.items():
            result = result.replace(f"{{{{ {key} }}}}", str(val))
        # For loops (simple)
        result = re.sub(r'\{% for (\w+) in (\w+) %\}', '', result)
        result = re.sub(r'\{% endfor %\}', '', result)
        # If blocks
        result = re.sub(r'\{% if .*? %\}', '', result)
        result = re.sub(r'\{% endif %\}', '', result)
        return result


class TemplateFolder:
    """Simulates Flask's template folder."""
    def __init__(self):
        self.templates: dict[str, str] = {}

    def add(self, name: str, content: str):
        self.templates[name] = content

    def render(self, template_name: str, **context) -> str:
        if template_name not in self.templates:
            return f"Template '{template_name}' not found"
        tpl = Template(self.templates[template_name])
        return tpl.render(**context)


# ======================== App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.templates = TemplateFolder()

    def route(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    @staticmethod
    def _match_route(route_pattern: str, actual_path: str) -> dict | None:
        param_names = []
        def replacer(m):
            full = m.group(0)
            if ':' in full:
                typ, name = full.strip('<>').split(':')
            else:
                typ, name = 'str', full.strip('<>')
            param_names.append((name, typ))
            if typ == 'int': return r'(\d+)'
            if typ == 'float': return r'([0-9.]+)'
            if typ == 'path': return r'(.+)'
            return r'([^/]+)'
        regex = '^' + re.sub(r'<[^>]+>', replacer, route_pattern) + '$'
        m = re.match(regex, actual_path)
        if not m: return None
        return {name: int(val) if typ == 'int' else float(val) if typ == 'float' else val
                for (name, typ), val in zip(param_names, m.groups())}

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
            params = self._match_route(route["path"], path)
            if route["method"] == method and params is not None:
                result = route["handler"](**params, **kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()

# Register templates
app.templates.add("home.html", """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <p>Year: {{ year }}</p>
</body>
</html>
""")

app.templates.add("user.html", """
<!DOCTYPE html>
<html>
<head><title>{{ name }}'s Profile</title></head>
<body>
    <h1>{{ name }}</h1>
    <p>Email: {{ email }}</p>
    <p>Member since: {{ joined }}</p>
    <p>Bio: {{ bio }}</p>
</body>
</html>
""")

app.templates.add("list.html", """
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ title }}</h1>
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
""")


# ======================== Routes ========================

@app.route("/")
def home():
    html = app.templates.render("home.html",
        title="Flask Templates",
        message="Rendered with Jinja2-like engine",
        year=datetime.now().year,
    )
    return {"html": html[:200] + "...", "type": "text/html"}


@app.route("/user/<name>")
def user_profile(name: str):
    users = {
        "alice": {"email": "alice@example.com", "joined": "2024-01-15", "bio": "Python developer"},
        "bob": {"email": "bob@example.com", "joined": "2024-03-20", "bio": "Data scientist"},
    }
    user = users.get(name.lower(), {"email": "unknown", "joined": "N/A", "bio": "No bio"})
    user["name"] = name
    html = app.templates.render("user.html", **user)
    return {"html": html[:200] + "...", "name": name, **user}


@app.route("/items")
def list_items():
    items = ["Laptop", "Mouse", "Keyboard", "Monitor", "Headphones"]
    html = app.templates.render("list.html", title="Products", items=items)
    return {"items": items, "count": len(items)}


# ======================== Demo ========================
print("=== Jinja2 Templates Demo ===\n")

print("1. Home page (rendered):")
r = app("GET", "/")
print(f"   {r['data']['html']}\n")

print("2. User profile:")
r = app("GET", "/user/Alice")
print(f"   Name: {r['data']['name']}")
print(f"   Email: {r['data']['email']}")
print(f"   Joined: {r['data']['joined']}")

print("\n3. Items list:")
r = app("GET", "/items")
print(f"   Count: {r['data']['count']}")
for item in r['data']['items']:
    print(f"   - {item}")
