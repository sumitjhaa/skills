# 📁 Static Files
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Serve CSS, JavaScript, images; use `url_for` for static URLs.

## Static Folder

Flask serves files from a `static/` folder automatically at `/static/<path>`.

```
myapp/
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── images/logo.png
├── templates/
└── app.py
```

## Linking Static Files in Templates

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo">
```

## Why `url_for`?

- Generates correct URLs regardless of app root
- Adds cache-busting query strings in production
- Easy to change static folder location later

## Serving Static Files Programmatically

```python
from flask import send_from_directory

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)
```

<!-- 🧠 In production, serve static files via Nginx/Apache, not Flask. -->

## Run the Code

```bash
python code/03-static-files.py
```
