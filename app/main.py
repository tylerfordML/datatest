from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api import router as api_router
from app.health import router as health_router
from app.logs.config import setup_logging
from app.middleware.request import RequestIDMiddleware

setup_logging()

app = FastAPI(title="Roman Numeral Service")

app.add_middleware(RequestIDMiddleware)

app.include_router(api_router)
app.include_router(health_router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
