# 🧪 Testing with httpx + pytest
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** TestClient, fixtures, test organization, async testing.

## Install

```bash
pip install pytest httpx
```

## TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

<!-- 🧪 TestClient uses httpx under the hood. No need to run the server. -->

## Testing CRUD

```python
def test_create_item():
    response = client.post("/items", json={"name": "Laptop", "price": 999.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
```

## Fixtures

```python
import pytest

@pytest.fixture
def test_db():
    # Setup
    db = create_test_database()
    populate_test_data(db)
    yield db
    # Teardown
    drop_test_database(db)

def test_list_items(test_db):
    response = client.get("/items")
    assert len(response.json()["items"]) == 3
```

<!-- 🔄 Fixtures run before each test. Use them for DB setup, auth tokens, file cleanup. -->

## Auth in Tests

```python
def test_protected_endpoint():
    # First, login to get token
    login_resp = client.post("/token", data={"username": "test", "password": "test"})
    token = login_resp.json()["access_token"]

    # Use the token
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

## Test Structure

```
tests/
├── conftest.py        # Shared fixtures
├── test_main.py       # Basic endpoint tests
├── test_auth.py       # Auth-specific tests
└── test_items.py      # CRUD tests
```

## Run the Code

```bash
python code/19-testing-httpx-pytest.py
```
