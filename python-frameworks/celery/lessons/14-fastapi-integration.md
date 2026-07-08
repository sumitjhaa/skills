# 🏗️ Celery with FastAPI
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Use Celery for background tasks in FastAPI.

## Setup

```python
# app/tasks.py
from celery import Celery

app = Celery('fastapi_app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0')

@app.task
def generate_report(user_id: int, report_type: str):
    # Long-running task
    data = collect_data(user_id)
    report = build_report(data, report_type)
    return report
```

## FastAPI Endpoint

```python
# app/main.py
from fastapi import FastAPI
from .tasks import generate_report

api = FastAPI()

@api.post("/reports/{user_id}")
async def start_report(user_id: int):
    task = generate_report.delay(user_id, "monthly")
    return {"task_id": task.id, "status": "processing"}

@api.get("/reports/status/{task_id}")
async def report_status(task_id: str):
    result = generate_report.AsyncResult(task_id)
    if result.ready():
        return {"status": "completed", "data": result.get()}
    return {"status": result.status}
```

<!-- 🤔 Return the task_id immediately, let the client poll for completion. -->

## Run the Code

```bash
python code/14-fastapi-integration.py
```
