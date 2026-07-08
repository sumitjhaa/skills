"""Celery basics — app, task, eager mode for testing."""
from celery import Celery


print("=== Celery Basics ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def add(x, y):
    return x + y

@app.task
def multiply(x, y):
    return x * y

result1 = add.delay(2, 3)
print(f"add(2, 3) = {result1.get()}")

result2 = multiply.delay(4, 5)
print(f"multiply(4, 5) = {result2.get()}")

result3 = add.delay(10, 20)
print(f"add(10, 20) = {result3.get()}")

print(f"\nTasks work synchronously in eager mode (no broker needed).")
print(f"Set task_always_eager = True for testing.")
