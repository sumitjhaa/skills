# 🏗️ Task Signals
<!-- ⏱️ 10 min | 🔶 Intermediate -->

**What You'll Learn:** Hook into task lifecycle events.

## Available Signals

```python
from celery.signals import (
    task_prerun,      # before task starts
    task_postrun,     # after task completes
    task_success,     # task succeeded
    task_failure,     # task failed
    task_retry,       # task being retried
    task_revoked,     # task revoked
)
```

## Signal Handlers

```python
@task_prerun.connect
def log_task_start(sender, task_id, task, args, kwargs, **kw):
    print(f"[{task_id}] Starting {task.name}")

@task_success.connect
def log_task_success(sender, result, **kw):
    print(f"Task completed: {result}")

@task_failure.connect
def log_task_failure(sender, task_id, exception, traceback, **kw):
    print(f"[{task_id}] Failed: {exception}")
    log_error(traceback)
```

## Use Cases

- Telemetry and monitoring
- Database cleanup
- Resource release
- Custom logging

<!-- 🤔 Signals let you observe and react to task lifecycle without modifying task code. -->

## Run the Code

```bash
python code/11-task-signals.py
```
