"""Running workers — worker commands and concurrency (simulated)."""
from celery import Celery


print("=== Running Workers ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def cpu_intensive(n):
    total = sum(i * i for i in range(n))
    return total

print("Simulating multiple workers with eager mode:\n")

concurrencies = [1, 2, 4]
for c in concurrencies:
    app.conf.worker_concurrency = c
    result = cpu_intensive.delay(10_000)
    print(f"  concurrency={c}: result={result.get()}")

print(f"\nWorker commands (for real deployment):")
print(f"  celery -A tasks worker --loglevel=info")
print(f"  celery -A tasks worker --concurrency=4")
print(f"  celery -A tasks worker -Q queue_name")
print(f"  celery -A tasks worker --detach --logfile=celery.log")
