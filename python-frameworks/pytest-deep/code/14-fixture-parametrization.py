"""Fixture parametrization — params, indirect, factory fixtures."""
import pytest


@pytest.fixture(params=["small", "medium", "large"])
def dataset(request):
    sizes = {"small": 10, "medium": 100, "large": 1000}
    return list(range(sizes[request.param]))


def test_dataset_size(dataset):
    assert len(dataset) in (10, 100, 1000)


class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role


@pytest.fixture
def user(request):
    return User(name="Test", role=request.param)


@pytest.mark.parametrize("user", ["admin", "user", "viewer"], indirect=True)
def test_user_role(user):
    assert user.role in ("admin", "user", "viewer")


@pytest.fixture
def make_user():
    created = []

    def _make(name, role="user"):
        u = User(name=name, role=role)
        created.append(u)
        return u

    yield _make
    created.clear()


def test_factory(make_user):
    alice = make_user("Alice", "admin")
    bob = make_user("Bob")
    assert alice.role == "admin"
    assert bob.role == "user"
    assert alice.name == "Alice"


@pytest.fixture
def config(request):
    marker = request.node.get_closest_marker("slow")
    return {"timeout": 60 if marker else 5, "retries": 3 if marker else 1}


@pytest.mark.slow
def test_slow_config(config):
    assert config["timeout"] == 60
    assert config["retries"] == 3


def test_fast_config(config):
    assert config["timeout"] == 5
    assert config["retries"] == 1
