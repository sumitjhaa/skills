"""Static files, templates with Jinja2, file serving."""
from typing import Any, Optional
import json
import os
from datetime import datetime


# ======================== Simple Template Engine ========================

class Template:
    """Minimal template engine (simulates Jinja2)."""
    def __init__(self, template_string: str):
        self.template = template_string

    def render(self, **context) -> str:
        result = self.template
        for key, value in context.items():
            placeholder = "{{ " + key + " }}"
            result = result.replace(placeholder, str(value))
            placeholder2 = "{{" + key + "}}"
            result = result.replace(placeholder2, str(value))
        return result


class Jinja2Templates:
    """Simulates Jinja2Templates for FastAPI."""
    def __init__(self, directory: str):
        self.directory = directory
        self._templates: dict[str, Template] = {}

    def _load(self, name: str) -> Template:
        if name not in self._templates:
            path = os.path.join(self.directory, name)
            if os.path.exists(path):
                with open(path) as f:
                    self._templates[name] = Template(f.read())
            else:
                self._templates[name] = Template("")
        return self._templates.get(name, Template(""))

    def render(self, name: str, **context) -> str:
        template = self._load(name)
        return template.render(**context)


# ======================== Static File Server ========================

class StaticFiles:
    """Simulates StaticFiles for serving static assets."""
    def __init__(self, directory: str):
        self.directory = directory
        self._files: dict[str, bytes] = {}

    def add_file(self, path: str, content: bytes):
        self._files[path] = content

    def get_file(self, path: str) -> Optional[bytes]:
        full_path = path.lstrip("/")
        return self._files.get(full_path)

    def exists(self, path: str) -> bool:
        return path.lstrip("/") in self._files

    def url_for(self, path: str) -> str:
        return f"/static/{path.lstrip('/')}"


# ======================== App with Templates ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.templates = Jinja2Templates("templates")
        self.static = StaticFiles("static")

    def get(self, path: str):
        def decorator(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return decorator

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        # Check static files first
        if method == "GET" and path.startswith("/static/"):
            content = self.static.get_file(path)
            if content:
                return {"status": 200, "content": content.decode(), "content_type": self._get_content_type(path)}
            return {"status": 404, "data": {"detail": "File not found"}}
        # Check routes
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}

    def _get_content_type(self, path: str) -> str:
        ext = os.path.splitext(path)[1].lower()
        return {
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
        }.get(ext, "application/octet-stream")


app = FastAPI()

# Seed static files
app.static.add_file("static/css/style.css", b"body { font-family: sans-serif; }")
app.static.add_file("static/js/app.js", b'console.log("Hello from FastAPI");')
app.static.add_file("static/img/logo.svg", b'<svg xmlns="http://www.w3.org/2000/svg"><text>Logo</text></svg>')

# Seed templates (in memory)
app.templates._templates["index.html"] = Template("""
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
<h1>{{ heading }}</h1>
<p>Welcome to {{ app_name }}, {{ username }}!</p>
<p>Posts today: {{ post_count }}</p>
</body>
</html>
""")

app.templates._templates["post.html"] = Template("""
<!DOCTYPE html>
<html>
<head><title>{{ post_title }}</title></head>
<body>
<article>
<h1>{{ post_title }}</h1>
<p>{{ content }}</p>
<small>By {{ author }} on {{ date }}</small>
</article>
</body>
</html>
""")


# ======================== Routes ========================

@app.get("/")
def home():
    html = app.templates.render("index.html",
        title="FastAPI Blog",
        heading="Hello, FastAPI!",
        app_name="FastAPI Demo",
        username="Visitor",
        post_count=42,
    )
    return {"html": html[:200] + "..."}


@app.get("/posts/{post_id}")
def view_post(post_id: int):
    posts = {
        1: {"title": "Hello FastAPI", "content": "Getting started with FastAPI", "author": "alice"},
        2: {"title": "Templates in FastAPI", "content": "Using Jinja2 with FastAPI", "author": "alice"},
    }
    post = posts.get(post_id, {"title": "Not Found", "content": "Post does not exist", "author": "?"})
    html = app.templates.render("post.html",
        post_title=post["title"],
        content=post["content"],
        author=post["author"],
        date=datetime.now().strftime("%Y-%m-%d"),
    )
    return {"html": html[:200] + "..." if post_id <= 2 else html}


@app.get("/static/{file_path:path}")
def static_file(file_path: str):
    return {"static_url": f"/static/{file_path}"}


# ======================== Demo ========================
print("=== Static Files & Templates Demo ===\n")

# --- Static files ---
print("1. Static files:")
for f in ["static/css/style.css", "static/js/app.js", "static/img/logo.svg"]:
    exists = app.static.exists(f)
    url = app.static.url_for(f)
    print(f"   {'✅' if exists else '❌'} {f:35s} → {url}")

# --- Template rendering ---
print("\n2. Template rendering:")
result = app("GET", "/")
print(f"   GET / → {result['status']}")
print(f"   {result['data']['html']}")

print("\n3. Post template:")
result = app("GET", "/posts/1")
print(f"   GET /posts/1 → {result['status']}")
print(f"   {result['data']['html']}")

# --- Static file serving ---
print("\n4. Static file access:")
result = app("GET", "/static/css/style.css")
print(f"   GET /static/css/style.css → {result['status']}, type={result.get('content_type', '?')}")
print(f"   Content: {result.get('content', '')}")

result = app("GET", "/static/nonexistent.js")
print(f"   GET /static/nonexistent.js → {result['status']}")
