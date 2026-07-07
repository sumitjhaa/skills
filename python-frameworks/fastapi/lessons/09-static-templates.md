# 🖼️ Static Files & Templates
<!-- ⏱️ 10 min | 🟢 Supplement -->

**What You'll Learn:** Serve static assets (CSS, JS, images) and render HTML templates with Jinja2.

## Mount Static Files

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

<!-- 📁 Any file in `static/` is served at `/static/filename`. -->

## Jinja2 Templates

```python
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})
```

<!-- 🧩 `request` is required in the context for Jinja2's URL helpers. -->

## Template File (index.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <link href="/static/style.css" rel="stylesheet">
</head>
<body>
    <h1>{{ title }}</h1>
</body>
</html>
```

## Directory Structure

```
app/
├── main.py
├── static/
│   ├── style.css
│   └── script.js
└── templates/
    └── index.html
```

<!-- ⚡ FastAPI doesn't have a built-in template engine — Jinja2 is FastAPI's recommended choice. -->

## Run the Code

```bash
python code/09-static-templates.py
```
