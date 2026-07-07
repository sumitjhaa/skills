# ⏳ Background Tasks
<!-- ⏱️ 10 min | 🟢 Supplement -->

**What You'll Learn:** FastAPI BackgroundTasks, deferred execution, task tracking.

## BackgroundTasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email (slow operation)
    pass

@app.post("/users")
def create_user(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "User created. Email will be sent."}
```

<!-- ⚡ Background tasks run after the response is sent — no waiting for the client. -->

## When to Use

| Use Case | Why Background |
|----------|----------------|
| Send emails | SMTP is slow |
| Log to external service | Don't block response |
| Image processing | CPU-intensive |
| Webhook calls | Fire-and-forget |
| Generate reports | Can take seconds |

## Not a Queue

BackgroundTasks runs in the same process. For production:

| Tool | When |
|------|------|
| `BackgroundTasks` | Simple, same-process, non-critical |
| Celery / Redis Queue | Critical tasks, retry, distributed |

## Task Tracking

```python
class TaskTracker:
    def __init__(self):
        self.tasks: dict[int, dict] = {}
        self._next = 1

    def add(self, name: str, fn, *args):
        tid = self._next
        self._next += 1
        self.tasks[tid] = {"name": name, "status": "running"}
        background_tasks.add_task(self._run, tid, fn, *args)
        return tid

    def _run(self, tid, fn, *args):
        try:
            fn(*args)
            self.tasks[tid]["status"] = "completed"
        except Exception as e:
            self.tasks[tid]["status"] = "failed"
            self.tasks[tid]["error"] = str(e)
```

## Run the Code

```bash
python code/21-background-tasks.py
```
