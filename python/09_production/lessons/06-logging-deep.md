# 🎯 Logging Deep
<!-- ⏱️ 14 min read | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Configure Python's logging module — log levels, handlers, formatters, file rotation, and structured logging.

> 💡 **TL;DR — The whole point:** `print()` is for debugging. `logging` is for production — it captures timestamps, severity levels, and can be redirected without changing code.

## 🔗 Why This Matters
When a production system fails, logs are your first place to look. Good logging tells you what happened, when, and in what order. Bad logging (or `print` statements) leaves you guessing.

## The Concept
- **Levels:** DEBUG < INFO < WARNING < ERROR < CRITICAL
- **Handlers:** send log records to console, file, network, etc.
- **Formatters:** control the output format (timestamp, level, message)
- **Loggers:** hierarchical, named with dots (`app.db`, `app.api`)
- **Rotating File Handler:** splits logs by size or time

## Code Example
```python
"""E-commerce: Structured logging for order processing."""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional


def setup_logging(log_dir: str = "logs", verbose: bool = False) -> logging.Logger:
    Path(log_dir).mkdir(exist_ok=True)
    log_file = Path(log_dir) / "orders.log"

    # Root logger config
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    console.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    root.addHandler(console)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    root.addHandler(file_handler)

    return logging.getLogger(__name__)


logger = setup_logging(verbose=True)


class OrderService:
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.OrderService")

    def create_order(self, customer: str, items: list[dict]) -> Optional[str]:
        self.logger.info(f"Creating order for {customer} with {len(items)} items")

        if not items:
            self.logger.warning(f"Empty order attempted by {customer}")
            return None

        try:
            total = sum(item["price"] * item["qty"] for item in items)
            order_id = f"ORD-{hash(customer + str(total)) % 1000:03d}"
            self.logger.info(f"Order {order_id} created: ${total:.2f} for {customer}")
            return order_id
        except KeyError as e:
            self.logger.error(f"Invalid item data: {e}", exc_info=True)
            return None


service = OrderService()

# Successful order
order_id = service.create_order("Alice", [
    {"name": "Laptop", "price": 1499.99, "qty": 1}
])
print(f"Order result: {order_id}")

# Failed order
bad_order = service.create_order("Bob", [])
print(f"Bad order: {bad_order}")

# Error order
error_order = service.create_order("Charlie", [{"name": "Test"}])
print(f"Error order: {error_order}")
```

## 🔍 How It Works
- `getLogger(__name__)` creates a logger with a dotted name based on the module
- Messages propagate to parent loggers unless `propagate = False`
- `RotatingFileHandler` keeps logs at 1MB each, with 3 backups
- `exc_info=True` in log calls includes the full traceback
- Different handlers can have different levels — DEBUG to file, INFO to console
- `logging.getLogger().setLevel()` controls the minimum level

## ⚠️ Common Pitfall
Logging sensitive data (passwords, credit cards, PII). Never log secrets. Use `logging.Filter` to redact sensitive fields. Also, beware of `logging.debug(f"...")` — f-strings are always evaluated even if the message isn't logged. Use `logging.debug("...", arg)` with % formatting instead.

## 🧠 Memory Aid
"DEBUG = dev, INFO = ops, WARNING = fishy, ERROR = broke, CRITICAL = fire. Console = INFO, File = DEBUG."

## 🏃 Try It
Add a JSON formatter that outputs `{"timestamp": ..., "level": ..., "logger": ..., "message": ...}`. Configure it as a second file handler. Write some test log entries and inspect the JSON output.

## 🔗 Related
- [Argparse](05-argparse.md) — `--verbose` flag controls log level
- [Pytest Deep](15-pytest-deep.md) — testing with `caplog` fixture

## ➡️ Next
[Type Checking](07-type-checking.md)
