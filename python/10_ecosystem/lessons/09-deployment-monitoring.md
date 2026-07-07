# 🚢 Deployment & Monitoring
<!-- ⏱️ 18 min read | 🔴 Mastery | 🧠 Mastery -->

**What You'll Learn:** Structured logging (JSON), health checks, Prometheus metrics, Docker multi-stage builds, Docker Compose for production stack, and basic Kubernetes deployment.

> 💡 **TL;DR — The whole point:** Writing the code is half the battle. Deployment packages it, Docker ensures consistency, Prometheus monitors it, structured logging debugs it, and health checks keep it alive.

## 🔗 Why This Matters
A social-media analytics API goes to production. It crashes at 3AM. The logs say "error" with no context. The health check returns 200 even though the database is down. This lesson prevents that nightmare.

## The Concept
- **Structured logging:** JSON logs with context (request_id, user_id, duration)
- **Health checks:** /health returns UP/DOWN with dependency status
- **Prometheus metrics:** request count, latency histogram, error rate
- **Docker multi-stage:** build deps in stage 1, minimal runtime in stage 2
- **Docker Compose:** app + DB + Redis + Prometheus
- **Kubernetes:** Deployment + Service + ConfigMap + liveness/readiness probes

## Code Example
```python
"""Social-media: FastAPI app with structured logging, metrics, health checks."""

import time
import logging
import random
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
)
logger = logging.getLogger("social_api")

app = FastAPI(title="Social Analytics API")
METRICS: dict[str, float | int] = {
    "http_requests_total": 0,
    "http_request_duration_seconds": 0.0,
    "errors_total": 0,
}


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    METRICS["http_requests_total"] += 1
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    METRICS["http_request_duration_seconds"] = duration
    logger.info("request", extra={
        "method": request.method,
        "path": request.url.path,
        "status": response.status_code,
        "duration_ms": round(duration * 1000, 2),
    })
    return response


@app.get("/health")
async def health():
    db_ok = random.choice([True, True, True, False])
    redis_ok = True
    if not db_ok:
        logger.error("health_check_failed", extra={"component": "database"})
        return JSONResponse(
            status_code=503,
            content={"status": "DOWN", "database": "unreachable", "redis": "ok"},
        )
    return {"status": "UP", "database": "ok", "redis": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/metrics")
async def metrics():
    return {
        "http_requests_total": METRICS["http_requests_total"],
        "http_request_duration_seconds": METRICS["http_request_duration_seconds"],
        "errors_total": METRICS["errors_total"],
    }


@app.get("/analyze")
async def analyze(text: str = "default"):
    METRICS["http_requests_total"] += 1
    result = {
        "text": text,
        "word_count": len(text.split()),
        "char_count": len(text),
        "sentiment": random.choice(["positive", "neutral", "negative"]),
    }
    logger.info("analyze_complete", extra={"text": text[:20], "result": result})
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```yaml
# docker-compose.yml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/social
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: social
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  redis:
    image: redis:7-alpine

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
```

## 🔍 How It Works
- **Structured JSON logs:** each log line is a JSON object parsable by log aggregators
- **Health check:** returns 200 with "UP" when all deps are healthy, 503 with "DOWN" when something fails
- **Prometheus metrics:** simple counter/gauge endpoint; production would use prometheus_client library
- **Docker Compose:** depends_on with condition: service_healthy ensures DB is ready before API starts
- **K8s probes:** livenessProbe (is app alive?), readinessProbe (is it ready to serve traffic?)

## ⚠️ Common Pitfall
Health checks that don't actually check dependencies. A /health that returns 200 even when the database is disconnected is worse than no health check. Always verify actual connectivity.

## 🧠 Memory Aid
"Structured logs = JSON with context. Health check = 'is the app actually working?' Metrics = count everything. Docker Compose = run the stack. K8s probes = keep it alive."

## 🏃 Try It
Add a /health endpoint to a FastAPI app that checks if a local SQLite file exists and readable. Return 200 if OK, 503 if not. Add structured logging that logs every request with method, path, and duration.

## 🔗 Related
- [Docker for Python](../09_production/lessons/11-docker-python.md) — Docker basics
- [FastAPI Deep](06-fastapi-deep.md) — building the API
- [Logging Deep](../09_production/lessons/06-logging-deep.md) — logging fundamentals

## ➡️ Next
Review and practice with [Exercises](../practice/exercises.md)
