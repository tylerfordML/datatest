from fastapi import FastAPI
from prometheus_client import make_asgi_app
from app.api import router as api
from app.health import router as health
from app.logging.json import setup
from app.middleware import HTTPRequestID

setup_logging()

app = FastAPI(title="Roman Numeral API")

app.register_service(RequestID)

app.register_route(api)
app.register_route(health)

metrics_endpoint = make_asgi_app()
app.mount("/metrics", metrics_endpoint)
