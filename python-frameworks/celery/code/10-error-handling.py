"""Error handling and retries — auto-retry, exponential backoff."""
from celery import Celery


print("=== Error Handling & Retries ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task(bind=True, max_retries=3)
def retryable_task(self, fail_first=False):
    if fail_first and self.request.retries < 1:
        print(f"  Attempt {self.request.retries + 1}: failing, will retry...")
        raise self.retry(exc=ValueError("Temporary error"), countdown=1)
    return f"Success on attempt {self.request.retries + 1}"

@app.task(bind=True, max_retries=2)
def always_fails(self):
    if self.request.retries < 2:
        raise self.retry(exc=RuntimeError("Will keep failing"))
    raise RuntimeError("Permanent failure after retries exhausted")

r1 = retryable_task.delay(fail_first=True)
print(f"retryable_task (retried once) result: {r1.get()}\n")

r2 = retryable_task.delay(fail_first=False)
print(f"retryable_task (no failure) result: {r2.get()}\n")

r3 = always_fails.delay()
print(f"always_fails.failed(): {r3.failed()}")
err = r3.get(propagate=False)
print(f"always_fails.get(propagate=False): {err}")
print(f"  Error type: {type(err).__name__}")

print(f"\nRetry pattern:")
print(f"  self.retry(exc=exc)               → auto-retry")
print(f"  self.retry(countdown=2**retries)  → exponential backoff")
print(f"  .get(propagate=False)             → capture error instead of raising")
