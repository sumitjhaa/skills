"""Getting started with pytest — basic test file."""
def add(a, b):
    return a + b

def greet(name):
    return f"Hello, {name}!"


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_greet():
    assert greet("World") == "Hello, World!"
    assert greet("") == "Hello, !"


def test_string_upper():
    assert "hello".upper() == "HELLO"


def test_list_contains():
    assert 3 in [1, 2, 3, 4]
    assert "a" in {"a": 1}


def test_dict_key():
    data = {"name": "Alice"}
    assert "name" in data
    assert data["name"] == "Alice"
