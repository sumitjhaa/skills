# ⚠️ Exceptions & Warnings
<!-- ⏱️ 10 min | 🟡 Intermediate -->

**What You'll Learn:** Testing expected exceptions and warnings with `raises` and `warns`.

## Testing Exceptions

```python
import pytest

def test_raises():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

## Inspecting the Exception

```python
def test_error_message():
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    
    assert "negative" in str(exc_info.value)
    assert exc_info.type is ValueError
```

## Match Parameter

```python
def test_error_match():
    with pytest.raises(ValueError, match="must be positive"):
        validate_age(-1)
```

## Testing Warnings

```python
import warnings

def test_warning():
    with pytest.warns(UserWarning) as record:
        warnings.warn("deprecated", UserWarning)
    
    assert "deprecated" in str(record[0].message)
```

## No Exception

```python
def test_no_exception():
    with pytest.raises(ValueError):
        pass  # ❌ Fails — no exception raised
```

<!-- 🤔 Always use `pytest.raises` instead of `try/except` in tests. -->

## Run the Code

```bash
pytest code/10-exceptions-warnings.py -v
```
