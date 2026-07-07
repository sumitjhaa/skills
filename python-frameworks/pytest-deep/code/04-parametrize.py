"""Parametrize — run tests with multiple inputs."""
import pytest


@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, -5, 5),
    (0, 0, 0),
    (-1, -1, -2),
])
def test_add(a, b, expected):
    assert a + b == expected


@pytest.mark.parametrize("name, length", [
    pytest.param("Alice", 5, id="alice"),
    pytest.param("Bob", 3, id="bob"),
    pytest.param("", 0, id="empty"),
])
def test_name_length(name, length):
    assert len(name) == length


def check_permission(role, action):
    permissions = {
        "admin": {"read", "write", "delete"},
        "user": {"read"},
    }
    return action in permissions[role]


@pytest.mark.parametrize("role, action, allowed", [
    ("admin", "read", True),
    ("admin", "write", True),
    ("admin", "delete", True),
    ("user", "read", True),
    ("user", "write", False),
    ("user", "delete", False),
])
def test_permissions(role, action, allowed):
    assert check_permission(role, action) == allowed


@pytest.mark.parametrize("value, expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(value, expected):
    assert value * value == expected
