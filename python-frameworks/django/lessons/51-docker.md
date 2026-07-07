# 📘 Django Phase 06 — Lesson 01: Docker for Django

> 🎯 **Goal**: Containerize Django with Docker — multi-stage builds, docker-compose, and production-ready images.

## 📖 Concepts

### Why Docker?
Consistent environments from dev to prod. No "it works on my machine". Each service (web, DB, Redis, Celery) runs in its own container.

### Dockerfile Structure
```dockerfile
# Multi-stage build
FROM python:3.12-slim AS builder
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim AS runtime
COPY --from=builder /root/.local /root/.local
COPY . .
EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi", "--bind", "0.0.0.0:8000"]
```

### Docker Compose Services

| Service | Image | Purpose |
|---------|-------|---------|
| `web` | Build from Dockerfile | Django + Gunicorn |
| `db` | `postgres:16-alpine` | Database |
| `redis` | `redis:7-alpine` | Cache + Celery broker |
| `celery` | Same as web | Async task worker |
| `celery-beat` | Same as web | Periodic tasks |
| `nginx` | `nginx:alpine` | Reverse proxy + static |

### Best Practices
- Use `.dockerignore` to exclude `__pycache__`, `.git`, `.env`
- Don't run as root — create a `USER` directive
- Use `--no-cache-dir` with pip to reduce image size
- Pin base image versions (`python:3.12-slim`, not `python:latest`)
- Use multi-stage builds to keep final image small

### ADHD-Friendly Summary
```
Dockerfile → container image
docker-compose.yml → multi-service setup
Multi-stage → smaller images
.dockerignore → exclude junk
docker compose up -d → run everything
```

## 🛠️ Code

```dockerfile
# Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
RUN useradd -m django && chown -R django /app
USER django
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4"]
```

## 🧪 Practice

1. Write a `Dockerfile` for Django with multi-stage build
2. Create a `docker-compose.yml` with web, db (postgres), and redis
3. Add a `.dockerignore` with common patterns
4. Use `docker compose run --rm web python manage.py migrate`
5. Reduce image size by using `--no-cache-dir` and slim base image

## 🧠 Key Takeaways

- Multi-stage builds keep production images small
- Separate services into containers (web, db, redis, celery)
- Use `.dockerignore` to speed up builds
- Never run containers as root in production
- `docker compose` is the standard for multi-container Django apps
