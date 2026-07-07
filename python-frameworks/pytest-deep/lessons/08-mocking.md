# 🎭 Mocking
<!-- ⏱️ 15 min | 🔴 Advanced -->

**What You'll Learn:** `mocker` fixture from pytest-mock, `Mock` / `MagicMock`, asserting calls.

## Installing pytest-mock

```bash
pip install pytest-mock
```

## Basic Mocking

```python
def test_api_call(mocker):
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"key": "value"}
    
    result = my_function()  # Uses mocked requests.get
    assert result == "value"
```

## Asserting Calls

```python
def test_send_email(mocker):
    mock = mocker.patch("smtplib.SMTP.sendmail")
    
    send_welcome_email("alice@test.com")
    
    mock.assert_called_once()
    mock.assert_called_with("from@test.com", "alice@test.com", ANY)
```

## Side Effects

```python
def test_retry(mocker):
    mock = mocker.patch("db.save")
    mock.side_effect = [Exception("Timeout"), Exception("Timeout"), None]
    
    result = save_with_retry(data)  # Retries on failure
    assert result is True
    assert mock.call_count == 3
```

## Mock Return Value Sequences

```python
mock = mocker.patch("api.get_page")
mock.side_effect = [
    [{"id": 1}, {"id": 2}],  # First call
    [{"id": 3}],              # Second call
    [],                       # Third call (empty = done)
]
```

<!-- 🧠 `mocker` auto-cleans up after the test — no need for `with patch(...)`. -->

## Run the Code

```bash
pytest code/08-mocking.py -v
```
