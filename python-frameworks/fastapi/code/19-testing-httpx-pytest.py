"""Testing FastAPI with httpx + pytest: test client, fixtures, assertions."""
from typing import Any, Optional
import json


# ======================== Simulated Test Client ========================

class TestClient:
    """Simulates FastAPI's TestClient from httpx."""
    def __init__(self, app):
        self.app = app
        self._cookies: dict = {}
        self._headers: dict = {}

    def set_headers(self, **headers):
        self._headers.update(headers)

    def _make_request(self, method: str, path: str, **kwargs) -> "TestResponse":
        all_kwargs = {**kwargs}
        if "headers" in kwargs:
            all_kwargs["headers"] = {**self._headers, **kwargs["headers"]}
        else:
            all_kwargs["headers"] = {**self._headers}

        result = self.app(method, path, **all_kwargs)
        return TestResponse(result)

    def get(self, path: str, **kwargs) -> "TestResponse":
        return self._make_request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> "TestResponse":
        return self._make_request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> "TestResponse":
        return self._make_request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> "TestResponse":
        return self._make_request("DELETE", path, **kwargs)


class TestResponse:
    """Simulates httpx.Response for testing."""
    def __init__(self, result: dict):
        self._result = result
        self.status_code = result.get("status", 200)
        self._data = result.get("data", {})

    def json(self) -> dict:
        return self._data

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data


# ======================== Test Framework ========================

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error: str | None = None

    def __str__(self):
        icon = "✅" if self.passed else "❌"
        details = f" — {self.error}" if self.error else ""
        return f"{icon} {self.name}{details}"


class TestRunner:
    """Simple test runner with setup/teardown."""
    def __init__(self):
        self.results: list[TestResult] = []
        self.current_test: str = ""

    def test(self, name: str):
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = TestResult(name)
                try:
                    func(*args, **kwargs)
                    result.passed = True
                except AssertionError as e:
                    result.error = str(e)
                except Exception as e:
                    result.error = f"{type(e).__name__}: {e}"
                self.results.append(result)
                return result
            return wrapper
        return decorator

    def assert_eq(self, actual, expected, msg=""):
        if actual != expected:
            raise AssertionError(f"{msg}Expected {expected!r}, got {actual!r}")

    def assert_in(self, item, container, msg=""):
        if item not in container:
            raise AssertionError(f"{msg}{item!r} not in {container!r}")

    def assert_true(self, condition, msg=""):
        if not condition:
            raise AssertionError(msg or "Expected True")

    def assert_status(self, response: TestResponse, expected: int):
        self.assert_eq(response.status_code, expected, f"Status mismatch: ")

    def summary(self) -> str:
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        return f"\nResults: {passed}/{total} passed ({total - passed} failed)"


# ======================== App Under Test ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.items: dict[int, dict] = {}
        self._next_id = 1

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def delete(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "DELETE", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()
client = TestClient(app)
runner = TestRunner()


# ======================== Endpoints ========================

@app.get("/items")
def list_items():
    return {"items": list(app.items.values())}

@app.post("/items")
def create_item(name: str, price: float = 0.0):
    item = {"id": app._next_id, "name": name, "price": price}
    app.items[app._next_id] = item
    app._next_id += 1
    return item

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = app.items.get(item_id)
    if item is None:
        return {"error": "not_found"}
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in app.items:
        return {"error": "not_found"}
    del app.items[item_id]
    return {"deleted": True}


# ======================== Fixtures ========================

def setup_test_db():
    """Fixture: Set up fresh state before each test."""
    app.items.clear()
    app._next_id = 1
    app.items[1] = {"id": 1, "name": "Test Item", "price": 10.99}
    app.items[2] = {"id": 2, "name": "Another Item", "price": 25.50}
    app._next_id = 3


# ======================== Tests ========================

@runner.test("GET /items returns all items")
def test_list_items():
    setup_test_db()
    response = client.get("/items")
    runner.assert_status(response, 200)
    data = response.json()
    runner.assert_eq(len(data["items"]), 2)

@runner.test("GET /items/1 returns single item")
def test_get_item():
    setup_test_db()
    response = client.get("/items/1")
    runner.assert_status(response, 200)
    runner.assert_eq(response["name"], "Test Item")
    runner.assert_eq(response["price"], 10.99)

@runner.test("GET /items/999 returns error for nonexistent")
def test_get_item_not_found():
    setup_test_db()
    response = client.get("/items/999")
    runner.assert_in("error", response)

@runner.test("POST /items creates new item")
def test_create_item():
    setup_test_db()
    response = client.post("/items", name="New Item", price=15.99)
    runner.assert_status(response, 200)
    runner.assert_eq(response["name"], "New Item")
    runner.assert_eq(response["price"], 15.99)

@runner.test("POST /items auto-increments id")
def test_create_item_id():
    setup_test_db()
    r1 = client.post("/items", name="Item A")
    r2 = client.post("/items", name="Item B")
    runner.assert_eq(r1["id"], 3)
    runner.assert_eq(r2["id"], 4)

@runner.test("DELETE /items removes item")
def test_delete_item():
    setup_test_db()
    response = client.delete("/items/1")
    runner.assert_status(response, 200)
    runner.assert_true(response["deleted"])
    # Verify it's gone
    get_resp = client.get("/items/1")
    runner.assert_in("error", get_resp)

@runner.test("DELETE /items/999 returns error")
def test_delete_not_found():
    setup_test_db()
    response = client.delete("/items/999")
    runner.assert_in("error", response)

@runner.test("Multiple items after creation")
def test_multiple_items():
    setup_test_db()
    client.post("/items", name="Item A")
    client.post("/items", name="Item B")
    client.post("/items", name="Item C")
    response = client.get("/items")
    runner.assert_eq(len(response["items"]), 5)

@runner.test("Item prices are stored correctly")
def test_item_price():
    setup_test_db()
    response = client.get("/items/2")
    runner.assert_eq(response["price"], 25.50)

@runner.test("Empty list when no items")
def test_empty_list():
    app.items.clear()
    response = client.get("/items")
    runner.assert_eq(len(response["items"]), 0)


# ======================== Run Tests ========================
print("=== Testing with httpx + pytest (Simulated) ===\n")

print("Running tests...\n")

# Run all test functions (in a real pytest, these are collected automatically)
test_functions = [
    test_list_items,
    test_get_item,
    test_get_item_not_found,
    test_create_item,
    test_create_item_id,
    test_delete_item,
    test_delete_not_found,
    test_multiple_items,
    test_item_price,
    test_empty_list,
]

for test_fn in test_functions:
    result = test_fn()
    print(f"  {result}")

print(runner.summary())

# Fixture pattern summary
print("\n\nTest Patterns Used:")
print("  ✅ TestClient — simulates httpx.AsyncClient")
print("  ✅ TestResponse — status_code, .json(), .ok")
print("  ✅ Fixtures — setup_test_db() for fresh state")
print("  ✅ Assertions — assert_eq, assert_in, assert_true, assert_status")
print("  ✅ Setup/Teardown — per-test database reset")
