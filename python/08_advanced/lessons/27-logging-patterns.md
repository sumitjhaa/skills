# 🎯 Logging Patterns: dictConfig, RotatingFileHandler, extra Context
<!-- ⏱️ 14 min | 🟡 Applied | 🧠 Applied -->

**What You'll Learn:** Configure structured JSON logging with `dictConfig`, rotating file handlers, and per-module loggers with `extra` context.

> 💡 **TL;DR — The whole point:** `logging.config.dictConfig` gives you one-shot centralized config for formatters, handlers, and loggers; `RotatingFileHandler` manages log file sizes; and `extra={}` adds structured context to every log record.

## 🔗 Why This Matters
Production apps send logs to ELK/Loki/Datadog — they need JSON format. Log files must rotate to avoid filling disks. Every log line should carry context like `order_id` and `user_id` for debugging.

## The Concept
`dictConfig` replaces manual `setLevel`, `addHandler` calls with a single dict defining the entire logging pipeline. `RotatingFileHandler` writes to `app.log` and creates `app.log.1, .2, .3` when it reaches `maxBytes`. The `extra` parameter adds arbitrary key-value pairs to the log record, accessible via `%(key)s` in the format string.

## Code Example
```python
"""Logging patterns: JSON format, rotating files, structured context — production apps"""
import logging, logging.config, logging.handlers, sys, json

# --- 1. Per-module logger: standard pattern for every Python module ---
logger = logging.getLogger(__name__)  # Gets logger named after module path

# --- 2. dictConfig: one-shot config (from JSON/YAML in real apps) ---
logging.config.dictConfig({
    "version": 1,
    "formatters": {
        "simple": {"format": "%(levelname)s | %(name)s | %(message)s"},
        "json": {  # Structured logging for log aggregation (ELK, Loki, Datadog)
            "format": '{"time":"%(asctime)s","level":"%(levelname)s","module":"%(name)s","msg":"%(message)s"}',
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log", "maxBytes": 1024*1024, "backupCount": 3,  # 1MB, 3 backups
            "formatter": "json",
        },
    },
    "loggers": {
        "app": {"handlers": ["file"], "level": "DEBUG"},
        "": {"handlers": ["console"], "level": "INFO"},  # Root logger
    },
})

# --- 3. extra: add structured context to log records (key=value pairs) ---
logger.info("Order processed", extra={"order_id": "ORD-123", "user_id": 42})

# --- Usage ---
print(f"Logger name: {logger.name}, effective level: {logging.getLevelName(logger.getEffectiveLevel())}")
print(f"Check app.log for JSON output (rotating at 1MB)")
```

## 🔍 How It Works
- `dictConfig` with `version: 1` configures `formatters` (how messages look), `handlers` (where they go), and `loggers` (which handlers + level per module)
- `RotatingFileHandler(maxBytes=1MB, backupCount=3)` rotates at 1MB, keeping 3 backups (`app.log.1` through `.3`)
- `extra={"key": "val"}` makes `%(key)s` available in the format string — the JSON formatter includes it
- The root logger (`""`) catches anything not handled by a named logger — set it to `WARNING` in production
- `logging.getLogger(__name__)` gives each module its own logger named after its dotted path

## ⚠️ Common Pitfall
`dictConfig` can only be called once (subsequent calls are ignored unless `incremental=True` or `disable_existing_loggers=False`). Call it at application startup before any module creates its logger. Use `force=True` (Python 3.8+) to reconfigure.

## 🧠 Memory Aid
"dictConfig = 'one dict to rule all logs.' RotatingFileHandler = 'auto-split big log files.' extra = 'sticky notes on log records.'"

## 🏃 Try It
Add a `TimedRotatingFileHandler` that rotates logs at midnight instead of by size. Configure it with `when='midnight'` and `backupCount=7`. Write a log every second for 10 seconds and check the rotation.

## 🔗 Related
- [Logging](../../../06_errors/lessons/06-logging.md) — logging basics, levels, basicConfig

## ➡️ Next
[CSV Patterns](28-csv-patterns.md)
