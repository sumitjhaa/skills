# 📘 Django Phase 05 — Lesson 01: Celery & Async Tasks

> 🎯 **Goal**: Offload long-running tasks to Celery workers — email, reports, image processing.

## 📖 Concepts

### Why Celery?
Django request-response cycle is synchronous. Slow tasks (email, report generation, image resizing) block the response. Celery runs them in background workers.

### Architecture
```
Web (Gunicorn)         Redis/RabbitMQ          Worker(s)
┌──────────┐     →     ┌──────────┐    →    ┌──────────┐
│ View:    │    task   │ Message  │   pop   │ Celery   │
│ send_email│  ──────  │ Broker   │  ─────  │ Worker   │
│ .delay() │           │          │         │ executes │
└──────────┘           └──────────┘         └──────────┘
```

### Task States

| State | Meaning |
|-------|---------|
| `PENDING` | Not started |
| `RECEIVED` | Picked up by broker |
| `STARTED` | Worker started |
| `SUCCESS` | Completed successfully |
| `FAILURE` | Raised exception |
| `RETRY` | Being retried |

### Key Patterns

| Pattern | Code | Use Case |
|---------|------|----------|
| Async call | `task.delay(arg)` | Fire-and-forget |
| Countdown | `task.apply_async(args=[x], countdown=30)` | Delayed execution |
| Retry | `@task(max_retries=3, default_retry_delay=60)` | Flaky operations |
| Periodic | Celery Beat | Cron jobs |
| Chain | `chain(task1.s() \| task2.s())` | Sequential tasks |

### ADHD-Friendly Summary
```
task.delay(args) → fire & forget
@task(max_retries=3) → auto retry on failure
result.get() → wait for result (blocking)
beat_schedule → cron-like periodic tasks
```

## 🛠️ Code

```python
# tasks.py
from celery import shared_task

@shared_task
def send_email_notification(user_email, subject, body):
    # Simulate email sending
    print(f"Sending to {user_email}: {subject}")
    return {"sent": True}

@shared_task(bind=True, max_retries=3)
def generate_report(self, report_type, user_id):
    try:
        # Long-running report generation
        data = build_report(report_type, user_id)
        return data
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

# views.py
from .tasks import send_email_notification

def register(request):
    user = create_user(request.POST)
    send_email_notification.delay(user.email, "Welcome!", "Thanks for joining")
    return render(request, 'done.html')
```

## 🧪 Practice

1. Create a `send_welcome_email` task with `delay()`
2. Create a `process_image` task with `max_retries=3`
3. Set up Celery Beat to run `cleanup_sessions` every 24h
4. Chain two tasks: `resize_image` → `upload_to_s3`
5. Use `result.get(timeout=10)` to wait for a task result

## 🧠 Key Takeaways

- `delay()` is the simplest way to call a task asynchronously
- Use `bind=True` to access `self.retry()` for automatic retries
- Celery Beat handles scheduling (like cron for Django)
- Always check `result.successful()` before `result.get()`
- Run worker: `celery -A project worker -l info`
