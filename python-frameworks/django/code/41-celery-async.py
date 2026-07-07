"""Celery & async tasks: task queues, periodic tasks, result tracking."""
from typing import Any, Optional, Callable
from functools import wraps
import time
import random
from collections import defaultdict


# ======================== Celery Simulation ========================

class Task:
    """Simulates a Celery task."""
    def __init__(self, fn: Callable, name: str = None, max_retries: int = 3):
        self.fn = fn
        self.name = name or fn.__name__
        self.max_retries = max_retries

    def delay(self, *args, **kwargs):
        """Async execution (simulated)."""
        return self.apply_async(args, kwargs)

    def apply_async(self, args, kwargs, countdown: int = 0):
        task_id = f"{self.name}-{random.randint(10000, 99999)}"
        result = AsyncResult(task_id)
        # Simulate immediate execution (in real Celery this is async)
        try:
            result.set_result(self.fn(*args, **kwargs))
        except Exception as e:
            result.set_error(str(e))
        return result


class AsyncResult:
    """Simulates Celery's AsyncResult."""
    def __init__(self, task_id: str):
        self.task_id = task_id
        self._result = None
        self._error = None
        self._ready = False

    def set_result(self, value):
        self._result = value
        self._ready = True

    def set_error(self, error: str):
        self._error = error
        self._ready = True

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def successful(self) -> bool:
        return self._ready and self._error is None

    def get(self, timeout: float = None) -> Any:
        if self._error:
            raise RuntimeError(self._error)
        return self._result


# ======================== Shared Task Decorator ========================
TASKS: dict[str, Task] = {}

def task(fn: Callable = None, *, name: str = None, max_retries: int = 3):
    """Simulates @celery.task decorator."""
    def decorator(f):
        t = Task(f, name=name, max_retries=max_retries)
        TASKS[t.name] = t
        return t
    if fn:
        return decorator(fn)
    return decorator


# ======================== Periodic Task (cron-like) ========================
class PeriodicTask:
    """Simulates Celery beat periodic task."""
    def __init__(self, fn, schedule: str):
        self.fn = fn
        self.schedule = schedule
        self.name = fn.__name__


beat_schedule: dict[str, dict] = {}

def periodic_task(schedule: str):
    def decorator(fn):
        task_obj = PeriodicTask(fn, schedule)
        beat_schedule[fn.__name__] = {
            "task": fn.__name__,
            "schedule": schedule,
        }
        return task_obj
    return decorator


# ======================== App Tasks ========================

@task(name="send_email_notification")
def send_email_notification(user_email: str, subject: str, body: str) -> dict:
    """Simulate sending an email (async task)."""
    time.sleep(0.05)  # Simulate network delay
    print(f"  [EMAIL] To: {user_email}, Subject: {subject}")
    return {"sent": True, "to": user_email, "subject": subject}


@task(max_retries=5)
def generate_report(report_type: str, user_id: int) -> dict:
    """Simulate a long-running report generation task."""
    time.sleep(0.1)
    data = {
        "report_type": report_type,
        "user_id": user_id,
        "generated_at": time.time(),
        "rows": random.randint(50, 500),
    }
    if random.random() < 0.1:  # 10% failure rate
        raise ValueError("Report generation failed - DB timeout")
    return data


@task
def process_image(image_path: str, thumbnail_size: tuple = (300, 300)) -> dict:
    """Simulate image processing (thumbnail generation)."""
    time.sleep(0.08)
    return {
        "original": image_path,
        "thumbnail": f"thumb_{image_path}",
        "size": thumbnail_size,
    }


@periodic_task(schedule="0 3 * * *")  # daily at 3am
def cleanup_expired_sessions():
    """Periodic cleanup of expired sessions."""
    print("  [CRON] Cleaning up expired sessions...")
    return {"cleaned": random.randint(10, 100)}


@periodic_task(schedule="*/30 * * * *")  # every 30 min
def sync_external_data():
    """Periodic sync with external API."""
    print("  [CRON] Syncing external data...")
    return {"synced": True, "records": random.randint(1, 20)}


# ======================== Demo ========================
print("=== Celery & Async Tasks Demo ===\n")

# --- Basic async task ---
print("1. Sending email (async):")
result = send_email_notification.delay(
    "alice@example.com",
    "Welcome!",
    "Thanks for joining",
)
print(f"   Task ID: {result.task_id}")
print(f"   Ready: {result.ready}")
print(f"   Result: {result.get()}")

# --- Report generation with retry ---
print("\n2. Generating report (may retry):")
for attempt in range(3):
    try:
        result = generate_report.delay("user_activity", 42)
        report = result.get()
        print(f"   Report: {report['report_type']}, rows={report['rows']}")
        break
    except RuntimeError as e:
        print(f"   Attempt {attempt + 1} failed: {e}")
        if attempt == 2:
            print("   All retries exhausted")

# --- Chain tasks (sequential) ---
print("\n3. Processing image (chain):")
img_result = process_image.delay("uploads/photo.jpg", (150, 150))
img_data = img_result.get()
print(f"   Thumbnail: {img_data['thumbnail']}")

# --- Periodic tasks ---
print(f"\n4. Periodic tasks registered:")
for name, config in beat_schedule.items():
    print(f"   - {name}: schedule='{config['schedule']}'")

# --- All registered tasks ---
print(f"\n5. All registered tasks ({len(TASKS)}):")
for name, t in TASKS.items():
    print(f"   - {name} (max_retries={t.max_retries})")
