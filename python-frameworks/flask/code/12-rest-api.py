"""REST API with Flask-RESTful: resources, marshalling, request parsing."""
from typing import Any, Optional
from datetime import datetime
import json
import re


# ======================== Resource Base ========================

class Resource:
    """Simulates Flask-RESTful's Resource."""
    def __init__(self):
        self.methods: dict[str, Any] = {}

    def get(self, **kw): return {"error": "Method not allowed"}, 405
    def post(self, **kw): return {"error": "Method not allowed"}, 405
    def put(self, **kw): return {"error": "Method not allowed"}, 405
    def delete(self, **kw): return {"error": "Method not allowed"}, 405


class Api:
    """Simulates Flask-RESTful's Api."""
    def __init__(self):
        self.resources: list[dict] = []

    def add_resource(self, resource_cls, path: str, endpoint: str = ""):
        self.resources.append({"path": path, "endpoint": endpoint or path, "resource_cls": resource_cls})

    def register(self, app):
        for res in self.resources:
            cls = res["resource_cls"]
            instance = cls()
            for method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                handler = getattr(instance, method.lower(), None)
                if handler:
                    app.routes.append({"path": res["path"], "methods": [method], "handler": handler})


# ======================== Models ========================

class ItemStore:
    def __init__(self):
        self.items: dict[int, dict] = {}
        self._next = 1

    def all(self) -> list:
        return list(self.items.values())

    def get(self, item_id: int) -> Optional[dict]:
        return self.items.get(item_id)

    def create(self, data: dict) -> dict:
        item = {"id": self._next, **data, "created_at": datetime.now().isoformat()}
        self.items[self._next] = item
        self._next += 1
        return item

    def update(self, item_id: int, data: dict) -> Optional[dict]:
        if item_id not in self.items:
            return None
        self.items[item_id].update(data)
        self.items[item_id]["updated_at"] = datetime.now().isoformat()
        return self.items[item_id]

    def delete(self, item_id: int) -> bool:
        if item_id not in self.items:
            return False
        del self.items[item_id]
        return True

store = ItemStore()

# Seed data
for name, price, cat in [("Laptop", 999.99, "electronics"), ("Mouse", 29.99, "electronics"), ("Book", 19.99, "media")]:
    store.create({"name": name, "price": price, "category": cat})


# ======================== Resources ========================

class ItemListResource(Resource):
    def get(self, **kw):
        return {"items": store.all(), "count": len(store.all())}

    def post(self, **kw):
        if not kw.get("name"):
            return {"error": "Name is required"}, 400
        item = store.create({"name": kw["name"], "price": float(kw.get("price", 0)), "category": kw.get("category", "general")})
        return {"item": item, "message": "Created"}, 201


class ItemResource(Resource):
    def get(self, item_id: int, **kw):
        item = store.get(item_id)
        if not item:
            return {"error": "Not found"}, 404
        return {"item": item}

    def put(self, item_id: int, **kw):
        data = {}
        if "name" in kw: data["name"] = kw["name"]
        if "price" in kw: data["price"] = float(kw["price"])
        if "category" in kw: data["category"] = kw["category"]
        item = store.update(item_id, data)
        if not item:
            return {"error": "Not found"}, 404
        return {"item": item, "message": "Updated"}

    def delete(self, item_id: int, **kw):
        if not store.delete(item_id):
            return {"error": "Not found"}, 404
        return {"message": "Deleted"}, 200


class StatsResource(Resource):
    def get(self, **kw):
        items = store.all()
        categories = {}
        for item in items:
            cat = item.get("category", "unknown")
            categories[cat] = categories.get(cat, 0) + 1
        avg_price = sum(i["price"] for i in items) / len(items) if items else 0
        return {
            "total_items": len(items),
            "categories": categories,
            "avg_price": round(avg_price, 2),
            "max_price": max(i["price"] for i in items) if items else 0,
            "min_price": min(i["price"] for i in items) if items else 0,
        }


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

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

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                if isinstance(result, tuple):
                    data, status = result
                    return {"status": status, "data": data}
                return {"status": 200, "data": result}
            params = self._match_route(r["path"], path)
            if method in r["methods"] and params is not None:
                result = r["handler"](**params, **kw)
                if isinstance(result, tuple):
                    data, status = result
                    return {"status": status, "data": data}
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}


app = Flask()

# Register API resources
api = Api()
api.add_resource(ItemListResource, "/api/items")
api.add_resource(ItemResource, "/api/items/<int:item_id>")
api.add_resource(StatsResource, "/api/stats")
api.register(app)


# ======================== Demo ========================
print("=== REST API Demo ===\n")

print("1. GET /api/items (list):")
r = app("GET", "/api/items")
print(f"   {len(r['data']['items'])} items\n")

print("2. GET /api/items/1 (single):")
r = app("GET", "/api/items/1")
print(f"   {json.dumps(r['data']['item'], indent=2)}\n")

print("3. POST /api/items (create):")
r = app("POST", "/api/items", name="Keyboard", price=89.99, category="electronics")
print(f"   Created: {r['data']['item']}\n")

print("4. PUT /api/items/1 (update):")
r = app("PUT", "/api/items/1", price=849.99)
print(f"   Updated: {r['data']['item']}\n")

print("5. DELETE /api/items/3 (delete):")
r = app("DELETE", "/api/items/3")
print(f"   {r['data']['message']}\n")

print("6. GET /api/stats (stats):")
r = app("GET", "/api/stats")
print(f"   {json.dumps(r['data'], indent=2)}\n")

print("7. Error cases:")
r = app("GET", "/api/items/999")
print(f"   Not found: {r['data']}")
r = app("POST", "/api/items")
print(f"   Missing name: {r['data']}")
