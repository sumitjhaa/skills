"""Task routing — sending tasks to different queues."""
from celery import Celery


print("=== Task Routing ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

app.conf.task_queues = {
    'default': {'exchange': 'default', 'routing_key': 'default'},
    'high': {'exchange': 'high', 'routing_key': 'high'},
    'slow': {'exchange': 'slow', 'routing_key': 'slow'},
}

app.conf.task_routes = {
    'tasks.send_email': {'queue': 'high'},
    'tasks.process_report': {'queue': 'slow'},
}

@app.task(queue='high')
def send_email(recipient):
    return f"Email sent to {recipient}"

@app.task(queue='slow')
def process_report(report_id):
    return f"Report {report_id} processed"

@app.task(queue='default')
def default_task(n):
    return n * 2

r1 = send_email.delay("user@example.com")
print(f"send_email (high queue): {r1.get()}")

r2 = process_report.delay(42)
print(f"process_report (slow queue): {r2.get()}")

r3 = default_task.delay(5)
print(f"default_task (default queue): {r3.get()}")

print(f"\nQueue design:")
print(f"  high:   fast tasks (emails, notifications)")
print(f"  slow:   batch processing (reports, exports)")
print(f"  default: everything else")
