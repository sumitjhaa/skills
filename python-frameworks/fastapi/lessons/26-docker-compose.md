# 🐳 Docker + Docker Compose
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Multi-stage Dockerfiles, Compose services, volumes, networking, health checks.

## Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /app/wheels /app/wheels
RUN pip install --no-index --find-links=/app/wheels -r requirements.txt
COPY app/ .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

<!-- 🏗️ Multi-stage keeps images small. Builder stage discarded. Final image only has runtime deps. -->

## Docker Compose

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/app
      REDIS_URL: redis://redis:6379/0
    depends_on: [db, redis]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]

  db:
    image: postgres:15-alpine
    volumes: ["postgres_data:/var/lib/postgresql/data"]
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## Key Compose Settings

| Setting | Purpose |
|---------|---------|
| `build: .` | Build from Dockerfile |
| `ports` | Host:Container mapping |
| `volumes` | Persistent data |
| `depends_on` | Startup order |
| `healthcheck` | Service readiness |
| `restart: unless-stopped` | Auto-recovery |

## Run the Code

```bash
python code/26-docker-compose.py
```
