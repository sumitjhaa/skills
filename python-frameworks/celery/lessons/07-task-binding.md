# 🏗️ Task Binding & Inheritance
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Access task context and create reusable task classes.

## Bind=True

```python
@app.task(bind=True)
def log_and_process(self, data):
    # self.request contains task context
    print(f"Task ID: {self.request.id}")
    print(f"Task args: {self.request.args}")
    print(f"Retry #{self.request.retries}")
    return process(data)
```

## Task Inheritance

```python
from celery import Task

class DatabaseTask(Task):
    """Base task with database connection management."""
    _db = None

    def before_start(self, task_id, args, kwargs):
        self._db = create_connection()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if self._db:
            self._db.close()

@app.task(base=DatabaseTask)
def query_db(query):
    # self._db is available here
    return execute_query(query)
```

<!-- 🤔 Use base tasks for cross-cutting concerns: DB connections, logging, metrics. -->

## Run the Code

```bash
python code/07-task-binding.py
```
