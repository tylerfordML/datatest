import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

# Module-level logger used for middleware-level diagnostics if needed
logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsible for request traceability.

    Behavior:
    - If the client provides an `X-Request-ID` header, propagate it.
    - Otherwise, generate a new UUID.
    - Attach the request ID to both the request lifecycle and response headers.

    This enables correlation of logs and metrics across distributed systems.
    """

    async def dispatch(self, request: Request, call_next):
        # Use client-provided request ID when available to support upstream tracing.
        # Fall back to a generated UUID to guarantee every request is traceable.
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Attach request ID to request state for access by handlers and loggers.
        request.state.request_id = request_id

        # Continue processing the request through the middleware chain.
        response = await call_next(request)

        # Echo request ID back to the client for debugging and correlation.
        response.headers["X-Request-ID"] = request_id

        return response
