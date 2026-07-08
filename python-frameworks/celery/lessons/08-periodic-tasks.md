# 🏗️ Periodic Tasks (Celery Beat)
<!-- ⏱️ 15 min | 🔶 Intermediate -->

**What You'll Learn:** Schedule tasks to run on a timer.

## Celery Beat Scheduler

```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,                    # every 30s
        'args': (16, 16),
    },
    'daily-report': {
        'task': 'tasks.generate_report',
        'schedule': crontab(hour=8, minute=0),  # daily at 8 AM
        'args': ('daily',),
    },
    'weekly-cleanup': {
        'task': 'tasks.cleanup',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Sunday 2 AM
    },
}
```

## Start Beat

```bash
celery -A tasks beat --loglevel=info
# Run beat + worker together for dev:
celery -A tasks worker --beat --loglevel=info
```

## Crontab Examples

```python
crontab(minute='*/15')           # every 15 minutes
crontab(hour=9, minute=30)       # daily at 9:30
crontab(hour='9-17', minute=0)   # hourly 9am-5pm
crontab(day_of_week='mon-fri', hour=8)  # weekdays at 8am
```

<!-- 🤔 Use `worker --beat` for dev. Use separate beat process in production. -->

## Run the Code

```bash
python code/08-periodic-tasks.py
```
