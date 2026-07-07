# 🌐 Web Frameworks: Flask & Django
<!-- ⏱️ 16 min | 🔴 Advanced | 🧠 Production -->

**What You'll Learn:** Build web applications with Flask (lightweight, flexible) and understand Django's "batteries-included" approach — plus when to choose which.

> 💡 **TL;DR — The whole point:** Flask gives you freedom (pick your own tools). Django gives you everything (ORM, admin, auth built-in). Both are production-proven. FastAPI (covered earlier) is the modern async alternative.

## 🔗 Why This Matters
Most Python apps serve data via the web — APIs, dashboards, admin panels, e-commerce sites. Knowing at least one full-stack framework (Django) and one micro-framework (Flask) makes you deploy-ready for any scenario.

## The Concept

| Aspect | Flask | Django | FastAPI |
|--------|-------|--------|---------|
| Paradigm | Micro-framework | Full-stack | Modern async |
| ORM | None (use SQLAlchemy) | Django ORM (built-in) | None (use SQLAlchemy) |
| Admin Panel | None (use Flask-Admin) | Built-in (`/admin/`) | None |
| Auth | Flask-Login | Built-in auth system | FastAPI Users / OAuth |
| REST API | Flask-RESTx | Django REST Framework | Built-in (auto docs) |
| Async | Limited (Flask 2.x) | Limited (Django 3.x+) | Native async |
| Learning Curve | Low | Medium | Low–Medium |

## Code Example

```python
"""
Flask vs Django comparison — runnable Flask app.
Django requires a project scaffold; this shows both patterns.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory "database"
items: list[dict] = []
counter = 0


@app.route("/")
def home():
    return jsonify({"service": "Flask API", "version": "1.0", "items_count": len(items)})


@app.route("/items", methods=["GET"])
def list_items():
    return jsonify(items)


@app.route("/items", methods=["POST"])
def create_item():
    global counter
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price required"}), 400
    counter += 1
    item = {"id": counter, "name": data["name"], "price": data["price"]}
    items.append(item)
    return jsonify(item), 201


@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)


# --- Django equivalent pattern (for reference) ---
DJANGO_PATTERN = """
# Django requires a project setup, but the view pattern is:

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("items/", views.ItemList.as_view()),
    path("items/<int:pk>/", views.ItemDetail.as_view()),
]

# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

class ItemList(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class ItemDetail(APIView):
    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "not found"}, status=404)
        return Response(ItemSerializer(item).data)
"""

if __name__ == "__main__":
    print("=== Flask API ===")
    print(f"Routes: {[rule.rule for rule in app.url_map.iter_rules() if rule.endpoint != 'static']}")
    print("\nStart with: flask run  (or: python this_file.py)")
    print("\n=== Django equivalent pattern ===")
    print(DJANGO_PATTERN)
    app.run(debug=True, port=5000)
```

## 🔍 How It Works
- Flask routes are decorated functions — `@app.route("/path")` maps to a function
- `request.get_json()` parses JSON request bodies
- `jsonify(...)` creates a JSON response with proper `Content-Type`
- Django separates concerns: `urls.py` (routing) → `views.py` (logic) → `serializers.py` (data shape) → `models.py` (database)
- Django REST Framework (DRF) provides `APIView`, `ModelViewSet`, and auto-generated browsable APIs
- `Item.objects.all()` is the Django ORM — no raw SQL needed

## ⚠️ Common Pitfall
- Running Flask's dev server (`app.run()`) in production — use Gunicorn/Waitress instead
- Not setting `SECRET_KEY`, `DEBUG=False`, and `ALLOWED_HOSTS` in production
- Django's ORM makes N+1 queries easy — use `select_related()` and `prefetch_related()`
- Forgetting migrations: `python manage.py makemigrations` + `migrate`

## 🧠 Memory Aid
"Flask: decorate and go. Django: apps, models, views, serializers, urls — every piece in its place."

## 🏃 Try It
Extend the Flask app with a `PUT /items/<id>` (update) and `DELETE /items/<id>` (delete) endpoint. Then add input validation with Pydantic.

## 🔗 Related
- [FastAPI Deep](06-fastapi-deep.md) — async alternative with auto-docs
- [Web APIs](03-web-apis.md) — HTTP fundamentals
- [SQLAlchemy Deep](07-sqlalchemy-deep.md) — database layer used with Flask
- [Docker for Python](../09_production/lessons/11-docker-python.md) — containerizing your web app

## ➡️ Next
[18 — JWT & OAuth Security](18-jwt-oauth-security.md)
