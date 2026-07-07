# 📘 Django Phase 06 — Lesson 08: Performance Monitoring & APM

> 🎯 **Goal**: Monitor production performance — slow query detection, APM traces, and alerting.

## 📖 Concepts

### What to Monitor

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Response time (p95) | < 200ms | 200-500ms | > 500ms |
| Error rate | < 0.1% | 0.1-1% | > 1% |
| DB query time | < 10ms | 10-50ms | > 50ms |
| Cache hit rate | > 90% | 80-90% | < 80% |
| CPU usage | < 50% | 50-80% | > 80% |
| Memory usage | < 70% | 70-85% | > 85% |

### APM (Application Performance Monitoring)
APM tools trace a request through your entire stack:

```
Browser → Nginx → Gunicorn → Django → DB/Redis/API
  ↑        ↑        ↑         ↑          ↑
  T1       T2       T3        T4         T5
```

Each span (segment) has timing, allowing you to see where time is spent.

### Slow Query Detection
```sql
-- PostgreSQL: find slow queries
SELECT query, calls, total_time / calls AS avg_time,
       rows, shared_blks_hit, shared_blks_read
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;
```

### Profiling in Development

| Tool | What It Shows |
|------|--------------|
| `django-debug-toolbar` | SQL queries, cache, signals on every page |
| `django-silk` | Full request profiling with call stacks |
| `py-spy` | Sampling profiler for Python |
| `cProfile` | Built-in Python profiler |

### Alert Rules

| Rule | Condition | Action |
|------|-----------|--------|
| High error rate | > 5% in 5 minutes | PagerDuty |
| Slow p95 | > 500ms for 5 minutes | Slack |
| DB connection spike | > 80% of pool | Slack |
| Disk space | < 10% free | Email |
| Health check fails | 3 consecutive failures | PagerDuty |

### ADHD-Friendly Summary
```
Sentry APM → trace slow requests
pg_stat_statements → find slow queries
django-debug-toolbar → dev profiling
Alert on p95 > 500ms
Alert on error rate > 1%
```

## 🛠️ Code

```python
# monitoring.py
import time
import logging
from django.db import connection

logger = logging.getLogger('myapp.performance')

class QueryCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        queries = len(connection.queries)
        total_time = sum(float(q.get('time', 0)) for q in connection.queries)
        if queries > 20:
            logger.warning(
                "High query count",
                extra={'path': request.path, 'queries': queries, 'time': total_time},
            )
        return response


class SlowQueryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_threshold = 0.1  # 100ms

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start
        if duration > 1.0:
            logger.warning("Slow request", extra={
                'path': request.path, 'duration': duration,
            })
        return response
```

## 🧪 Practice

1. Install `django-debug-toolbar` and check query count on a page
2. Add `pg_stat_statements` and find the top 5 slowest queries
3. Set up Sentry APM to trace transactions
4. Create a Grafana dashboard with p95 response time, error rate, DB query time
5. Set up alerts for high error rate and slow p95

## 🧠 Key Takeaways

- Profile before optimizing — measure, then fix
- Track p95/p99, not just average (averages hide problems)
- APM traces show where time is spent in each request
- `pg_stat_statements` is the best tool for finding slow DB queries
- Alert on symptoms (high response time), not causes (high CPU)
- Set up monitoring on day 1 — don't wait for an outage
