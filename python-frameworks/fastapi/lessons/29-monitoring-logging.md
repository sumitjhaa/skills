# 📊 Monitoring & Logging
<!-- ⏱️ 15 min | 🟢 Core -->

**What You'll Learn:** Structured logging, metrics collection, health checks, alerting.

## Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        })

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.getLogger().addHandler(handler)
```

<!-- 📝 JSON logs are parseable by ELK, Datadog, Grafana Loki. Always use structured logging in production. -->

## Key Log Fields

| Field | Example | Why |
|-------|---------|-----|
| `timestamp` | `2024-01-01T00:00:00Z` | When? |
| `level` | `ERROR` | Severity |
| `message` | `DB timeout` | What? |
| `service` | `api-v2` | Which service? |
| `trace_id` | `abc-123` | Request tracing |
| `duration_ms` | `45.2` | How slow? |

## Metrics

```python
from prometheus_client import Counter, Histogram

REQUESTS = Counter("http_requests_total", "Total requests", ["method", "endpoint"])
DURATION = Histogram("http_request_duration_ms", "Request duration", ["method"])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    REQUESTS.labels(request.method, request.url.path).inc()
    start = time.time()
    response = await call_next(request)
    DURATION.labels(request.method).observe((time.time() - start) * 1000)
    return response
```

## Health Check

```python
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "checks": {
            "database": {"healthy": True, "latency_ms": 2.3},
            "redis": {"healthy": True, "latency_ms": 0.8},
        },
        "uptime_seconds": time.time() - start_time,
    }
```

## Run the Code

```bash
python code/29-monitoring-logging.py
```
