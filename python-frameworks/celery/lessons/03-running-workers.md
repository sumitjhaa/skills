# 🏗️ Running Workers
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** Start and manage Celery workers.

## Start Worker

```bash
# Basic
celery -A tasks worker --loglevel=info

# With concurrency
celery -A tasks worker --concurrency=4

# Named queue
celery -A tasks worker -Q queue_name

# In background
celery -A tasks worker --detach --logfile=celery.log
```

## Stop Worker

```bash
celery -A tasks control shutdown
```

## Inspect Workers

```bash
celery -A tasks inspect active
celery -A tasks inspect registered
celery -A tasks inspect stats
```

<!-- 🤔 Use `--concurrency` to control parallelism. Default = CPU count. -->

## Run the Code

```bash
python code/03-running-workers.py
```
