# 📊 Parametrize
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Run the same test with multiple inputs using `@pytest.mark.parametrize`.

## Basic Parametrization

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, -5, 5),
])
def test_add(a, b, expected):
    assert a + b == expected
```

## Single Parameter

```python
@pytest.mark.parametrize("name", ["Alice", "Bob", "Charlie"])
def test_greeting(name):
    assert len(name) > 0
```

## Stacking Parametrize

```python
@pytest.mark.parametrize("username", ["alice", "bob"])
@pytest.mark.parametrize("role", ["admin", "user"])
def test_access(username, role):
    pass  # Runs 4 times: 2 × 2
```

## Test ID Customization

```python
@pytest.mark.parametrize("n, expected", [
    pytest.param(2, 4, id="two"),
    pytest.param(3, 9, id="three"),
])
def test_square(n, expected):
    assert n * n == expected
```

Use `-k` to run specific parametrized cases:

```bash
pytest -k "two"          # Runs only test_square[two]
pytest -k "alice-admin"  # Runs specific combo
```

<!-- 🤔 Each parametrized case generates a separate test — `-v` shows all. -->

## Run the Code

```bash
pytest code/04-parametrize.py -v
```
