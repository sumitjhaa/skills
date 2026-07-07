# 📘 Django Phase 06 — Lesson 03: Deployment Strategies

> 🎯 **Goal**: Deploy Django to production — VPS, PaaS, platform-specific configurations.

## 📖 Concepts

### Deployment Options

| Platform | Type | Effort | Cost | Best For |
|----------|------|--------|------|----------|
| **VPS** (DigitalOcean, Linode) | IaaS | High | $5-20/mo | Full control |
| **Platform** (Railway, Render) | PaaS | Low | $0-15/mo | Quick deploy |
| **Heroku** | PaaS | Low | $7-25/mo | Simple apps |
| **AWS / GCP / Azure** | Cloud | High | Variable | Enterprise |
| **Docker Swarm / K8s** | Orchestration | Very High | Variable | Scale |

### VPS Deployment Stack
```
Internet → Nginx (port 443) → Gunicorn (port 8000) → Django
              ↓
         Static files (S3/CDN)
              ↓
         PostgreSQL, Redis, Celery
```

### Key Configurations

| Component | Setting | 
|-----------|---------|
| Gunicorn | `workers = 2 * CPU + 1` |
| Nginx | Proxy pass to gunicorn, serve static |
| PostgreSQL | Connection pooling with pgBouncer |
| Redis | Cache + Celery broker |
| Supervisor/systemd | Process management |

### Environment-Specific Settings
```python
# settings/production.py
from .base import *
import os

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

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

STATIC_ROOT = '/var/www/static'
MEDIA_ROOT = '/var/www/media'
```

### Health Check Endpoint
```python
# urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'database': check_db(),
        'redis': check_redis(),
    })
```

### ADHD-Friendly Summary
```
VPS: Nginx → Gunicorn → Django
PaaS: Push to git → auto-deploy
DEBUG=False, SECRET_KEY from env
Health check → curl /health/
Monitor → Sentry + uptime checks
```

## 🛠️ Code

```python
# deploy/checklist.py
DEPLOY_CHECKLIST = [
    "DEBUG=False",
    "SECRET_KEY from environment variable",
    "ALLOWED_HOSTS configured",
    "Database migrated",
    "Static files collected",
    "CORS configured",
    "HTTPS enabled (nginx/certbot)",
    "Health check endpoint",
    "Sentry error tracking",
    "Logging configured",
    "Database backups scheduled",
    "Monitoring alerts set up",
    "SSL certificate valid",
    "Celery worker running",
    "Redis connected",
]
```

## 🧪 Practice

1. Set up a VPS with Nginx + Gunicorn + Django
2. Configure PostgreSQL and run migrations
3. Set up SSL with certbot (Let's Encrypt)
4. Create a health check endpoint
5. Deploy to Railway or Render from a GitHub repo

## 🧠 Key Takeaways

- Nginx serves static/media and proxies to Gunicorn
- Gunicorn workers = `2 * CPU cores + 1`
- Always set `DEBUG=False` and use env vars for secrets
- Health checks are essential for monitoring
- Automate deployment with CI/CD — never deploy manually
