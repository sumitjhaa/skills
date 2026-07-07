"""Performance monitoring: APM, slow query detection, profiling, alerting."""
import json
import time
import random
import statistics
from collections import defaultdict
from datetime import datetime


# ======================== Slow Query Detector ========================

class SlowQueryDetector:
    """Detects and logs slow database queries."""
    def __init__(self, slow_threshold: float = 0.1):
        self.slow_threshold = slow_threshold
        self.slow_queries: list[dict] = []
        self.total_queries = 0

    def record(self, query: str, duration: float, source: str = ""):
        self.total_queries += 1
        if duration > self.slow_threshold:
            entry = {
                "query": query[:100],
                "duration": round(duration, 4),
                "source": source,
                "timestamp": datetime.now().isoformat(),
                "threshold": self.slow_threshold,
            }
            self.slow_queries.append(entry)
            return True
        return False

    def summary(self) -> dict:
        if not self.slow_queries:
            return {"slow_count": 0, "avg_slow_duration": 0}
        durations = [q["duration"] for q in self.slow_queries]
        return {
            "total_queries": self.total_queries,
            "slow_count": len(self.slow_queries),
            "slow_pct": round(len(self.slow_queries) / max(self.total_queries, 1) * 100, 2),
            "avg_slow_duration": round(statistics.mean(durations), 4),
            "max_slow_duration": round(max(durations), 4),
        }

    def top_slow(self, n: int = 5) -> list[dict]:
        return sorted(self.slow_queries, key=lambda x: x["duration"], reverse=True)[:n]


# ======================== APM Simulator ========================

class APMTransaction:
    """Represents a single request transaction tracked by APM."""
    def __init__(self, name: str, method: str = "GET"):
        self.name = name
        self.method = method
        self.start = time.time()
        self.end: float = 0.0
        self.segments: list[dict] = []
        self.error: str = ""
        self.metadata: dict = {}

    def add_segment(self, name: str, category: str, duration: float, meta: dict = None):
        self.segments.append({
            "name": name,
            "category": category,
            "duration": round(duration, 4),
            "meta": meta or {},
        })

    def finish(self):
        self.end = time.time()

    @property
    def duration(self) -> float:
        return round((self.end or time.time()) - self.start, 4)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "method": self.method,
            "duration": self.duration,
            "segments": self.segments,
            "error": self.error,
            "timestamp": datetime.fromtimestamp(self.start).isoformat(),
        }


class APMCollector:
    """Collects and analyzes APM transactions."""
    def __init__(self):
        self.transactions: list[APMTransaction] = []

    def record(self, transaction: APMTransaction):
        self.transactions.append(transaction)

    def stats(self) -> dict:
        durations = [t.duration for t in self.transactions]
        errors = [t for t in self.transactions if t.error]
        if not durations:
            return {}
        return {
            "total_requests": len(self.transactions),
            "avg_duration": round(statistics.mean(durations), 4),
            "p95_duration": round(sorted(durations)[int(len(durations) * 0.95)], 4),
            "p99_duration": round(sorted(durations)[int(len(durations) * 0.99)], 4),
            "max_duration": round(max(durations), 4),
            "error_count": len(errors),
            "error_rate": round(len(errors) / max(len(self.transactions), 1) * 100, 2),
        }

    def slowest_endpoints(self, n: int = 5) -> list[dict]:
        by_name: dict[str, list[float]] = defaultdict(list)
        for t in self.transactions:
            key = f"{t.method} {t.name}"
            by_name[key].append(t.duration)
        result = []
        for endpoint, durations in by_name.items():
            result.append({
                "endpoint": endpoint,
                "avg": round(statistics.mean(durations), 4),
                "max": round(max(durations), 4),
                "count": len(durations),
            })
        return sorted(result, key=lambda x: x["avg"], reverse=True)[:n]


# ======================== Alert Rules ========================

class AlertRule:
    """Defines an alert threshold."""
    def __init__(self, name: str, metric: str, operator: str, threshold: float, severity: str = "warning"):
        self.name = name
        self.metric = metric
        self.operator = operator
        self.threshold = threshold
        self.severity = severity

    def evaluate(self, value: float) -> bool:
        if self.operator == "gt":
            return value > self.threshold
        elif self.operator == "lt":
            return value < self.threshold
        elif self.operator == "gte":
            return value >= self.threshold
        elif self.operator == "lte":
            return value <= self.threshold
        return False


class AlertManager:
    """Manages alert rules and triggers notifications."""
    def __init__(self):
        self.rules: list[AlertRule] = []
        self.alerts: list[dict] = []

    def add_rule(self, rule: AlertRule):
        self.rules.append(rule)

    def check(self, metrics: dict) -> list[dict]:
        triggered = []
        for rule in self.rules:
            value = metrics.get(rule.metric, 0)
            if rule.evaluate(value):
                alert = {
                    "rule": rule.name,
                    "metric": rule.metric,
                    "value": value,
                    "threshold": rule.threshold,
                    "severity": rule.severity,
                    "timestamp": datetime.now().isoformat(),
                }
                self.alerts.append(alert)
                triggered.append(alert)
        return triggered


# ======================== Demo ========================
print("=== Performance Monitoring Demo ===\n")

# --- Slow query detection ---
print("1. Slow query detector (threshold=0.05s):")
detector = SlowQueryDetector(slow_threshold=0.05)

queries = [
    ("SELECT * FROM posts WHERE id = %s", 0.003, "PostDetail"),
    ("SELECT * FROM posts JOIN comments ON ...", 0.320, "PostList"),
    ("SELECT * FROM posts WHERE title ILIKE '%django%'", 0.150, "Search"),
    ("UPDATE posts SET views = views + 1 WHERE id = %s", 0.002, "TrackView"),
    ("SELECT * FROM audit_log ORDER BY created_at DESC", 1.200, "AdminDashboard"),
    ("SELECT COUNT(*) FROM posts WHERE is_published = true", 0.001, "Stats"),
]

for query, duration, source in queries:
    is_slow = detector.record(query, duration, source=source)
    if is_slow:
        print(f"   ⚠ SLOW ({duration:.3f}s): {query[:50]}...")

summary = detector.summary()
print(f"\n   Summary: {summary['slow_count']} slow of {summary['total_queries']} ({summary['slow_pct']}%)")
print(f"   Avg slow: {summary['avg_slow_duration']}s, Max: {summary['max_slow_duration']}s")

# --- APM transactions ---
print("\n2. APM transaction tracking:")
apm = APMCollector()

for _ in range(50):
    t = APMTransaction(random.choice(["post_list", "post_detail", "create_post", "search", "dashboard"]),
                        random.choice(["GET", "POST"]))
    t.add_segment("db_query", "database", random.uniform(0.01, 0.3))
    t.add_segment("template_render", "view", random.uniform(0.005, 0.05))
    if random.random() < 0.05:
        t.add_segment("external_api", "http", random.uniform(0.1, 0.5))
    t.finish()
    if random.random() < 0.03:
        t.error = "DatabaseTimeout"
    apm.record(t)

stats = apm.stats()
print(f"   Requests: {stats['total_requests']}")
print(f"   Avg: {stats['avg_duration']}s, P95: {stats['p95_duration']}s, P99: {stats['p99_duration']}s")
print(f"   Error rate: {stats['error_rate']}%")

print("\n   Slowest endpoints:")
for ep in apm.slowest_endpoints(3):
    print(f"     • {ep['endpoint']}: avg={ep['avg']}s (n={ep['count']})")

# --- Alert rules ---
print("\n3. Alerting rules:")
alerts = AlertManager()
alerts.add_rule(AlertRule("High error rate", "error_rate", "gt", 5.0, "critical"))
alerts.add_rule(AlertRule("Slow response time", "p95_duration", "gt", 0.5, "warning"))
alerts.add_rule(AlertRule("High DB load", "db_connections", "gt", 50, "warning"))

triggered = alerts.check({"error_rate": 3.2, "p95_duration": 0.8, "db_connections": 12})
for alert in triggered:
    print(f"   🔔 [{alert['severity']}] {alert['rule']}: {alert['value']} > {alert['threshold']}")

# --- Recommended setup ---
print("\n4. Recommended production monitoring stack:")
stack = [
    ("Sentry", "Error tracking + performance (slow queries, APM)"),
    ("New Relic / Datadog / Scout APM", "Full APM with transaction traces"),
    ("Prometheus + Grafana", "Custom metrics and dashboards"),
    ("pg_stat_statements", "PostgreSQL slow query tracking"),
    ("django-silk", "Request profiling in development"),
    ("django-debug-toolbar", "Query debugging in development"),
    ("Uptime Robot / Pingdom", "Synthetic monitoring (uptime checks)"),
    ("PagerDuty / Opsgenie", "Alert notifications"),
]
for name, desc in stack:
    print(f"   🔸 {name}: {desc}")
