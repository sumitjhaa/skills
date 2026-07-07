# 🧪 Testing with pytest
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Test client, fixtures, assertions, coverage, testing patterns.

## Install

```bash
pip install pytest pytest-cov
```

## Test Client

Flask provides a test client for simulating requests:

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
```

## Writing Tests

```python
def test_list_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = response.get_json()
    assert "items" in data
    assert len(data["items"]) > 0

def test_get_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.get_json()["item"]["name"] == "Laptop"

def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
```

## Testing POST Requests

```python
def test_create_item(client):
    response = client.post("/items",
        json={"name": "Keyboard", "price": 89.99})
    assert response.status_code == 201
    data = response.get_json()
    assert data["item"]["name"] == "Keyboard"

def test_create_item_validation(client):
    response = client.post("/items", json={})
    assert response.status_code == 400
    assert "error" in response.get_json()
```

## Fixtures for Test Data

```python
@pytest.fixture
def setup_db(client):
    # Clear and seed test data
    app.items.clear()
    app.items[1] = {"id": 1, "name": "Laptop", "price": 999.99}
    app.items[2] = {"id": 2, "name": "Mouse", "price": 29.99}
    yield

def test_search(setup_db, client):
    response = client.get("/search?q=lap")
    data = response.get_json()
    assert data["count"] == 1
    assert data["results"][0]["name"] == "Laptop"
```

## Running Tests

```bash
pytest                          # All tests
pytest -v                       # Verbose
pytest tests/                   # Specific directory
pytest -k "item"                # Filter by name
pytest --cov=app tests/         # Coverage report
```

## Test Structure

```
tests/
├── conftest.py      # Shared fixtures
├── test_routes.py   # Route tests
├── test_models.py   # Model tests
└── test_api.py      # API tests
```

<!-- 🤔 Name test files with `test_` prefix and test functions with `test_` prefix. -->

## Run the Code

```bash
python code/16-testing-pytest.py
```
