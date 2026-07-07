# 🧪 Getting Started
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Write your first pytest test, assertion introspection, test discovery.

## Your First Test

```python
# test_demo.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

## Running Tests

```bash
pytest                          # Discover and run all tests
pytest -v                       # Verbose
pytest test_demo.py             # Run a specific file
pytest test_demo.py::test_addition  # Run a specific test
pytest -k "addition"            # Run tests matching keyword
```

## Assertion Introspection

```python
def test_fail():
    a, b = 1, 2
    assert a == b  # pytest shows: assert 1 == 2
```

## Test Discovery Rules

- Files matching `test_*.py` or `*_test.py`
- Functions matching `test_*`
- Classes matching `Test*` (no `__init__`)

<!-- 🤔 No `unittest.TestCase` needed — plain `assert` works with rich diff output. -->

## Run the Code

```bash
pytest code/01-getting-started.py -v
```
