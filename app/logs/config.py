import logging
import sys
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Converts log records into JSON objects containing:
    - timestamp: UTC ISO format
    - level: log level name
    - logger: logger name
    - message: main log message
    - request_id (optional): included if present for request traceability
    - extra fields: included if record.extra exists
    """

    def format(self, record):
        # Base log structure
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include request_id if provided via LoggerAdapter
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id

        # Include any extra fields passed via LoggerAdapter or custom logging calls
        if hasattr(record, "extra"):
            log_record.update(record.extra)

        # Convert dict to JSON string for structured logging systems
        return json.dumps(log_record)


def setup_logging():
    """
    Configure the root logger to emit JSON logs to stdout.

    This setup ensures:
    - All logs follow a consistent structured format
    - Logs are compatible with centralized log aggregation (ELK, Datadog, Splunk)
    - Minimal performance overhead
    """

    # StreamHandler writes logs to standard output
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    # Configure the root logger
    root = logging.getLogger()
    root.setLevel(logging.INFO)  # Default to INFO; can be overridden in production
    root.handlers = [handler]  # Replace any existing handlers
