"""Monitoring — Flower and task inspection (simulated)."""
from celery import Celery


print("=== Monitoring ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def task_a(n):
    return n + 1

@app.task
def task_b(n):
    return n * 2

@app.task
def task_c(n):
    return n ** 2

results = []
results.append(task_a.delay(1))
results.append(task_b.delay(2))
results.append(task_c.delay(3))
results.append(task_a.delay(10))
results.append(task_b.delay(20))

print("Task status overview:")
print(f"{'ID':<36} | {'Name':<8} | {'Status':<10} | {'Result':<10}")
print("-" * 70)
for r in results:
    print(f"{r.id:<36} | {'...':<8} | {r.status:<10} | {str(r.get()):<10}")

print(f"\nFlower monitoring (real deployment):")
print(f"  Start:   celery -A tasks flower --port=5555")
print(f"  Workers: curl http://localhost:5555/api/workers")
print(f"  Tasks:   curl http://localhost:5555/api/tasks")
print(f"\n  Includes: real-time stats, queue lengths, task history,")
print(f"            worker status, task revocation.")
