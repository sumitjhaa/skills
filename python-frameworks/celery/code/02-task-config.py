"""Task configuration — options, serializer, rate limiting."""
from celery import Celery


print("=== Task Configuration ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
    rate_limit='10/m',
)
def process_data(self, data):
    print(f"  Processing: {data} (task_id={self.request.id})")
    return f"processed_{data}"

@app.task(rate_limit='5/s')
def fast_task(n):
    return n * 2

result = process_data.delay("test_data")
print(f"Result: {result.get()}")

for i in range(3):
    r = fast_task.delay(i)
    print(f"fast_task({i}) = {r.get()}")

print(f"\nTask config options:")
print(f"  bind=True      → self access (task context)")
print(f"  max_retries=3  → auto-retry count")
print(f"  rate_limit     → max executions per time unit")
