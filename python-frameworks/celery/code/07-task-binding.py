"""Task binding and inheritance — self access, base task classes."""
from celery import Celery, Task


print("=== Task Binding & Inheritance ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task(bind=True)
def process_with_context(self, data):
    print(f"  Task ID:     {self.request.id}")
    print(f"  Task name:   {self.request.task}")
    print(f"  Args:        {self.request.args}")
    print(f"  Retries:     {self.request.retries}")
    return f"processed_{data}"

class LoggedTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print(f"  [LOG] Task {task_id} succeeded: {retval}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"  [LOG] Task {task_id} failed: {exc}")

@app.task(base=LoggedTask)
def divide(x, y):
    return x / y

r1 = process_with_context.delay("hello")
print(f"\nResult: {r1.get()}\n")

r2 = divide.delay(10, 2)
print(f"Result: {r2.get()}\n")

r3 = divide.delay(10, 0)
print(f"Result: {r3.get(propagate=False)}")
