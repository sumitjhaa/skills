# 📘 Django Phase 06 — Lesson 09: Error Tracking & Alerting

> 🎯 **Goal**: Track errors in production with Sentry, group by fingerprint, and get notified on critical failures.

## 📖 Concepts

### Why Error Tracking?
- `500.html` tells you nothing
- `tail -f` logs is reactive
- Sentry/error trackers give you: stack trace, request data, user info, browser info, and auto-grouping

### Sentry Key Concepts

| Concept | Description |
|---------|-------------|
| **Event** | Single error occurrence |
| **Issue** | Group of similar events (same fingerprint) |
| **Fingerprint** | Unique hash based on exception type + location |
| **Release** | Version of your code (for regression tracking) |
| **Transaction** | Full request trace (APM) |
| **Span** | Single operation within a transaction |

### Sentry Integration
```python
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
    traces_sample_rate=0.2,  # Sample 20% of transactions
    send_default_pii=False,
    environment="production",
    release="myapp@1.2.3",
)
```

### Manual Error Capture
```python
from sentry_sdk import capture_message, capture_exception

# Capture an exception
try:
    risky_operation()
except Exception as e:
    capture_exception(e)

# Capture a message
capture_message("Payment webhook received", level="info")

# Add context
from sentry_sdk import set_context, set_user, set_tag

set_user({"id": user.id, "email": user.email})
set_tag("environment", "production")
set_context("payment", {"amount": 99.99, "currency": "USD"})
```

### Alerting Channels

| Channel | Severity | Use Case |
|---------|----------|----------|
| Email | Warning+ | Non-critical |
| Slack | Error+ | Team notification |
| PagerDuty | Critical | On-call escalation |
| SMS | Critical | Major outage |

### Error Severity Levels

| Level | Response |
|-------|----------|
| `debug` | Ignored in production |
| `info` | Logged, no alert |
| `warning` | Slack notification |
| `error` | Slack + email |
| `critical` | PagerDuty + SMS |

### ADHD-Friendly Summary
```
Sentry → error tracking + grouping
Fingerprint → deduplicates same error
Release tracking → find when bug was introduced
Alert on error+ → Slack, critical → PagerDuty
Add context (user, tags) → faster debugging
```

## 🛠️ Code

```python
# sentry.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

def init_sentry(dsn: str, environment: str, release: str):
    sentry_sdk.init(
        dsn=dsn,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=environment,
        release=release,
    )

def capture_error(exception: Exception, request=None, user=None, tags: dict = None):
    with sentry_sdk.push_scope() as scope:
        if user:
            scope.set_user({"id": str(user.id), "email": user.email})
        if tags:
            for k, v in tags.items():
                scope.set_tag(k, v)
        sentry_sdk.capture_exception(exception)
```

## 🧪 Practice

1. Install `sentry-sdk` and configure Django integration
2. Capture an intentional error and view it in Sentry
3. Add user context to errors (user id, email)
4. Add custom tags (environment, version, region)
5. Set up alert rules: Slack for errors, PagerDuty for criticals

## 🧠 Key Takeaways

- Sentry groups similar errors by fingerprint — no duplicate noise
- Always add user context — "who got this error?" is the first question
- Set `traces_sample_rate` to 0.1-0.2 in production (not 1.0)
- Use releases to track when a bug was introduced
- Configure alerts early — don't find out about errors from users
- `send_default_pii=False` for privacy compliance
