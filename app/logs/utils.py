import logging

def get_logger(name: str, request_id: str | None = None):
    """
    Retrieve a logger instance with optional request context.

    If a request_id is provided, the logger is wrapped in a LoggerAdapter
    to automatically inject the request_id into all log records.
    """

    # Obtain (or create) a named logger.
    # Logger configuration (handlers/formatters) is expected to be
    # initialized once at application startup.
    logger = logging.getLogger(name)

    # When a request ID is available, wrap the logger so that
    # the request_id is included in structured log output.
    if request_id:
        return logging.LoggerAdapter(
            logger,
            {"request_id": request_id}
        )

    # Fallback to a standard logger when no request context exists
    # (e.g., during startup or background tasks).
    return logger
