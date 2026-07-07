"""Logging & monitoring: structured logging, log levels, aggregation."""
import json
import logging
import time
import random
from datetime import datetime
from collections import defaultdict


# ======================== Structured Logging ========================

class StructuredFormatter(logging.Formatter):
    """Format logs as JSON for log aggregation tools."""
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "value": str(record.exc_info[1]),
            }
        return json.dumps(log_entry)


class Logger:
    """Wrapper around logging with structured output."""
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(StructuredFormatter())
            self.logger.addHandler(handler)

    def _log(self, level: str, message: str, **extra):
        record = self.logger.makeRecord(
            self.logger.name,
            getattr(logging, level.upper()),
            "", 0, message, (), None,
        )
        record.extra_fields = extra
        self.logger.handle(record)

    def info(self, msg: str, **kwargs):
        self._log("INFO", msg, **kwargs)
    def warning(self, msg: str, **kwargs):
        self._log("WARNING", msg, **kwargs)
    def error(self, msg: str, **kwargs):
        self._log("ERROR", msg, **kwargs)
    def critical(self, msg: str, **kwargs):
        self._log("CRITICAL", msg, **kwargs)
    def debug(self, msg: str, **kwargs):
        self._log("DEBUG", msg, **kwargs)


# ======================== Request Logging Middleware ========================

class RequestLogger:
    """Simulates request logging middleware."""
    def __init__(self):
        self.log = Logger("django.request")
        self.requests: list[dict] = []

    def log_request(self, method: str, path: str, status: int, duration: float, user: str = "anonymous"):
        entry = {
            "method": method,
            "path": path,
            "status": status,
            "duration_ms": round(duration * 1000, 2),
            "user": user,
            "timestamp": datetime.now().isoformat(),
        }
        self.requests.append(entry)
        level = "INFO" if status < 400 else "WARNING" if status < 500 else "ERROR"
        getattr(self.log, level.lower())(
            f"{method} {path} → {status}",
            **entry,
        )
        return entry


# ======================== Metrics Collector ========================

class MetricsCollector:
    """Simple metrics collection (counters, gauges, histograms)."""
    def __init__(self):
        self.counters: dict[str, int] = defaultdict(int)
        self.gauges: dict[str, float] = {}
        self.histograms: dict[str, list[float]] = defaultdict(list)

    def increment(self, metric: str, value: int = 1):
        self.counters[metric] += value

    def gauge(self, metric: str, value: float):
        self.gauges[metric] = value

    def observe(self, metric: str, value: float):
        self.histograms[metric].append(value)

    def snapshot(self) -> dict:
        return {
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": {
                k: {
                    "count": len(v),
                    "avg": round(sum(v) / len(v), 2) if v else 0,
                    "max": max(v) if v else 0,
                    "p95": sorted(v)[int(len(v) * 0.95)] if v else 0,
                }
                for k, v in self.histograms.items()
            },
        }


# ======================== Log Aggregation ========================

class LogAggregator:
    """Simulates log aggregation (like ELK, Datadog, or Loki)."""
    def __init__(self):
        self.logs: list[dict] = []

    def ingest(self, log_entry: dict):
        self.logs.append(log_entry)

    def search(self, query: str, limit: int = 10) -> list[dict]:
        query = query.lower()
        results = []
        for entry in self.logs:
            if query in json.dumps(entry).lower():
                results.append(entry)
                if len(results) >= limit:
                    break
        return results

    def errors_by_endpoint(self) -> dict[str, int]:
        errors = defaultdict(int)
        for entry in self.logs:
            if entry.get("level") in ("ERROR", "CRITICAL"):
                path = entry.get("path", "unknown")
                errors[path] += 1
        return dict(errors)

    def stats(self) -> dict:
        total = len(self.logs)
        levels = defaultdict(int)
        for entry in self.logs:
            levels[entry.get("level", "UNKNOWN")] += 1
        return {
            "total_logs": total,
            "by_level": dict(levels),
            "error_rate": round(levels.get("ERROR", 0) / max(total, 1) * 100, 2),
        }


# ======================== Demo ========================
print("=== Logging & Monitoring Demo ===\n")

# --- Structured logging ---
print("1. Structured logging (JSON):")
log = Logger("myapp")
log.info("User registered", user_id=42, email="alice@example.com")
log.warning("Rate limit approaching", client_ip="203.0.113.5", current_rate=95, limit=100)
try:
    raise ValueError("Database connection timeout")
except ValueError as e:
    log.error("Request failed", path="/api/posts/", status=500, error=str(e))

# --- Request logging ---
print("\n2. Request logging:")
req_logger = RequestLogger()
for method, path, status, dur in [
    ("GET", "/posts/", 200, 0.045),
    ("GET", "/posts/1/", 200, 0.032),
    ("POST", "/posts/", 201, 0.120),
    ("GET", "/admin/", 403, 0.015),
    ("GET", "/nonexistent/", 404, 0.010),
    ("POST", "/posts/", 400, 0.025),
    ("GET", "/api/error/", 500, 2.300),
]:
    req_logger.log_request(method, path, status, dur, user="alice" if "admin" not in path else "bob")

# --- Metrics ---
print("\n3. Metrics collection:")
metrics = MetricsCollector()
metrics.increment("http.requests.total", 150)
metrics.increment("http.requests.error", 3)
metrics.gauge("db.connections.active", 12)
metrics.gauge("celery.queue.size", 5)
for _ in range(100):
    metrics.observe("http.request.duration", random.uniform(0.01, 0.5))
for _ in range(10):
    metrics.observe("db.query.duration", random.uniform(0.001, 0.1))

snapshot = metrics.snapshot()
print(f"   Requests: {snapshot['counters']}")
print(f"   Gauges: {snapshot['gauges']}")
print(f"   Request duration: avg={snapshot['histograms']['http.request.duration']['avg']}s")
print(f"   DB query duration: avg={snapshot['histograms']['db.query.duration']['avg']}s")

# --- Log aggregation ---
print("\n4. Log aggregation:")
aggregator = LogAggregator()
for entry in req_logger.requests:
    aggregator.ingest(entry)

stats = aggregator.stats()
print(f"   Total: {stats['total_logs']}, Errors: {stats['error_rate']}%")
print(f"   Errors by endpoint: {aggregator.errors_by_endpoint()}")

errors = aggregator.search("500")
print(f"   Search '500': {len(errors)} results")

# --- Log configuration ---
print("\n5. Django LOGGING config (for settings.py):")
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structured": {"()": "myapp.logging.StructuredFormatter"},
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "structured"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/var/log/django/app.log",
            "maxBytes": 10485760,
            "backupCount": 5,
            "formatter": "structured",
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO"},
        "django.request": {"handlers": ["console", "file"], "level": "WARNING"},
        "myapp": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
    },
}
print(f"   Loggers: {list(logging_config['loggers'].keys())}")
print(f"   Handlers: {list(logging_config['handlers'].keys())}")
print(f"   Formatters: {list(logging_config['formatters'].keys())}")

print("\n6. Monitoring tools:")
tools = [
    ("Sentry", "Error tracking & performance monitoring"),
    ("Datadog", "Full observability platform"),
    ("New Relic", "APM & infrastructure monitoring"),
    ("Prometheus + Grafana", "Open-source metrics & dashboards"),
    ("ELK Stack", "Log aggregation (Elasticsearch, Logstash, Kibana)"),
    ("Loki + Grafana", "Log aggregation (like Prometheus for logs)"),
]
for name, desc in tools:
    print(f"   🔸 {name}: {desc}")
