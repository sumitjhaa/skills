# 📘 Django Phase 06 — Lesson 05: Logging & Monitoring

> 🎯 **Goal**: Structured logging, log aggregation, metrics collection, and monitoring dashboards.

## 📖 Concepts

### Why Structured Logging?
Raw log lines are hard to search. JSON logs are parseable by log aggregators (ELK, Loki, Datadog).

```json
# Bad
"INFO: User alice logged in"

# Good
{"timestamp": "2024-01-15T10:30:00Z", "level": "INFO", "event": "user_login", "user": "alice", "ip": "203.0.113.5"}
```

### Log Levels

| Level | When | Example |
|-------|------|---------|
| `DEBUG` | Development only | SQL queries, variable values |
| `INFO` | Normal operations | User registered, request completed |
| `WARNING` | Something unexpected | Slow query, rate limit approaching |
| `ERROR` | Runtime error | DB connection failed, API error |
| `CRITICAL` | System down | Can't connect to database |

### Django Logging Configuration
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'myapp.logging.StructuredFormatter',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'json'},
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {'handlers': ['console'], 'level': 'INFO'},
        'django.request': {'handlers': ['console', 'file'], 'level': 'WARNING'},
        'myapp': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}
```

### Metrics to Monitor

| Metric | What It Tells You | Alert Threshold |
|--------|-------------------|-----------------|
| Request rate | Traffic volume | — |
| Response time (avg/p95/p99) | Performance | avg > 200ms, p95 > 500ms |
| Error rate | Stability | > 1% errors |
| DB query time | Query performance | > 100ms per query |
| DB connections | Connection pool usage | > 80% of max |
| Cache hit rate | Cache effectiveness | < 80% |
| Celery queue depth | Task backlog | > 1000 |
| Disk usage | Storage | > 85% |

### Monitoring Stack
- **Sentry** — Error tracking + APM
- **Prometheus + Grafana** — Metrics + dashboards
- **Loki + Grafana** — Log aggregation
- **Datadog / New Relic** — All-in-one
- **Uptime Robot** — Synthetic monitoring

### ADHD-Friendly Summary
```
JSON logs → parseable by aggregators
Sentry → error tracking
Prometheus → metrics
Grafana → dashboards
Alert on p95 > 500ms or error rate > 1%
```

## 🛠️ Code

```python
# logging.py
import json
import logging
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'line': record.lineno,
        })
```

## 🧪 Practice

1. Configure structured JSON logging for Django
2. Add `django-request` logging to track all requests
3. Set up Sentry for error tracking
4. Add a health check endpoint that exposes metrics
5. Create a Grafana dashboard for request rate, error rate, and response time

## 🧠 Key Takeaways

- Structured logs (JSON) are searchable and parseable
- Log at appropriate levels — don't fill prod logs with DEBUG
- Monitor p95/p99 response time, not just average
- Alert on symptoms (error rate, slow responses), not causes
- Sentry catches what logs miss — context-rich error reporting
