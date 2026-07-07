# 📘 Django Phase 06 — Lesson 04: Environment Variables & Settings Management

> 🎯 **Goal**: Manage environment-specific settings with 12-factor app principles, `.env` files, and settings modules.

## 📖 Concepts

### 12-Factor App — Config
> "Store config in the environment."

Never hardcode secrets or environment-specific values in settings files.

### Settings Structure
```
myapp/
  settings/
    __init__.py     # Route to correct environment
    base.py         # Shared settings
    development.py  # Dev overrides
    staging.py      # Staging overrides
    production.py   # Production overrides
.env                # Local env vars (gitignored)
.env.example        # Template (committed)
```

### Using Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file in development

SECRET_KEY = os.environ['SECRET_KEY']  # Required, no default
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
DATABASE_URL = os.environ.get('DATABASE_URL', '')
```

### python-decouple / django-environ
```python
# With django-environ
import environ

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
DATABASES = {
    'default': env.db(),  # Parses DATABASE_URL
}
```

### .env File Template
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
DATABASE_URL=postgres://user:pass@localhost:5432/myapp
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-key
```

### Secrets Management

| Method | Good For | Not Good For |
|--------|----------|--------------|
| `.env` (gitignored) | Local dev | Production (check Vault) |
| Environment variables | Docker, CI/CD | Managing many secrets |
| HashiCorp Vault | Enterprise | Simple projects |
| AWS Secrets Manager | AWS projects | Non-AWS projects |
| GitHub Secrets | CI/CD only | Runtime |

### ADHD-Friendly Summary
```
settings/base.py → shared
settings/production.py → overrides
.env → local dev vars (gitignored)
os.environ → runtime config
12-factor: config in environment
```

## 🛠️ Code

```python
# settings/production.py
import os
from .base import *

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': '5432',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ['REDIS_URL'],
    }
}

STATIC_ROOT = '/var/www/static'
MEDIA_ROOT = '/var/www/media'
```

## 🧪 Practice

1. Create `settings/` package with `base.py`, `development.py`, `production.py`
2. Install `python-decouple` or `django-environ` and use it for config
3. Create a `.env.example` file with all required vars (no secrets)
4. Validate that production settings fail if `SECRET_KEY` is missing
5. Set `DJANGO_SETTINGS_MODULE` to different values for dev/prod

## 🧠 Key Takeaways

- Never hardcode secrets — use environment variables
- Use multiple settings files for different environments
- Commit `.env.example` — never commit `.env`
- Fail fast on missing required config in production
- 12-factor app = config in environment, not in code
