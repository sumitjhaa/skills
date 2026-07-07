# 🎯 Docker for Python
<!-- ⏱️ 16 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Write Dockerfiles for Python apps, multi-stage builds, docker-compose for development, .dockerignore, and volume mounts for hot-reload.

> 💡 **TL;DR — The whole point:** Docker packages your app and all its dependencies into a container that runs the same everywhere — no more "it works on my machine."

## 🔗 Why This Matters
Production Python apps need consistent environments. Docker ensures your local dev, CI tests, and production servers all use the same Python version, same libraries, same OS packages.

## The Concept
- **Dockerfile:** instructions to build an image
- **Image:** a snapshot of your app + dependencies
- **Container:** a running instance of an image
- **Multi-stage build:** separate build deps from runtime deps
- **docker-compose:** define multi-container setups (app + DB + cache)

## Code Example
```dockerfile
# Dockerfile — multi-stage build for Python e-commerce API

# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app          # Hot-reload in dev
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/ecommerce
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=ecommerce
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

```
# .dockerignore
__pycache__
*.pyc
.env
.venv
.git
.gitignore
*.log
dist
build
*.egg-info
```

```python
"""app/main.py — FastAPI app that runs in Docker."""
from fastapi import FastAPI

app = FastAPI(title="E-Commerce API")


@app.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0"}
```

## 🔍 How It Works
- **Multi-stage build:** builder stage installs deps, runtime stage copies only what's needed
- **`--user`** flag in pip install avoids root-owned files
- **Non-root user:** creates `appuser` for security (never run containers as root)
- **Volume mounts:** `.:/app` syncs local changes into the container (hot-reload)
- **`.dockerignore`** prevents build context bloat (cache, venv, git)
- **Health checks:** `/health` endpoint lets orchestrators know the app is alive

## ⚠️ Common Pitfall
Installing with root inside the container and running as root. Always create a non-root user. Also, don't use `:latest` tags in production — pin exact versions (`python:3.12-slim`).

## 🧠 Memory Aid
"Dockerfile = build recipe. docker-compose = 'run my stack.' Multi-stage = build first, copy only what's needed. .dockerignore = 'don't send this to Docker.'"

## 🏃 Try It
Create a minimal Dockerfile for a FastAPI app with a `/ping` endpoint. Build it with `docker build -t my-api .` and run it with `docker run -p 8000:8000 my-api`. Verify it works.

## 🔗 Related
- [Virtual Environments](08-virtual-envs.md) — dependency isolation
- [Pre-commit & Makefile](12-precommit-makefile.md) — development workflow

## ➡️ Next
[Pre-commit & Makefile](12-precommit-makefile.md)
