# 🐳 Docker
<!-- ⏱️ 20 min | 🟡 Intermediate -->

**What You'll Learn:** Dockerfile, docker-compose, multi-stage builds, volumes, services.

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim AS runner
WORKDIR /app
COPY --from=builder /app/wheels /app/wheels
RUN pip install --no-cache-dir --no-index --find-links=/app/wheels -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Docker Compose

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/flaskapp
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: flaskapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Commands

```bash
# Build & start
docker compose build
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down

# Run migrations
docker compose exec web flask db upgrade
```

<!-- 🧠 Use multi-stage builds to keep images small. Never run as root inside containers. -->

## Run the Code

```bash
python code/19-docker.py
```
