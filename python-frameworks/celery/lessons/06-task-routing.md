# 🏗️ Task Routing
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Route tasks to specific queues.

## Define Queues

```python
app.conf.task_queues = {
    'default': {'exchange': 'default', 'routing_key': 'default'},
    'high_priority': {'exchange': 'high', 'routing_key': 'high'},
    'slow': {'exchange': 'slow', 'routing_key': 'slow'},
}
```

## Route Tasks

```python
# Per task
@app.task(queue='high_priority')
def urgent_task():
    ...

# Via config
app.conf.task_routes = {
    'tasks.send_email': {'queue': 'email'},
    'tasks.process_report': {'queue': 'slow'},
}
```

## Run Workers Per Queue

```bash
celery -A tasks worker -Q high_priority          # fast queue only
celery -A tasks worker -Q default,email           # multiple queues
celery -A tasks worker -Q slow --concurrency=1    # slow queue, single worker
```

<!-- 🤔 Separate queues for different workloads: fast API responses vs heavy batch jobs. -->

## Run the Code

```bash
python code/06-task-routing.py
```
