"""Background tasks: thread pool, job queue, progress tracking."""
from typing import Any, Optional, Callable
from datetime import datetime
import json
import time
import threading
import queue
import re


# ======================== Task Queue ========================

class Task:
    def __init__(self, task_id: int, name: str, fn: Callable, *args, **kw):
        self.id = task_id
        self.name = name
        self.fn = fn
        self.args = args
        self.kwargs = kw
        self.status = "pending"
        self.result: Any = None
        self.error: Optional[str] = None
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None

    def run(self):
        self.status = "running"
        try:
            self.result = self.fn(*self.args, **self.kwargs)
            self.status = "completed"
        except Exception as e:
            self.error = str(e)
            self.status = "failed"
        self.completed_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": self.id, "name": self.name, "status": self.status,
            "result": self.result, "error": self.error,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class TaskQueue:
    def __init__(self, max_workers: int = 4):
        self._queue: queue.Queue = queue.Queue()
        self._tasks: dict[int, Task] = {}
        self._next_id = 1
        self._workers: list[threading.Thread] = []
        self._running = True

        for _ in range(max_workers):
            t = threading.Thread(target=self._worker, daemon=True)
            t.start()
            self._workers.append(t)

    def _worker(self):
        while self._running:
            try:
                task = self._queue.get(timeout=1)
                task.run()
            except queue.Empty:
                continue
            except Exception:
                pass

    def add_task(self, name: str, fn: Callable, *args, **kw) -> int:
        tid = self._next_id
        self._next_id += 1
        task = Task(tid, name, fn, *args, **kw)
        self._tasks[tid] = task
        self._queue.put(task)
        return tid

    def get_task(self, tid: int) -> Optional[dict]:
        task = self._tasks.get(tid)
        return task.to_dict() if task else None

    def list_tasks(self, status: Optional[str] = None) -> list[dict]:
        tasks = self._tasks.values()
        if status:
            tasks = [t for t in tasks if t.status == status]
        return [t.to_dict() for t in tasks]

    def stats(self) -> dict:
        all_tasks = self._tasks.values()
        return {
            "total": len(all_tasks),
            "pending": sum(1 for t in all_tasks if t.status == "pending"),
            "running": sum(1 for t in all_tasks if t.status == "running"),
            "completed": sum(1 for t in all_tasks if t.status == "completed"),
            "failed": sum(1 for t in all_tasks if t.status == "failed"),
            "queue_size": self._queue.qsize(),
            "workers": len(self._workers),
        }

    def shutdown(self):
        self._running = False


task_queue = TaskQueue(max_workers=3)


# ======================== Job Functions ========================

def send_email_job(user_id: int, email: str, message: str):
    time.sleep(0.1)
    return f"Email sent to {email}: {message[:20]}..."

def generate_report_job(report_type: str, data_points: int):
    time.sleep(0.2)
    return f"{report_type} report generated with {data_points} data points"

def process_image_job(image_url: str, size: str):
    time.sleep(0.15)
    return f"Image {image_url} processed to {size}"

def cleanup_job():
    time.sleep(0.05)
    return "Cleanup completed: 12 temp files removed"

def failing_job():
    time.sleep(0.02)
    raise ValueError("Simulated failure in background job")


# ======================== Flask App ========================

class Flask:
    def __init__(self):
        self.routes: list[dict] = []
        self.task_queue = task_queue

    def route(self, path, methods=None):
        methods = methods or ["GET"]
        def deco(f):
            self.routes.append({"path": path, "methods": methods, "handler": f}); return f
        return deco

    @staticmethod
    def _match_route(route_pattern: str, actual_path: str) -> dict | None:
        param_names = []
        def replacer(m):
            full = m.group(0)
            if ':' in full:
                typ, name = full.strip('<>').split(':')
            else:
                typ, name = 'str', full.strip('<>')
            param_names.append((name, typ))
            if typ == 'int': return r'(\d+)'
            if typ == 'float': return r'([0-9.]+)'
            if typ == 'path': return r'(.+)'
            return r'([^/]+)'
        regex = '^' + re.sub(r'<[^>]+>', replacer, route_pattern) + '$'
        m = re.match(regex, actual_path)
        if not m: return None
        return {name: int(val) if typ == 'int' else float(val) if typ == 'float' else val
                for (name, typ), val in zip(param_names, m.groups())}

    def __call__(self, method, path, **kw):
        for r in self.routes:
            if method in r["methods"] and r["path"] == path:
                result = r["handler"](**kw)
                return {"status": 200, "data": result}
            params = self._match_route(r["path"], path)
            if method in r["methods"] and params is not None:
                result = r["handler"](**params, **kw)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"error": "Not Found"}}

app = Flask()


# ======================== Routes ========================

@app.route("/jobs/email", methods=["POST"])
def queue_email(**kw):
    tid = app.task_queue.add_task("send_email", send_email_job, int(kw.get("user_id", 0)), kw.get("email", ""), kw.get("message", ""))
    return {"task_id": tid, "status": "queued", "type": "email"}

@app.route("/jobs/report", methods=["POST"])
def queue_report(**kw):
    tid = app.task_queue.add_task("generate_report", generate_report_job, kw.get("type", "summary"), int(kw.get("data_points", 100)))
    return {"task_id": tid, "status": "queued", "type": "report"}

@app.route("/jobs/image", methods=["POST"])
def queue_image(**kw):
    tid = app.task_queue.add_task("process_image", process_image_job, kw.get("url", ""), kw.get("size", "800x600"))
    return {"task_id": tid, "status": "queued", "type": "image"}

@app.route("/jobs/cleanup", methods=["POST"])
def queue_cleanup(**kw):
    tid = app.task_queue.add_task("cleanup", cleanup_job)
    return {"task_id": tid, "status": "queued", "type": "cleanup"}

@app.route("/jobs/fail", methods=["POST"])
def queue_fail(**kw):
    tid = app.task_queue.add_task("failing_job", failing_job)
    return {"task_id": tid, "status": "queued", "type": "failing", "note": "This job will fail"}

@app.route("/jobs/<int:task_id>")
def get_job(task_id: int):
    task = app.task_queue.get_task(task_id)
    if not task:
        return {"error": "Task not found"}
    return {"task": task}

@app.route("/jobs")
def list_jobs(**kw):
    status_filter = kw.get("status")
    return {"tasks": app.task_queue.list_tasks(status_filter)}

@app.route("/jobs/stats")
def job_stats():
    return app.task_queue.stats()


# ======================== Demo ========================
print("=== Background Tasks Demo ===\n")

print("1. Queue various jobs:")
for fn, kw in [
    ("email", {"user_id": 1, "email": "user@test.com", "message": "Welcome!"}),
    ("report", {"type": "annual", "data_points": 5000}),
    ("image", {"url": "https://example.com/photo.jpg", "size": "1920x1080"}),
    ("cleanup", {}),
    ("fail", {}),
]:
    r = app("POST", f"/jobs/{fn}", **kw)
    print(f"   Queued {fn}: task_id={r['data']['task_id']}")

time.sleep(0.5)

print("\n2. Task results:")
for i in range(1, 6):
    r = app("GET", f"/jobs/{i}")
    t = r["data"]["task"]
    icon = "✅" if t["status"] == "completed" else "❌" if t["status"] == "failed" else "⏳"
    print(f"   {icon} [{t['id']}] {t['name']}: {t['status']} → {t.get('result', t.get('error', ''))}")

print("\n3. Stats:")
r = app("GET", "/jobs/stats")
print(f"   {json.dumps(r['data'], indent=2)}")

print("\n4. All tasks:")
r = app("GET", "/jobs")
for t in r["data"]["tasks"]:
    print(f"   [{t['id']:2d}] {t['name']:20s} {t['status']:10s} {(t.get('result') or '')[:40]}")
