"""FastAPI integration — async task submission and polling."""
from celery import Celery
import time


print("=== FastAPI Integration ===\n")

app = Celery('fastapi_app', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def generate_report(user_id, report_type="monthly"):
    print(f"  [REPORT] Generating {report_type} report for user {user_id}...")
    time.sleep(0.1)
    data = {"user_id": user_id, "total_orders": 42, "total_spent": 3500.0}
    return data

@app.task
def send_notification(user_id, message):
    print(f"  [NOTIFY] User {user_id}: {message}")
    return {"sent": True, "user_id": user_id}

task = generate_report.delay(123, "annual")
task_id = task.id
print(f"Task submitted: {task_id}")
print(f"Status: {task.status}")
print(f"Result: {task.get()}")

task2 = send_notification.delay(456, "Your report is ready!")
print(f"\nNotification task: {task2.id}")
print(f"Status: {task2.status}")
print(f"Result: {task2.get()}")

print(f"\nFastAPI pattern:")
print("  @api.post('/reports/{user_id}')")
print("    task = generate_report.delay(user_id)")
print("    return {'task_id': task.id}")
print("  @api.get('/reports/status/{task_id}')")
print("    result = AsyncResult(task_id)")
print("    return {'status': result.status, 'result': result.get()}")
