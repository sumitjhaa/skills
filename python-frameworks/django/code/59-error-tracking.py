"""Error tracking & alerting: Sentry integration, structured exceptions, notifications."""
import json
import time
import random
import traceback
import sys
from datetime import datetime
from collections import defaultdict


# ======================== Error Event ========================

class ErrorEvent:
    """Represents an error event captured by the error tracker."""
    def __init__(self, exception: Exception, request: dict = None):
        self.exception = exception
        self.request = request or {}
        self.timestamp = datetime.now().isoformat()
        self.event_id = f"evt-{random.randint(100000, 999999)}"
        self._fingerprint = ""
        self.tags: dict = {}
        self.extra: dict = {}
        self.user: dict = {}
        self.level = "error"

    @property
    def fingerprint(self) -> str:
        if not self._fingerprint:
            tb = traceback.extract_tb(sys.exc_info()[2]) if sys.exc_info()[0] else []
            key_parts = [type(self.exception).__name__]
            if tb:
                key_parts.append(tb[-1].filename if tb else "")
                key_parts.append(str(tb[-1].lineno if tb else 0))
            self._fingerprint = ":".join(key_parts)
        return self._fingerprint

    def to_dict(self) -> dict:
        tb = traceback.format_exception(type(self.exception), self.exception, self.exception.__traceback__)
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "level": self.level,
            "exception": {
                "type": type(self.exception).__name__,
                "value": str(self.exception),
                "traceback": tb[-5:] if len(tb) > 5 else tb,  # last 5 frames
            },
            "request": {
                "url": self.request.get("path", ""),
                "method": self.request.get("method", ""),
                "user": self.request.get("user", "anonymous"),
            },
            "fingerprint": self.fingerprint,
            "tags": self.tags,
            "extra": self.extra,
        }


# ======================== Error Tracker (Sentry-like) ========================

class ErrorTracker:
    """Simulates Sentry error tracking."""
    def __init__(self, dsn: str = ""):
        self.dsn = dsn
        self.events: list[ErrorEvent] = []
        self.grouped_events: dict[str, list[ErrorEvent]] = defaultdict(list)

    def capture_exception(self, exc: Exception, request: dict = None):
        event = ErrorEvent(exc, request)
        self.events.append(event)
        self.grouped_events[event.fingerprint].append(event)
        return event.event_id

    def set_context(self, event: ErrorEvent, key: str, value):
        event.extra[key] = value

    def set_user(self, event: ErrorEvent, user_id, email=""):
        event.user = {"id": user_id, "email": email}

    def set_tag(self, event: ErrorEvent, key: str, value: str):
        event.tags[key] = value

    def summary(self) -> dict:
        return {
            "total_events": len(self.events),
            "unique_errors": len(self.grouped_events),
            "by_type": dict(self._count_by_type()),
            "events_per_hour": round(len(self.events) / 24, 1) if self.events else 0,
        }

    def _count_by_type(self) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for event in self.events:
            counts[type(event.exception).__name__] += 1
        return dict(counts)

    def most_frequent(self, n: int = 5) -> list[dict]:
        sorted_groups = sorted(
            self.grouped_events.items(),
            key=lambda x: len(x[1]),
            reverse=True,
        )
        result = []
        for fingerprint, events in sorted_groups[:n]:
            first = events[0]
            result.append({
                "fingerprint": fingerprint,
                "count": len(events),
                "last_seen": events[-1].timestamp,
                "exception_type": type(first.exception).__name__,
                "message": str(first.exception)[:80],
            })
        return result


# ======================== Notification Channels ========================

class NotificationChannel:
    """Abstract notification channel."""
    def send(self, title: str, message: str, severity: str = "info"):
        raise NotImplementedError


class EmailChannel(NotificationChannel):
    def send(self, title: str, message: str, severity: str = "info"):
        return {"channel": "email", "to": "ops@example.com", "title": title, "sent": True}


class SlackChannel(NotificationChannel):
    def send(self, title: str, message: str, severity: str = "info"):
        return {"channel": "slack", "webhook": "https://hooks.slack.com/...", "title": title, "sent": True}


class PagerDutyChannel(NotificationChannel):
    def send(self, title: str, message: str, severity: str = "info"):
        return {"channel": "pagerduty", "severity": severity, "title": title, "sent": True}


# ======================== Alert Notifier ========================

class AlertNotifier:
    """Sends alerts based on error thresholds."""
    def __init__(self):
        self.channels: list[NotificationChannel] = []
        self.thresholds = {
            "error_per_minute": 10,
            "critical_errors": 1,
        }
        self.sent: list[dict] = []

    def add_channel(self, channel: NotificationChannel):
        self.channels.append(channel)

    def evaluate(self, tracker: ErrorTracker) -> list[dict]:
        alerts = []
        summary = tracker.summary()
        # Check if we have critical errors
        critical_count = summary.get("by_type", {}).get("CriticalError", 0)
        if critical_count >= self.thresholds["critical_errors"]:
            for channel in self.channels:
                result = channel.send(
                    "Critical Error Alert",
                    f"{critical_count} critical errors detected",
                    severity="critical",
                )
                self.sent.append(result)
                alerts.append(result)
        return alerts


# ======================== Demo ========================
print("=== Error Tracking & Alerting Demo ===\n")

# --- Error tracker ---
tracker = ErrorTracker(dsn="https://key@sentry.io/project")

# Simulate some errors
errors_to_raise = [
    (ValueError("Invalid post ID: abc"), {"path": "/posts/abc/", "method": "GET", "user": "alice"}),
    (KeyError("missing_field"), {"path": "/api/posts/", "method": "POST", "user": "bob"}),
    (ConnectionError("Database connection refused"), {"path": "/admin/", "method": "GET", "user": "admin"}),
    (ValueError("Invalid post ID: xyz"), {"path": "/posts/xyz/", "method": "GET", "user": "alice"}),
    (PermissionError("User does not have permission"), {"path": "/admin/secrets/", "method": "GET", "user": "bob"}),
    (TimeoutError("Celery task timed out"), {"path": "/reports/generate/", "method": "POST", "user": "admin"}),
    (ValueError("Invalid post ID: 999999"), {"path": "/posts/999999/", "method": "GET", "user": "charlie"}),
    (ConnectionError("Redis connection timeout"), {"path": "/api/search/", "method": "GET", "user": "alice"}),
]

for exc, request in errors_to_raise:
    event_id = tracker.capture_exception(exc, request)
    # Add context
    event = tracker.events[-1]
    tracker.set_tag(event, "environment", "production")
    tracker.set_tag(event, "region", "us-east-1")
    tracker.set_user(event, request.get("user", "?"), f"{request.get('user', '?')}@example.com")

# --- Summary ---
print("1. Error tracker summary:")
summary = tracker.summary()
print(f"   Total events: {summary['total_events']}")
print(f"   Unique errors: {summary['unique_errors']}")
print(f"   By type: {summary['by_type']}")

# --- Most frequent ---
print("\n2. Most frequent errors:")
for freq in tracker.most_frequent(3):
    print(f"   🔴 [{freq['exception_type']}] ({freq['count']}x) {freq['message']}")

# --- Alerting ---
print("\n3. Alert notifications:")
notifier = AlertNotifier()
notifier.add_channel(EmailChannel())
notifier.add_channel(SlackChannel())
notifier.add_channel(PagerDutyChannel())

alerts = notifier.evaluate(tracker)
for alert in alerts:
    print(f"   🔔 {alert['channel']}: {alert['title']}")

# --- Error detail ---
print("\n4. Error detail (last event):")
last_event = tracker.events[-1]
detail = last_event.to_dict()
print(f"   Event: {detail['event_id']}")
print(f"   Exception: {detail['exception']['type']}: {detail['exception']['value']}")
print(f"   Fingerprint: {detail['fingerprint']}")
print(f"   Request: {detail['request']['method']} {detail['request']['url']}")
print(f"   Tags: {detail['tags']}")

# --- Sentry setup ---
print("\n5. Sentry Django configuration:")
sentry_config = """
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn="https://your-dsn@sentry.io/project-id",
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ],
    traces_sample_rate=0.1,  # Sample 10% of transactions
    send_default_pii=False,   # Don't send user PII
    environment="production",
    release="myapp@1.2.3",
)
"""
print(sentry_config.strip())

# --- Error severity levels ---
print("\n6. Error severity levels:")
levels = [
    ("debug", "Development debugging only (ignored in prod)"),
    ("info", "Normal operational messages"),
    ("warning", "Something unexpected but not an error"),
    ("error", "Runtime error that should be investigated"),
    ("critical", "System is down or data loss imminent"),
]
for level, desc in levels:
    print(f"   • {level:10s}: {desc}")
