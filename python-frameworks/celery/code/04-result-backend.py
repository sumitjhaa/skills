"""Result backend — storing and retrieving task results."""
from celery import Celery


print("=== Result Backend ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

@app.task
def add(x, y):
    return x + y

@app.task
def divide(x, y):
    return x / y

result = add.delay(10, 5)
print(f"Task ID: {result.id}")
print(f"Ready:   {result.ready()}")
print(f"Status:  {result.status}")
print(f"Result:  {result.get()}")
print(f"Success: {result.successful()}")

result2 = add.delay(3, 7)
print(f"\nadd(3, 7):")
print(f"  .get():          {result2.get()}")
print(f"  .get(timeout=5): {result2.get(timeout=5)}")

result3 = divide.delay(10, 0)
try:
    result3.get()
except Exception as e:
    print(f"\ndivide(10, 0):")
    print(f"  .failed():      {result3.failed()}")
    print(f"  Error: {type(e).__name__}: {e}")

result4 = divide.delay(10, 0)
print(f"  .get(propagate=False): {result4.get(propagate=False)}")
