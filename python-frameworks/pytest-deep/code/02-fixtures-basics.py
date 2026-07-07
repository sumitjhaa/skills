"""Fixtures basics — dependency injection, yield fixtures, autouse."""
import pytest
import os


@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30, "roles": ["admin"]}


@pytest.fixture
def db_connection():
    return {"connected": True, "url": "sqlite:///:memory:"}


@pytest.fixture
def user(db_connection):
    return {"id": 1, "name": "Bob", "email": "bob@test.com"}


@pytest.fixture
def resource():
    print("\n  [setup] resource acquired")
    yield "my-resource"
    print("\n  [teardown] resource released")


@pytest.fixture(autouse=True)
def set_test_env():
    os.environ["PYTEST_RUNNING"] = "true"


def test_fixture_injection(sample_data, db_connection):
    assert sample_data["name"] == "Alice"
    assert db_connection["connected"]


def test_fixture_chaining(user, db_connection):
    assert user["id"] == 1
    assert user["name"] == "Bob"
    assert db_connection["url"] == "sqlite:///:memory:"


def test_yield_fixture(resource):
    assert resource == "my-resource"


def test_autouse():
    assert os.environ.get("PYTEST_RUNNING") == "true"
