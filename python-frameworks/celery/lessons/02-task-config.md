# 🏗️ Task Configuration
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Configure task behavior with decorator options.

## Task Options

```python
@app.task(
    bind=True,          # task instance accessible as `self`
    max_retries=3,      # auto-retry on failure
    default_retry_delay=60,  # seconds between retries
    acks_late=True,     # re-queue if worker crashes
    rate_limit='10/m',  # max 10 tasks per minute
)
def process_data(self, data):
    return transform(data)
```

## Configuration Methods

```python
# In app config
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Task-specific
@app.task(rate_limit='5/s')
def fast_task(): ...
```

<!-- 🤔 Start with `bind=True` for access to task context (retries, request info). -->

## Run the Code

```bash
python code/02-task-config.py
```
