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
