"""Static files: serving CSS, JS, images; URL generation."""
from typing import Any
from datetime import datetime
import json
import os
import re


# ======================== Static File Server ========================

class StaticFolder:
    """Simulates Flask's static folder serving."""
    def __init__(self, folder: str = "static"):
        self.folder = folder
        self.files: dict[str, bytes] = {}

    def add(self, path: str, content: bytes | str):
        if isinstance(content, str):
            content = content.encode()
        self.files[path] = content

    def url(self, path: str) -> str:
        return f"/static/{path}"

    def get(self, path: str) -> bytes | None:
        return self.files.get(path)

    def list_files(self) -> list[str]:
        return list(self.files.keys())


class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.static = StaticFolder()

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

# ======================== Register Static Files ========================

app.static.add("css/style.css", """
body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
h1 { color: #333; }
nav { background: #333; color: white; padding: 1em; }
nav a { color: white; margin-right: 1em; }
.alert { padding: 1em; background: #f4f4f4; border: 1px solid #ddd; }
footer { margin-top: 2em; color: #666; font-size: 0.9em; }
""")

app.static.add("js/script.js", """
console.log('Flask app loaded');
function greet(name) { return 'Hello ' + name + '!'; }
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM ready');
});
""")

app.static.add("css/dark.css", """
body { background: #222; color: #eee; }
h1 { color: #66b3ff; }
""")


# ======================== Routes ========================

@app.route("/")
def home():
    return {
        "message": "Static Files Demo",
        "css_url": app.static.url("css/style.css"),
        "js_url": app.static.url("js/script.js"),
        "dark_css_url": app.static.url("css/dark.css"),
        "available_files": app.static.list_files(),
    }


@app.route("/style")
def show_style():
    css = app.static.get("css/style.css")
    return {
        "file": "css/style.css",
        "content": css.decode() if css else "Not found",
        "url": app.static.url("css/style.css"),
    }


@app.route("/page")
def styled_page():
    return {
        "title": "Styled Page",
        "styles": [
            app.static.url("css/style.css"),
        ],
        "body": "This page would have CSS styling in a real Flask app.",
    }


@app.route("/static/<path:filepath>")
def serve_static(filepath: str):
    content = app.static.get(filepath)
    if content is None:
        return {"error": "File not found"}
    return {
        "file": filepath,
        "size": len(content),
        "content": content.decode()[:200] + "...",
    }


# ======================== Demo ========================
print("=== Static Files Demo ===\n")

print("1. Available static files:")
for f in app.static.list_files():
    print(f"   - {f}")

print("\n2. Home endpoint with static URLs:")
r = app("GET", "/")
print(f"   CSS URL: {r['data']['css_url']}")
print(f"   JS URL:  {r['data']['js_url']}")

print("\n3. Serving CSS content:")
r = app("GET", "/static/css/style.css")
print(f"   File: {r['data']['file']}, Size: {r['data']['size']} bytes")
print(f"   Content: {r['data']['content']}")

print("\n4. Not-found file:")
r = app("GET", "/static/css/missing.css")
print(f"   {r['data']}")

print("\n5. Typical HTML page structure with static files:")
r = app("GET", "/page")
print(f"   Title: {r['data']['title']}")
for s in r['data']['styles']:
    print(f"   <link rel='stylesheet' href='{s}'>")
