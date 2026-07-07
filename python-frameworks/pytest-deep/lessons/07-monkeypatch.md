# 🐒 Monkeypatch
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Replace attributes, environment variables, and import behavior during tests.

## Basic Monkeypatch

```python
import pytest

def test_set_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    assert os.environ["DATABASE_URL"] == "sqlite:///test.db"
```

## Replacing Attributes

```python
class Config:
    DEBUG = True

def test_config(monkeypatch):
    monkeypatch.setattr(Config, "DEBUG", False)
    assert Config.DEBUG is False
```

## Replacing Functions

```python
def get_user():
    return call_external_api()

def test_get_user(monkeypatch):
    def mock_get_user():
        return {"id": 1, "name": "Alice"}
    monkeypatch.setattr("module.get_user", mock_get_user)
```

## Deleting Attributes

```python
def test_delete(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
```

## Context Manager Alternative

```python
from unittest.mock import patch

with patch("module.get_user") as mock:
    mock.return_value = {"id": 1}
    result = get_user()
```

<!-- 🧠 Monkeypatch is built into pytest (no extra install). Use it for simple replacements, `unittest.mock` for complex mocking. -->

## Run the Code

```bash
pytest code/07-monkeypatch.py -v
```
