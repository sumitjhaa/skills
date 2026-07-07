"""Approx comparisons — float tolerance, collections."""
from pytest import approx
import pytest


def test_float_basic():
    assert 0.1 + 0.2 == approx(0.3)


def test_float_list():
    assert [0.1 + 0.2, 1.0 / 3.0] == approx([0.3, 1.0 / 3.0])


def test_float_dict():
    assert {"a": 0.1 + 0.2, "b": 1.0 / 3.0} == approx({"a": 0.3, "b": 1.0 / 3.0})


def test_relative_tolerance():
    value = 100.5
    assert value == approx(100, rel=0.01)   # Within 1%


def test_absolute_tolerance():
    value = 10.05
    assert value == approx(10, abs=0.1)     # Within 0.1


def test_combined_tolerance():
    value = 0.001
    assert value == approx(0, abs=0.01, rel=0.1)


def test_nested_approx():
    data = {
        "name": "test",
        "values": [0.1 + 0.2, 0.3 + 0.4],
        "stats": {"mean": 0.5},
    }
    expected = {
        "name": "test",
        "values": approx([0.3, 0.7]),
        "stats": {"mean": approx(0.5)},
    }
    assert data == expected


def test_approx_demo():
    """Demonstrate approx failures would look like."""
    with pytest.raises(AssertionError):
        assert 0.1 + 0.2 == 0.3
