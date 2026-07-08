# 🏗️ Monitoring with Flower
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Monitor Celery workers with Flower.

## Start Flower

```bash
# Basic
celery -A tasks flower

# With options
celery -A tasks flower --port=5555 --broker=redis://localhost:6379/0

# Basic auth
celery -A tasks flower --basic_auth=user:pass
```

## Flower Features

- Real-time worker status
- Task history and metrics
- Queue lengths and statistics
- Revoke/terminate tasks
- Filter and search tasks
- REST API

## Flower REST API

```bash
# List workers
curl http://localhost:5555/api/workers

# List tasks
curl http://localhost:5555/api/tasks

# Revoke task
curl -X POST http://localhost:5555/api/task/revoke/TASK_ID
```

<!-- 🤔 Flower is the go-to monitoring tool for Celery. Use it in dev and prod. -->

## Run the Code

```bash
python code/12-monitoring.py
```
