# ⏳ Background Tasks
<!-- ⏱️ 15 min | 🟡 Intermediate -->

**What You'll Learn:** Task queues, thread pools, job tracking, progress monitoring.

## Why Background Tasks?

HTTP requests should return quickly. Offload slow work (emails, reports, image processing) to background tasks.

## Simple Threading

```python
import threading

def send_email_job(user_id, email, message):
    time.sleep(5)  # Simulate slow operation
    print(f"Email sent to {email}")

@app.route("/jobs/email", methods=["POST"])
def queue_email():
    thread = threading.Thread(
        target=send_email_job,
        args=(user_id, email, message),
        daemon=True
    )
    thread.start()
    return {"task_id": id, "status": "queued"}
```

## Task Queue with Status Tracking

```python
class TaskQueue:
    def __init__(self, max_workers=4):
        self.queue = queue.Queue()
        self.tasks = {}
        self._start_workers(max_workers)

    def add_task(self, name, fn, *args):
        task = Task(id=self.next_id, name=name, fn=fn, args=args)
        self.tasks[task.id] = task
        self.queue.put(task)
        return task.id

    def get_task(self, task_id):
        task = self.tasks.get(task_id)
        return task.to_dict() if task else None

    def stats(self):
        return {"total": len(self.tasks), "pending": ..., "completed": ..., "failed": ...}
```

## Task Status Lifecycle

```
pending → running → completed
                  → failed
```

## Monitoring Tasks

```python
@app.route("/jobs/<int:task_id>")
def get_job(task_id):
    task = task_queue.get_task(task_id)
    if not task:
        return {"error": "Task not found"}
    return {"task": task}

@app.route("/jobs/stats")
def job_stats():
    return task_queue.stats()
```

## Choosing a Task Queue

| Solution | Use Case |
|----------|----------|
| `threading.Thread` | Simple, lightweight tasks |
| `concurrent.futures` | Thread pool management |
| Redis RQ | Persistent queues, middleware |
| Celery | Distributed, complex workflows |

<!-- 🧠 For production, use Celery or RQ with Redis — they persist tasks and survive restarts. -->

## Run the Code

```bash
python code/15-background-tasks.py
```
