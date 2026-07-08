# 🏗️ Celery Basics
<!-- ⏱️ 10 min | 🟢 Core -->

**What You'll Learn:** What Celery is and how to create your first task.

## What is Celery?

Celery is a distributed task queue for async execution. It lets you:
- Offload long-running work from your web app
- Schedule periodic tasks
- Run tasks in parallel across workers

## Components

```
App → sends task → Broker (Redis/RabbitMQ) → Worker executes task
```

## Basic Task

```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y
```

## Running

```bash
celery -A tasks worker --loglevel=info
```

## Testing (Eager Mode)

```python
app.conf.task_always_eager = True  # runs synchronously, no broker needed
result = add.delay(1, 2)
print(result.get())  # 3
```

<!-- 🤔 Always eager mode lets you test tasks without a running broker. -->

## Run the Code

```bash
python code/01-celery-basics.py
```
