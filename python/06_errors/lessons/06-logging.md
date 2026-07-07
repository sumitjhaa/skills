# 📝 Logging
<!-- ⏱️ 10 min read | 🟡 Medium | 🧠 Applied -->

**What You'll Learn:** How to use Python's `logging` module — levels, handlers, formatters, file logging, and structured logging.

> 💡 **TL;DR — The whole point:** `print()` is for debugging. `logging` is for production — levels, timestamps, file output, and structured error tracking.

## 🔗 Why This Matters
Context managers clean up resources. Logging tells you what happened. In production, you need to know: when did the error happen? Which module? How severe? Logging gives you all of this.

## The Concept
The `logging` module has four components:
- **Logger** — your code interface (`logger.info("msg")`)
- **Handler** — where it goes (console, file, network)
- **Formatter** — how it looks (timestamp, level, message)
- **Level** — how important it is (DEBUG → INFO → WARNING → ERROR → CRITICAL)

Use `getLogger(__name__)` to create a logger per module — the logger name automatically matches your module path.

## Code Example

```python
"""Production error tracking and structured logging."""

import logging
import json
from datetime import datetime

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/tmp/app.log", mode="w"),
    ],
)

logger = logging.getLogger(__name__)


def process_transaction(user_id: int, amount: float) -> dict:
    """Process a transaction with structured logging."""
    logger.info(f"Processing transaction", extra={"user_id": user_id, "amount": amount})

    if amount <= 0:
        logger.error(f"Invalid amount {amount} for user {user_id}")
        raise ValueError(f"Amount must be positive")

    if amount > 10000:
        logger.warning(f"Large transaction: ${amount} by user {user_id}")

    result = {"transaction_id": f"TXN-{datetime.now().timestamp():.0f}", "status": "completed", "amount": amount}
    logger.info(f"Transaction completed: {result['transaction_id']}")
    return result


def setup_json_logger(name: str, path: str) -> logging.Logger:
    """Create a logger that outputs JSON for machine parsing."""
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            return json.dumps({
                "time": self.formatTime(record),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            })

    log = logging.getLogger(name)
    handler = logging.FileHandler(path, mode="w")
    handler.setFormatter(JSONFormatter())
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    return log


# Demo
json_log = setup_json_logger("json_logger", "/tmp/structured.log")

try:
    process_transaction(1, 500)
    process_transaction(2, 50000)
    process_transaction(3, -100)
except ValueError as e:
    logger.error(f"Transaction failed: {e}")

json_log.info("System health check passed")
json_log.warning("Disk space low: 85% used")

print("\nJSON log output:")
print(open("/tmp/structured.log").read())
```

## 🔍 How It Works
- `basicConfig()` sets up a root logger with a StreamHandler
- Logger names follow module hierarchy — `getLogger(__name__)` creates `"module.sub"`
- Child loggers propagate to parents by default
- `RotatingFileHandler` rolls over at a max size (great for production)
- Never log sensitive data (passwords, tokens, PII)

## ⚠️ Common Pitfall
Using `print()` in production code. `print()` goes to stdout with no levels, no timestamps, no filtering. Use `logging` from day one.

## 🧠 Memory Aid
**"DEBUG = dev, INFO = ops, WARNING = odd, ERROR = broke, CRITICAL = fire"**: Five levels, from least to most severe. Use them consistently.

## 🏃 Try It
Set up a logger with two handlers: a `StreamHandler` at INFO level and a `RotatingFileHandler` at DEBUG level. Write a small program with messages at each level.

## 🔗 Related
- [Context Managers →](./05-context-managers.md)
- [ExceptionGroup →](./07-exceptiongroup.md)

## ➡️ Next
[ExceptionGroup](./07-exceptiongroup.md)
