"""Monitoring & logging: structured logging, metrics, health checks, alerting."""
from typing import Any, Optional
from datetime import datetime
import json
import time
import traceback


# ======================== Structured Logger ========================

class LogLevel:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class StructuredLogger:
    """Produces JSON-structured logs for log aggregation (ELK, Datadog)."""
    def __init__(self, service: str = "fastapi-app", environment: str = "development"):
        self.service = service
        self.environment = environment
        self.logs: list[dict] = []

    def _log(self, level: str, message: str, **extra):
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": self.service,
            "environment": self.environment,
            "level": level,
            "message": message,
            **extra,
        }
        self.logs.append(entry)
        # Simulate stdout output
        print(f"  [{level}] {message} | service={self.service} env={self.environment}")
        if extra:
            relevant = {k: v for k, v in extra.items() if k not in ("timestamp", "service", "environment", "level", "message")}
            if relevant:
                print(f"         extra: {json.dumps(relevant)}")
        return entry

    def info(self, message: str, **extra):
        return self._log(LogLevel.INFO, message, **extra)

    def warning(self, message: str, **extra):
        return self._log(LogLevel.WARNING, message, **extra)

    def error(self, message: str, exc_info: bool = False, **extra):
        if exc_info:
            extra["traceback"] = traceback.format_exc().strip()
        return self._log(LogLevel.ERROR, message, **extra)

    def critical(self, message: str, **extra):
        return self._log(LogLevel.CRITICAL, message, **extra)

    def debug(self, message: str, **extra):
        return self._log(LogLevel.DEBUG, message, **extra)

    def request_log(self, method: str, path: str, status: int, duration_ms: float, ip: str = "", user_id: str = ""):
        return self.info(
            f"{method} {path} → {status}",
            http_method=method,
            path=path,
            status_code=status,
            duration_ms=round(duration_ms, 1),
            client_ip=ip,
            user_id=user_id,
        )

    def export(self) -> list[dict]:
        return self.logs


logger = StructuredLogger(service="fastapi-api", environment="production")


# ======================== Metrics Collector ========================

class MetricsCollector:
    """Collect and expose application metrics."""
    def __init__(self):
        self._counters: dict[str, int] = {}
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = {}
        self._start_time = time.time()

    def increment(self, metric: str, value: int = 1):
        self._counters[metric] = self._counters.get(metric, 0) + value

    def gauge(self, metric: str, value: float):
        self._gauges[metric] = value

    def observe(self, metric: str, value: float):
        if metric not in self._histograms:
            self._histograms[metric] = []
        self._histograms[metric].append(value)

    def request_duration(self, duration_ms: float):
        self.observe("request_duration_ms", duration_ms)
        self.increment("requests_total")

    def snapshot(self) -> dict:
        uptime = time.time() - self._start_time
        metrics = {
            "uptime_seconds": round(uptime),
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
        }

        # Compute histogram stats
        for name, values in self._histograms.items():
            if values:
                metrics[name] = {
                    "count": len(values),
                    "avg": round(sum(values) / len(values), 2),
                    "min": round(min(values), 2),
                    "max": round(max(values), 2),
                    "p50": round(sorted(values)[len(values) // 2], 2),
                    "p95": round(sorted(values)[int(len(values) * 0.95)], 2),
                    "p99": round(sorted(values)[int(len(values) * 0.99)], 2),
                }
        return metrics


metrics = MetricsCollector()


# ======================== Health Check ========================

class HealthCheck:
    """Service health check with component status."""
    def __init__(self):
        self.checks: dict[str, Callable] = {}

    def register(self, name: str, check_fn: Callable):
        self.checks[name] = check_fn

    def run_all(self) -> dict:
        results = {}
        all_healthy = True
        for name, check_fn in self.checks.items():
            try:
                result = check_fn()
                healthy = result.get("healthy", False)
                results[name] = {"healthy": healthy, **result}
                if not healthy:
                    all_healthy = False
            except Exception as e:
                results[name] = {"healthy": False, "error": str(e)}
                all_healthy = False
        return {"status": "healthy" if all_healthy else "degraded", "checks": results}


health = HealthCheck()


# Register health checks
def check_database():
    return {"healthy": True, "latency_ms": 2.3, "connections": 5}

def check_redis():
    return {"healthy": True, "latency_ms": 0.8, "keys": 42}

def check_disk():
    return {"healthy": True, "free_gb": 45.2, "total_gb": 100}

health.register("database", check_database)
health.register("redis", check_redis)
health.register("disk", check_disk)


# ======================== Alert Rules ========================

class AlertRule:
    def __init__(self, name: str, condition: str, severity: str = "warning"):
        self.name = name
        self.condition = condition
        self.severity = severity

    def evaluate(self, metrics_snapshot: dict) -> Optional[dict]:
        # Simple condition evaluation
        if "error_rate" in metrics_snapshot.get("counters", {}):
            error_rate = metrics_snapshot["counters"]["error_rate"]
            if "> 5%" in self.condition and error_rate > 5:
                return {"alert": self.name, "severity": self.severity, "value": error_rate}
            if "> 10%" in self.condition and error_rate > 10:
                return {"alert": self.name, "severity": "critical", "value": error_rate}
        if "request_duration_ms" in metrics_snapshot:
            p95 = metrics_snapshot.get("request_duration_ms", {}).get("p95", 0)
            if "> 500ms" in self.condition and p95 > 500:
                return {"alert": self.name, "severity": self.severity, "value": p95}
        return None


alert_rules = [
    AlertRule("high_error_rate", "error_rate > 5%", "warning"),
    AlertRule("high_latency", "p95_latency > 500ms", "warning"),
    AlertRule("critical_error_rate", "error_rate > 10%", "critical"),
]


# ======================== FastAPI App ========================

class FastAPI:
    def __init__(self):
        self.routes: list[dict] = []

    def get(self, path: str):
        def deco(func):
            self.routes.append({"path": path, "method": "GET", "handler": func})
            return func
        return deco

    def __call__(self, method: str, path: str, **kwargs) -> dict:
        for route in self.routes:
            if route["method"] == method and route["path"] == path:
                start = time.time()
                result = route["handler"](**kwargs)
                duration = (time.time() - start) * 1000
                metrics.request_duration(duration)
                logger.request_log(method, path, 200, duration)
                return {"status": 200, "data": result}
        return {"status": 404, "data": {"detail": "Not Found"}}


app = FastAPI()


# ======================== Endpoints ========================

@app.get("/health")
def health_check():
    result = health.run_all()
    logger.info("Health check requested", status=result["status"])
    return result

@app.get("/metrics")
def metrics_endpoint():
    return metrics.snapshot()

@app.get("/logs")
def logs_endpoint(limit: int = 10):
    logs = logger.export()
    return {"logs": logs[-limit:], "total": len(logs)}

@app.get("/alerts")
def alerts_endpoint():
    snapshot = metrics.snapshot()
    triggered = []
    for rule in alert_rules:
        result = rule.evaluate(snapshot)
        if result:
            triggered.append(result)
    return {"alerts": triggered, "count": len(triggered)}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    duration = 15.0 + (user_id * 2.3)
    metrics.request_duration(duration)
    logger.info("User retrieved", user_id=user_id, duration_ms=round(duration, 1))
    return {"id": user_id, "username": f"user_{user_id}"}


# ======================== Demo ========================
print("=" * 60)
print("  MONITORING & LOGGING DEMO")
print("=" * 60)

# 1. Structured logging
print("\n1. Structured logging examples:")
logger.info("Application started", version="3.0.0", port=8000)
logger.request_log("GET", "/health", 200, 2.5, ip="10.0.0.1")
logger.request_log("POST", "/users", 201, 45.2, ip="10.0.0.2", user_id="42")
logger.warning("High memory usage", memory_percent=87.3, threshold=80)
logger.error("Database connection timeout", exc_info=True, database="postgres")

# 2. Health check
print("\n2. Health check:")
health_result = health.run_all()
print(f"   Status: {health_result['status']}")
for name, check in health_result["checks"].items():
    icon = "✅" if check["healthy"] else "❌"
    print(f"   {icon} {name}: healthy={check['healthy']}")

# 3. Metrics collection
print("\n3. Collecting metrics:")
for i in range(20):
    dur = 20 + (i * 5) + (hash(str(i)) % 100)
    metrics.request_duration(dur)

for i in range(5):
    app("GET", f"/users/{i+1}")

snapshot = metrics.snapshot()
print(f"   Total requests: {snapshot['counters'].get('requests_total', 0)}")
print(f"   Avg duration: {snapshot.get('request_duration_ms', {}).get('avg', 'N/A')}ms")
print(f"   P95 duration: {snapshot.get('request_duration_ms', {}).get('p95', 'N/A')}ms")
print(f"   Uptime: {snapshot['uptime_seconds']}s")

# 4. Alerting
print("\n4. Alert evaluation:")
for i in range(100):
    metrics.request_duration(600 + (i * 10))  # Simulate high latency

snapshot2 = metrics.snapshot()
alerts = []
for rule in alert_rules:
    result = rule.evaluate(snapshot2)
    if result:
        alerts.append(result)
        print(f"   🚨 {result['alert']} (severity: {result['severity']}, value: {result['value']})")

if not alerts:
    print("   No alerts triggered")

# 5. Metrics summary
print("\n5. Full metrics snapshot:")
print(json.dumps(snapshot2, indent=2)[:1000])
