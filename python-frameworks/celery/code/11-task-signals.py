"""Task signals — hook into task lifecycle events."""
from celery import Celery
from celery.signals import (
    task_prerun, task_postrun, task_success, task_failure,
)


print("=== Task Signals ===\n")

app = Celery('demo', broker='memory://', backend='cache+memory://')
app.conf.task_always_eager = True

events = []

@task_prerun.connect
def on_prerun(sender, task_id, task, args, kwargs, **kw):
    msg = f"  [PRERUN]  {task.name}({args})"
    events.append(msg)
    print(msg)

@task_postrun.connect
def on_postrun(sender, task_id, task, args, kwargs, retval, state, **kw):
    msg = f"  [POSTRUN] {task.name} → {state}"
    events.append(msg)
    print(msg)

@task_success.connect
def on_success(sender, result, **kw):
    msg = f"  [SUCCESS] Result: {result}"
    events.append(msg)
    print(msg)

@task_failure.connect
def on_failure(sender, task_id, exception, traceback, **kw):
    msg = f"  [FAILURE] Error: {exception}"
    events.append(msg)
    print(msg)

@app.task
def good_task(x, y):
    return x + y

@app.task
def bad_task(x):
    raise ValueError(f"bad value: {x}")

print("Running good_task:")
good_task.delay(2, 3)

print("\nRunning bad_task:")
bad_task.delay(99)
