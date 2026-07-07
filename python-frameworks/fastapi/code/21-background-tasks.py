"""Background tasks: task queue, delayed execution, progress tracking."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import time
import threading


# ======================== Background Task System ========================

class BackgroundTask:
    """Represents a single background task."""
    def __init__(self, task_id: int, name: str, fn: Callable, *args, **kwargs):
        self.id = task_id
        self.name = name
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.status = "pending"  # pending | running | completed | failed
        self.result: Any = None
        self.error: str | None = None
        self.created_at = datetime.now()
        self.completed_at: datetime | None = None

    def run(self):
        self.status = "running"
        try:
            self.result = self.fn(*self.args, **self.kwargs)
            self.status = "completed"
        except Exception as e:
            self.error = str(e)
            self.status = "failed"
        self.completed_at = datetime.now()


class BackgroundTasks:
    """Simulates FastAPI's BackgroundTasks with tracking."""
    def __init__(self):
        self._tasks: list[BackgroundTask] = []
        self._next_id = 1

    def add_task(self, name: str, fn: Callable, *args, **kwargs) -> int:
        task_id = self._next_id
        self._next_id += 1
        task = BackgroundTask(task_id, name, fn, *args, **kwargs)

        # Run in a separate thread (simulating background execution)
        thread = threading.Thread(target=task.run, daemon=True)
        self._tasks.append(task)
        thread.start()
        return task_id

    def get_task(self, task_id: int) -> BackgroundTask | None:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def get_all(self) -> list[dict]:
        return [
            {"id": t.id, "name": t.name, "status": t.status, "created_at": t.created_at.isoformat()}
            for t in self._tasks
        ]

    def pending_count(self) -> int:
        return sum(1 for t in self._tasks if t.status == "pending")

    def completed_count(self) -> int:
        return sum(1 for t in self._tasks if t.status == "completed")

    def failed_count(self) -> int:
        return sum(1 for t in self._tasks if t.status == "failed")


# ======================== Background Job Functions ========================

def send_welcome_email(user_id: int, email: str):
    """Simulate sending an email."""
    time.sleep(0.05)
    return f"Welcome email sent to {email} (user {user_id})"


def generate_report(report_type: str, data_size: int):
    """Simulate report generation."""
    time.sleep(0.1)
    return f"{report_type} report generated with {data_size} records"


def process_image(image_url: str, size: tuple[int, int]):
    """Simulate image processing."""
    time.sleep(0.08)
    return f"Image {image_url} resized to {size[0]}x{size[1]}"


def cleanup_temp_files():
    """Simulate cleanup job."""
    time.sleep(0.03)
    return "Temporary files cleaned up"


def failing_job():
    """Simulate a task that fails."""
    time.sleep(0.02)
    raise ValueError("Something went wrong processing the data")


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []
        self.background_tasks = BackgroundTasks()

    def post(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "POST", "handler": func})
            return func
        return deco

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                result = route["handler"](**kwargs)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.post("/users/register")
def register_user(user_id: int, email: str):
    """Register a user and send welcome email in background."""
    # Register user (immediate)
    user = {"id": user_id, "email": email, "created_at": datetime.now().isoformat()}

    # Send welcome email in background
    task_id = app.background_tasks.add_task("send_welcome_email", send_welcome_email, user_id, email)

    return {"user": user, "background_task_id": task_id, "message": "User registered. Welcome email will be sent."}


@app.post("/reports/generate")
def generate_report_endpoint(report_type: str = "summary", data_size: int = 100):
    """Generate a report in the background."""
    task_id = app.background_tasks.add_task("generate_report", generate_report, report_type, data_size)
    return {"task_id": task_id, "status": "running", "message": f"Generating {report_type} report..."}


@app.post("/images/process")
def process_image_endpoint(image_url: str = "https://example.com/img.jpg", width: int = 800, height: int = 600):
    """Process an image in the background."""
    task_id = app.background_tasks.add_task("process_image", process_image, image_url, (width, height))
    return {"task_id": task_id, "status": "processing", "message": f"Processing {image_url}"}


@app.post("/cleanup")
def trigger_cleanup():
    """Trigger cleanup in background."""
    task_id = app.background_tasks.add_task("cleanup", cleanup_temp_files)
    return {"task_id": task_id, "status": "running", "message": "Cleanup started"}


@app.post("/tasks/failing")
def trigger_failing_task():
    """Trigger a task that will fail."""
    task_id = app.background_tasks.add_task("failing_job", failing_job)
    return {"task_id": task_id, "status": "running", "message": "Failing task started (will fail)"}


@app.get("/tasks/{task_id}")
def get_task_status(task_id: int):
    """Check the status of a background task."""
    task = app.background_tasks.get_task(task_id)
    if task is None:
        return {"error": "Task not found"}
    return {
        "id": task.id,
        "name": task.name,
        "status": task.status,
        "result": task.result,
        "error": task.error,
        "created_at": task.created_at.isoformat(),
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
    }


@app.get("/tasks")
def list_tasks():
    """List all background tasks."""
    return {"tasks": app.background_tasks.get_all(), "total": len(app.background_tasks.get_all())}


@app.get("/tasks/stats")
def task_stats():
    """Get task statistics."""
    return {
        "total": len(app.background_tasks.get_all()),
        "pending": app.background_tasks.pending_count(),
        "completed": app.background_tasks.completed_count(),
        "failed": app.background_tasks.failed_count(),
    }


# ======================== Demo ========================
print("=== Background Tasks Demo ===\n")

# Trigger various background tasks
print("1. Register user (triggers welcome email):")
r1 = app("POST", "/users/register", user_id=42, email="alice@example.com")
print(f"   {json.dumps(r1['data'], indent=2)}\n")

print("2. Generate report:")
r2 = app("POST", "/reports/generate", report_type="annual", data_size=5000)
task_id_2 = r2["data"]["task_id"]
print(f"   {json.dumps(r2['data'], indent=2)}\n")

print("3. Process image:")
r3 = app("POST", "/images/process", image_url="https://example.com/photo.jpg", width=1920, height=1080)
print(f"   {json.dumps(r3['data'], indent=2)}\n")

print("4. Trigger cleanup:")
r4 = app("POST", "/cleanup")
print(f"   {json.dumps(r4['data'], indent=2)}\n")

print("5. Trigger failing task:")
r5 = app("POST", "/tasks/failing")
print(f"   {json.dumps(r5['data'], indent=2)}\n")

# Wait a moment for background tasks to complete
time.sleep(0.3)

# Check results
print(f"6. Task {task_id_2} status after wait:")
r6 = app("GET", f"/tasks/{task_id_2}")
print(f"   {json.dumps(r6['data'], indent=2)}\n")

print("7. All tasks:")
r7 = app("GET", "/tasks")
print(f"   {json.dumps(r7['data'], indent=2)}\n")

print("8. Task stats:")
r8 = app("GET", "/tasks/stats")
print(f"   {json.dumps(r8['data'], indent=2)}\n")

# Check the failing task
print("9. Failing task status:")
r9 = app("GET", "/tasks/5")
print(f"   {json.dumps(r9['data'], indent=2)}")
