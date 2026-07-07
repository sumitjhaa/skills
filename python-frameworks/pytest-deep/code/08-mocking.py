"""Mocking with pytest-mock — mocker fixture, call assertions, side effects."""
import pytest


def test_mock_return_value(mocker):
    mock = mocker.Mock()
    mock.get_data.return_value = {"id": 1, "name": "Alice"}
    result = mock.get_data()
    assert result == {"id": 1, "name": "Alice"}
    mock.get_data.assert_called_once()


def test_mock_side_effect(mocker):
    mock = mocker.Mock()
    mock.save.side_effect = [None, ValueError("Duplicate")]
    mock.save("first")
    with pytest.raises(ValueError, match="Duplicate"):
        mock.save("second")


def test_mock_side_effect_iteration(mocker):
    mock = mocker.Mock()
    mock.fetch.side_effect = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}],
        [],
    ]
    assert mock.fetch() == [{"id": 1}, {"id": 2}]
    assert mock.fetch() == [{"id": 3}]
    assert mock.fetch() == []


def test_mock_call_args(mocker):
    mock = mocker.Mock()
    mock.process("alice@test.com", role="admin")
    mock.process.assert_called_once_with("alice@test.com", role="admin")
    args, kwargs = mock.process.call_args
    assert args[0] == "alice@test.com"
    assert kwargs["role"] == "admin"


def test_mock_call_count(mocker):
    mock = mocker.Mock()
    mock.run()
    mock.run()
    mock.run()
    assert mock.run.call_count == 3


def test_mock_reset(mocker):
    mock = mocker.Mock()
    mock.run()
    mock.reset_mock()
    mock.run.assert_not_called()


def test_patch_context(mocker):
    import json
    mock_dumps = mocker.patch("json.dumps", return_value="[]")
    result = json.dumps([1, 2, 3])
    assert result == "[]"
    mock_dumps.assert_called_once_with([1, 2, 3])
