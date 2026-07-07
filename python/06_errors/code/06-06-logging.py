"""Production error tracking and structured logging."""
import logging
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", handlers=[logging.StreamHandler(), logging.FileHandler("/tmp/app.log", mode="w")])
logger = logging.getLogger(__name__)


def process_transaction(user_id: int, amount: float) -> dict:
    logger.info(f"Processing transaction for user {user_id}")
    if amount <= 0:
        logger.error(f"Invalid amount {amount}")
        raise ValueError(f"Amount must be positive")
    if amount > 10000:
        logger.warning(f"Large transaction: ${amount}")
    result = {"transaction_id": f"TXN-{datetime.now().timestamp():.0f}", "status": "completed"}
    logger.info(f"Completed: {result['transaction_id']}")
    return result


class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({"time": self.formatTime(record), "level": record.levelname, "logger": record.name, "message": record.getMessage()})


json_log = logging.getLogger("json_logger")
json_handler = logging.FileHandler("/tmp/structured.log", mode="w")
json_handler.setFormatter(JSONFormatter())
json_log.addHandler(json_handler)
json_log.setLevel(logging.DEBUG)

try:
    process_transaction(1, 500)
    process_transaction(2, 50000)
    process_transaction(3, -100)
except ValueError as e:
    logger.error(f"Failed: {e}")

json_log.info("Health check passed")
json_log.warning("Disk space low")
print("\nJSON log:", open("/tmp/structured.log").read())
