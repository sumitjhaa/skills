"""Testing with pytest: test client, fixtures, assertions, coverage."""
from typing import Any, Optional
from datetime import datetime
import json
import re


# ======================== Test Client ========================

class TestClient:
    def __init__(self, app):
        self.app = app
        self._cookies: dict = {}
        self._headers: dict = {}

    def set_header(self, key: str, value: str):
        self._headers[key] = value

    def _request(self, method: str, path: str, **kw) -> "TestResponse":
        all_kw = {k: v for k, v in kw.items() if k != "headers"}
        result = self.app(method, path, **all_kw)
        return TestResponse(result)

    def get(self, path: str, **kw): return self._request("GET", path, **kw)
    def post(self, path: str, **kw): return self._request("POST", path, **kw)
    def put(self, path: str, **kw): return self._request("PUT", path, **kw)
    def delete(self, path: str, **kw): return self._request("DELETE", path, **kw)


class TestResponse:
    def __init__(self, result: dict):
        self.status_code = result.get("status", 200)
        self._data = result.get("data", {})

    def json(self) -> dict:
        return self._data

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    def __getitem__(self, k): return self._data[k]
    def __contains__(self, k): return k in self._data


# ======================== Test Framework ========================

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error: Optional[str] = None

    def __str__(self):
        icon = "✅" if self.passed else "❌"
        return f"{icon} {self.name}" + (f" — {self.error}" if self.error else "")


class TestRunner:
    def __init__(self):
        self.results: list[TestResult] = []
        self.assertions = 0

    def test(self, name: str):
        def deco(f):
            def wrapper(*a, **kw):
                r = TestResult(name)
                try:
                    f(*a, **kw)
                    r.passed = True
                except AssertionError as e:
                    r.error = str(e)
                except Exception as e:
                    r.error = f"{type(e).__name__}: {e}"
                self.results.append(r)
                return r
            return wrapper
        return deco

    def assert_eq(self, a, b, msg=""):
        self.assertions += 1
        if a != b:
            raise AssertionError(f"{msg}Expected {b!r}, got {a!r}")

    def assert_in(self, item, container, msg=""):
        self.assertions += 1
        if item not in container:
            raise AssertionError(f"{msg}{item!r} not in {container!r}")

    def assert_true(self, cond, msg=""):
        self.assertions += 1
        if not cond:
            raise AssertionError(msg or "Expected True")

    def assert_status(self, resp: TestResponse, expected: int):
        self.assertions += 1
        if resp.status_code != expected:
            raise AssertionError(f"Status {resp.status_code} != {expected}")

    def assert_ok(self, resp: TestResponse):
        self.assertions += 1
        if not resp.ok:
            raise AssertionError(f"Response not OK: {resp.status_code}")

    def summary(self):
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        return f"\nResults: {passed}/{total} passed ({total - passed} failed, {self.assertions} assertions)"


# ======================== App Under Test ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.items: dict[int, dict] = {}
        self._next = 1
        self.users: dict[int, dict] = {}
        self._next_user = 1

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
                return {"status": 200, "data": result}
            params = self._match_route(r["path"], path)
            if method in r["methods"] and params is not None:
                result = r["handler"](**params, **kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()
client = TestClient(app)
runner = TestRunner()


# ======================== Endpoints ========================

@app.route("/items")
def list_items(**kw):
    return {"items": list(app.items.values())}

@app.route("/items", methods=["POST"])
def create_item(**kw):
    if not kw.get("name"):
        return {"error": "Name required"}
    item = {"id": app._next, "name": kw["name"], "price": float(kw.get("price", 0))}
    app.items[app._next] = item
    app._next += 1
    return {"item": item, "message": "Created"}

@app.route("/items/<int:item_id>")
def get_item(item_id, **kw):
    item = app.items.get(item_id)
    if not item:
        return {"error": "Not found"}
    return {"item": item}

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id, **kw):
    if item_id not in app.items:
        return {"error": "Not found"}
    del app.items[item_id]
    return {"message": "Deleted"}

@app.route("/health")
def health(**kw):
    return {"status": "healthy", "items": len(app.items)}

@app.route("/register", methods=["POST"])
def register(**kw):
    if not kw.get("username"):
        return {"error": "Username required"}
    user = {"id": app._next_user, "username": kw["username"], "email": kw.get("email", "")}
    app.users[app._next_user] = user
    app._next_user += 1
    return {"user": user}

@app.route("/search")
def search(**kw):
    q = kw.get("q", "")
    items = [v for v in app.items.values() if q.lower() in v["name"].lower()]
    return {"results": items, "count": len(items)}


# ======================== Fixtures ========================

def setup_db():
    app.items.clear()
    app._next = 1
    app.users.clear()
    app._next_user = 1
    app.items[1] = {"id": 1, "name": "Laptop", "price": 999.99}
    app.items[2] = {"id": 2, "name": "Mouse", "price": 29.99}
    app._next = 3
    app.users[1] = {"id": 1, "username": "alice", "email": "alice@test.com"}
    app._next_user = 2


# ======================== Tests ========================

@runner.test("GET /items returns list")
def test_list_items():
    setup_db()
    r = client.get("/items")
    runner.assert_ok(r)
    runner.assert_eq(len(r.json()["items"]), 2)

@runner.test("GET /items/1 returns single item")
def test_get_item():
    setup_db()
    r = client.get("/items/1")
    runner.assert_ok(r)
    runner.assert_eq(r["item"]["name"], "Laptop")
    runner.assert_eq(r["item"]["price"], 999.99)

@runner.test("GET /items/999 returns error")
def test_get_item_not_found():
    setup_db()
    r = client.get("/items/999")
    runner.assert_in("error", r)

@runner.test("POST /items creates item")
def test_create_item():
    setup_db()
    r = client.post("/items", name="Keyboard", price=89.99)
    runner.assert_ok(r)
    runner.assert_eq(r["item"]["name"], "Keyboard")
    runner.assert_eq(r["item"]["price"], 89.99)

@runner.test("POST /items without name fails")
def test_create_item_validation():
    setup_db()
    r = client.post("/items")
    runner.assert_in("error", r)

@runner.test("DELETE /items/1 removes item")
def test_delete_item():
    setup_db()
    r = client.delete("/items/1")
    runner.assert_ok(r)
    # Verify it's gone
    r2 = client.get("/items/1")
    runner.assert_in("error", r2)

@runner.test("DELETE /items/999 fails")
def test_delete_not_found():
    setup_db()
    r = client.delete("/items/999")
    runner.assert_in("error", r)

@runner.test("GET /health returns status")
def test_health():
    setup_db()
    r = client.get("/health")
    runner.assert_ok(r)
    runner.assert_eq(r["status"], "healthy")

@runner.test("POST /register creates user")
def test_register():
    setup_db()
    r = client.post("/register", username="bob", email="bob@test.com")
    runner.assert_ok(r)
    runner.assert_eq(r["user"]["username"], "bob")

@runner.test("GET /search filters by query")
def test_search():
    setup_db()
    r = client.get("/search", q="lap")
    runner.assert_eq(r["count"], 1)
    runner.assert_eq(r["results"][0]["name"], "Laptop")


# ======================== Run Tests ========================
print("=== Testing with pytest Demo ===\n")

tests = [
    test_list_items, test_get_item, test_get_item_not_found,
    test_create_item, test_create_item_validation,
    test_delete_item, test_delete_not_found,
    test_health, test_register, test_search,
]

for t in tests:
    result = t()
    print(f"  {result}")

print(runner.summary())
