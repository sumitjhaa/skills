"""Exception and warning testing — raises, warns."""
import pytest
import warnings


def validate_age(age):
    if age < 0:
        raise ValueError("Age must be positive")
    if age > 150:
        raise ValueError("Age seems unrealistic")
    return age


def parse_int(value):
    if not isinstance(value, str):
        raise TypeError("Expected string")
    if not value.strip():
        raise ValueError("Empty string")
    return int(value)


def deprecated_function():
    warnings.warn("Use new_function() instead", DeprecationWarning)
    return "old result"


def test_raises_exception():
    with pytest.raises(ValueError):
        validate_age(-1)


def test_raises_type():
    with pytest.raises(TypeError):
        parse_int(42)


def test_exception_message():
    with pytest.raises(ValueError) as exc_info:
        validate_age(-5)
    assert "positive" in str(exc_info.value)


def test_exception_match():
    with pytest.raises(ValueError, match="unrealistic"):
        validate_age(200)


def test_no_exception():
    assert validate_age(25) == 25


def test_multiple_exceptions():
    with pytest.raises((ValueError, TypeError)):
        parse_int("")  # ValueError


def test_warning():
    with pytest.warns(DeprecationWarning) as record:
        result = deprecated_function()
    assert result == "old result"
    assert len(record) == 1
    assert "new_function" in str(record[0].message)


def test_no_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = validate_age(30)
    assert len(w) == 0
