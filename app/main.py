from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api.router import router as api_router
from app.api.health import router as health_router
from app.logs.config import setup_logging
from app.middleware.request import RequestIDMiddleware

# Initialize structured JSON logging before the application starts
# to ensure all startup and runtime logs follow the same format.
setup_logging()

# Create the FastAPI application instance.
# The title is used for OpenAPI documentation and operational clarity.
app = FastAPI(title="Roman Numeral Service")

# Middleware injects a unique request ID into each request lifecycle.
# This enables end-to-end traceability across logs, metrics, and debugging sessions.
app.add_middleware(RequestIDMiddleware)

# Register the primary API routes (business functionality).
app.include_router(api_router)

# Register the health check endpoint used by orchestration and monitoring systems.
app.include_router(health_router)

# Expose Prometheus-compatible metrics via a dedicated ASGI application.
# Mounted separately to avoid interfering with request middleware and routing logic.
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
