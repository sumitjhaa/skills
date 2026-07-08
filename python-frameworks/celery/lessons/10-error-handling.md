# 🏗️ Error Handling & Retries
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Handle failures and automatically retry tasks.

## Auto-Retry

```python
@app.task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_url(self, url):
    try:
        return requests.get(url, timeout=5).text
    except Exception as exc:
        raise self.retry(exc=exc)
```

## Manual Retry with Backoff

```python
@app.task(bind=True, max_retries=5)
def process_file(self, path):
    try:
        return parse_file(path)
    except FileNotFoundError:
        # Immediate retry not useful — just fail
        raise
    except Exception as exc:
        # Exponential backoff
        countdown = 2 ** self.request.retries
        raise self.retry(exc=exc, countdown=countdown)
```

## Task Failure Handling

```python
result = task.delay()
try:
    value = result.get(timeout=10)
except celery.exceptions.TimeoutError:
    print("Task timed out")
except celery.exceptions.TaskRevokedError:
    print("Task was revoked")
```

<!-- 🤔 Exponential backoff prevents thundering herd on retries. -->

## Run the Code

```bash
python code/10-error-handling.py
```
