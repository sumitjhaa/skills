# 🏗️ Integration: Full Async Pipeline
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Complete Celery project with routing, beat, monitoring, and error handling.

## Project Structure

```
project/
├── celery_app.py      # Celery app definition
├── tasks/
│   ├── email.py       # email tasks
│   ├── reports.py     # report generation
│   └── cleanup.py     # maintenance tasks
├── beat_schedule.py   # periodic task config
└── run.py             # entry point
```

## Key Patterns

```python
# 1. Separate queues by priority
@app.task(queue='high', max_retries=3)
def send_email(recipient, subject, body): ...

@app.task(queue='slow', max_retries=1)
def generate_monthly_report(user_id): ...

# 2. Beat schedule for maintenance
app.conf.beat_schedule = {
    'cleanup-every-hour': {...},
    'daily-report': {...},
}

# 3. Chain tasks
pipeline = fetch_data.s() | process_data.s() | store_results.s()

# 4. Error handling with dead-letter queue
```

<!-- 🤔 This structure scales from dev to production. Add more queues as needed. -->

## Run the Code

```bash
python code/15-integration-pipeline.py
```
