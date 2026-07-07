"""Marks — skip, skipif, xfail, custom marks."""
import pytest
import sys


@pytest.mark.skip(reason="Not implemented yet")
def test_todo():
    assert False


@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_new_syntax():
    assert sys.version_info >= (3, 8)


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    assert 1 / 0


@pytest.mark.xfail(strict=True, reason="Should fail until fixed")
def test_strict_xfail():
    assert False


@pytest.mark.xfail(reason="Will pass if implementation changes")
def test_unexpected_pass():
    assert True


@pytest.mark.slow
def test_heavy_computation():
    result = sum(range(100000))
    assert result == 4999950000


@pytest.mark.api
def test_external_service():
    assert True  # Placeholder for real API test


def test_always_runs():
    assert 1 + 1 == 2
