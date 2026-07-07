"""Advanced logging — hierarchy, handlers, formatters, filters, and JSON logging."""

import logging
import logging.handlers
import json
import sys
from pathlib import Path


LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs JSON log records."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


class SensitiveFilter(logging.Filter):
    """Filter out log records containing sensitive keywords."""

    def __init__(self, keywords: list[str] | None = None):
        super().__init__()
        self.keywords = keywords or ["password", "secret", "token"]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(kw in message.lower() for kw in self.keywords)


def setup_logging() -> None:
    """Configure root logger with console and rotating file handlers."""
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Remove default handlers
    root_logger.handlers.clear()

    # Console handler (INFO+)
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    ))
    root_logger.addHandler(console)

    # Rotating file handler (DEBUG+)
    rotating = logging.handlers.RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=1024 * 10,
        backupCount=3,
    )
    rotating.setLevel(logging.DEBUG)
    rotating.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))
    root_logger.addHandler(rotating)

    # JSON file handler (WARNING+)
    json_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "app.json",
        maxBytes=1024 * 10,
        backupCount=3,
    )
    json_handler.setLevel(logging.WARNING)
    json_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(json_handler)

    # Sensitive filter on root
    root_logger.addFilter(SensitiveFilter())


# Module-level loggers
app_logger = logging.getLogger("myapp")
db_logger = logging.getLogger("myapp.database")
api_logger = logging.getLogger("myapp.api")


def simulate_operations() -> None:
    """Run sample operations demonstrating different log levels."""
    app_logger.info("Application started")

    db_logger.debug("Connecting to database")
    db_logger.info("Database connected successfully")
    db_logger.warning("Slow query detected: SELECT * FROM movies")

    api_logger.info("Fetching movie data from external API")
    api_logger.error("API request failed: timeout after 5s", exc_info=True)

    app_logger.critical("Disk space critically low — shutting down")

    # This should be filtered out
    app_logger.info("User password: supersecret123")


def main() -> None:
    setup_logging()
    simulate_operations()
    print(f"\nLogs written to: {LOG_DIR}")


if __name__ == "__main__":
    main()
