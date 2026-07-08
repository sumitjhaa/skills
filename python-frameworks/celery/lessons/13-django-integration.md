# 🏗️ Celery with Django
<!-- ⏱️ 20 min | 🔶 Intermediate -->

**What You'll Learn:** Integrate Celery with Django.

## Setup

```python
# myapp/celery.py
from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

## Task in Django App

```python
# myapp/tasks.py
from .celery import app

@app.task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)
    send_email(user.email, 'Welcome!')
```

## Settings

```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
```

<!-- 🤔 `autodiscover_tasks()` automatically finds tasks in all installed apps. -->

## Run the Code

```bash
python code/13-django-integration.py
```
