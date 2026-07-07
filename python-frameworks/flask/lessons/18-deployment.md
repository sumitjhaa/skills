# 🚀 Deployment
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Gunicorn, Nginx reverse proxy, environment configs, production best practices.

## Development vs Production

| Aspect | Development | Production |
|--------|------------|------------|
| Server | `flask run` | Gunicorn/uWSGI |
| Debug | Enabled | Disabled |
| Secret Key | Hardcoded | Environment variable |
| Database | SQLite | PostgreSQL |
| Static | Flask serves | Nginx serves |

## Environment Configuration

```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = "sqlite:///dev.db"
```

## Gunicorn

```bash
pip install gunicorn
```

```bash
# Basic
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With config
gunicorn -w 4 \
    --worker-class sync \
    --timeout 30 \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    app:app
```

## Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.example.com;

    location /static/ {
        alias /var/www/app/static/;
        expires 30d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Environment Variables

```bash
export FLASK_ENV=production
export SECRET_KEY=$(openssl rand -hex 32)
export DATABASE_URL=postgresql://user:pass@localhost/db
gunicorn -w 4 app:app
```

<!-- 🤔 Never commit secrets. Use environment variables or a secrets manager. -->

## Run the Code

```bash
python code/18-deployment.py
```
