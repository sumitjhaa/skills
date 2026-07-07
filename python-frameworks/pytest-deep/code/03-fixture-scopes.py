"""Fixture scopes — function, module, session."""
import pytest

call_counters = {"function": 0, "module": 0, "session": 0}


@pytest.fixture(scope="function")
def func_fixture():
    call_counters["function"] += 1
    return call_counters["function"]


@pytest.fixture(scope="module")
def module_fixture():
    call_counters["module"] += 1
    return call_counters["module"]


@pytest.fixture(scope="session")
def session_fixture():
    call_counters["session"] += 1
    return call_counters["session"]


def test_first(func_fixture, module_fixture, session_fixture):
    assert func_fixture == 1     # First call in this test
    assert module_fixture == 1   # Once per module
    assert session_fixture == 1  # Once per session


def test_second(func_fixture, module_fixture, session_fixture):
    assert func_fixture == 2     # New fixture per test
    assert module_fixture == 1   # Same as first test
    assert session_fixture == 1  # Same as first test


def test_third(func_fixture, session_fixture):
    assert func_fixture == 3
    assert session_fixture == 1


class TestScoped:
    def test_class_a(self, func_fixture):
        assert func_fixture == 4

    def test_class_b(self, func_fixture):
        assert func_fixture == 5
