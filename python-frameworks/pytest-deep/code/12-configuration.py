"""Configuration — testing CLI flags, markers configuration example."""
import pytest


def test_verbose_output():
    assert True


@pytest.mark.slow
def test_marker_filter():
    assert True


@pytest.mark.api
def test_api_marker():
    assert True


@pytest.mark.slow
@pytest.mark.api
def test_combined_markers():
    assert True


@pytest.mark.parametrize("env, expected", [
    ("dev", True),
    ("prod", False),
])
def test_env_debug(env, expected):
    configs = {"dev": {"debug": True}, "prod": {"debug": False}}
    assert configs[env]["debug"] == expected


def test_skip_last():
    """Passing test to verify config."""
    assert True
