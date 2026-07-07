# 🔧 Fixtures Basics
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Create fixtures, dependency injection, yield fixtures for cleanup.

## Defining Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

def test_with_fixture(sample_data):
    assert sample_data["name"] == "Alice"
```

## Dependency Injection

Pytest injects fixture return values into test functions by matching parameter names.

```python
@pytest.fixture
def db_connection():
    return {"connected": True}

@pytest.fixture
def user(db_connection):
    return {"id": 1, "name": "Bob"}

def test_user(user, db_connection):
    assert user["id"] == 1
    assert db_connection["connected"]
```

## Yield Fixtures (Setup + Teardown)

```python
@pytest.fixture
def resource():
    print("\nsetup")
    yield "resource"
    print("\ncleanup")

def test_resource(resource):
    assert resource == "resource"
```

## Autouse Fixtures

```python
@pytest.fixture(autouse=True)
def setup_env():
    os.environ["TESTING"] = "true"
```

<!-- 🧠 Fixtures run when the test requests them — not before. -->

## Run the Code

```bash
pytest code/02-fixtures-basics.py -v
```
