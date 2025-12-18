import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class HTTPRequestID(BaseHTTPMiddleware):
    async def inject(self, request: Request, response_call):
        http_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = http_id

        http_response = await response_call(request)
        http_response.headers["X-Request-ID"] = http_id
        
        return http_response
