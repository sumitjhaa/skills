# 🏗️ Project Setup & First Routes
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Create a Flask project, understand the structure, write routes, and run the dev server.

## Install & Setup

```bash
pip install flask
```

Minimal app (`app.py`):

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Hello Flask!"}
```

<!-- 🤔 Flask can return dicts — it auto-converts to JSON (since Flask 2.3+). -->

## Run the Server

```bash
flask run --debug
# or
python -m flask run --port 5000
```

`--debug` enables auto-reload on code changes and a debugger.

## Routes & Views

```python
@app.route("/")
def home():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return {"app": "Flask Demo", "version": "1.0.0"}
```

## Dynamic Routes

```python
@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"
```

<!-- 🧠 Route parameters are strings by default. Use converters: `<int:id>`, `<float:price>`, `<path:subpath>`. -->

## Project Structure

```
myapp/
├── app.py           # Main application
├── requirements.txt # flask
└── .gitignore
```

## Run the Code

```bash
python code/01-project-setup.py
```
