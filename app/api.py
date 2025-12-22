from fastapi import APIRouter, Query, HTTPException, Request
from app.service import RomanNumeralTranslateService
from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    CONVERSION_COUNT
)
from app.logs.utils import get_logger
import asyncio
import time

# Router isolates HTTP concerns from application bootstrap
router = APIRouter()

# Service encapsulates pure domain logic (no HTTP or framework dependencies)
service = RomanNumeralTranslateService()


@router.get("/romannumeral")
async def convert_roman(
    request: Request,
    query: int | None = Query(None),
    min: int | None = Query(None),
    max: int | None = Query(None),
):
    # Logger is request-scoped via request_id to support traceability
    logger = get_logger(__name__, request.state.request_id)

    # Track request start time for latency metrics
    start_time = time.time()
    endpoint = "/romannumeral"

    try:
        # Log receipt of request for debugging and traffic analysis
        logger.info("request_received")

        # --- Single-value conversion path ---
        # Used when the `query` parameter is provided
        if query is not None:
            # Increment metric for single conversions
            CONVERSION_COUNT.labels(type="single").inc()

            # Delegate conversion to domain service
            result = {
                "input": str(query),
                "output": service.convert(query),
            }

            HTTPstatus = 200
            return result

        # --- Range conversion path ---
        # Used when both `min` and `max` are provided
        if min is not None and max is not None:
            # Validate range bounds early to avoid undefined behavior
            if min >= max:
                raise ValueError("min must be less than max")

            # Increment metric for range conversions
            CONVERSION_COUNT.labels(type="range").inc()

            # Async wrapper enables parallel execution of conversions
            async def convert_async(n: int):
                return {
                    "input": str(n),
                    "output": service.convert(n),
                }

            # Create tasks for all values in the requested range (inclusive)
            tasks = [convert_async(i) for i in range(min, max + 1)]

            # Execute conversions concurrently and preserve order
            results = await asyncio.gather(*tasks)

            HTTPstatus = 200
            return {"conversions": results}

        # If neither single nor range parameters are valid, fail fast
        raise ValueError("Invalid query parameters")

    except ValueError as e:
        # All domain validation errors are treated as client errors (400)
        HTTPstatus = 400

        # Log invalid input with context for debugging
        logger.warning(
            "invalid_input",
            extra={"error": str(e), "query": query, "min": min, "max": max}
        )

        raise HTTPException(status_code=400, detail=str(e))

    finally:
        # Compute request latency regardless of success or failure
        latency = time.time() - start_time

        # Record latency histogram for performance monitoring
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)

        # Increment request counter with method, endpoint, and status
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(HTTPstatus),
        ).inc()

        # Final structured log summarizing request outcome
        logger.info(
            "request_completed",
            extra={"latency_seconds": latency, "status": HTTPstatus}
        )
