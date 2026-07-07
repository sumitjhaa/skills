"""Shared fixtures for tests in this directory."""
import pytest


@pytest.fixture
def db():
    class FakeDB:
        def __init__(self):
            self.data = {}

        def get(self, key):
            return self.data.get(key)

        def set(self, key, value):
            self.data[key] = value

        def clear(self):
            self.data.clear()

    return FakeDB()


@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Alice", "email": "alice@test.com"}
