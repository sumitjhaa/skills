"""Periodic tasks — Celery beat schedule with eager mode."""
from celery import Celery
from celery.schedules import crontab


print("=== Periodic Tasks (Celery Beat) ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

app.conf.beat_schedule = {
    'every-5-seconds': {
        'task': 'tasks.heartbeat',
        'schedule': 5.0,
        'args': ('ping',),
    },
    'daily-report': {
        'task': 'tasks.generate_report',
        'schedule': crontab(hour=8, minute=0),
        'args': ('daily',),
    },
}

@app.task
def heartbeat(msg):
    return f"Heartbeat: {msg}"

@app.task
def generate_report(report_type):
    return f"{report_type} report generated"

r1 = heartbeat.delay("pong")
print(f"Heartbeat: {r1.get()}")

r2 = generate_report.delay("monthly")
print(f"Report: {r2.get()}")

print(f"\nBeat schedule config:")
print(f"  Every 5 seconds: heartbeat('ping')")
print(f"  Daily at 8:00:   generate_report('daily')")

print(f"\nCrontab examples:")
print(f"  crontab(minute='*/15')           → every 15 min")
print(f"  crontab(hour=9, minute=30)        → daily 9:30")
print(f"  crontab(day_of_week=0, hour=2)    → Sunday 2AM")
