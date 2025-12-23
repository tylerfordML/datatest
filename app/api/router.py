from fastapi import APIRouter, Query, HTTPException, Request
from typing import Optional
import asyncio
import time

from app.service.roman import RomanNumeralTranslateService
from app.models import (
    RomanNumeralResponse,
    RomanNumeralRangeResponse,
    ErrorResponse
)
from app.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    CONVERSION_COUNT
)
from app.logs.utils import get_logger

router = APIRouter(
    prefix="/v1",
    tags=["Roman Numerals"]
)

service = RomanNumeralTranslateService()


@router.get(
    "/romannumeral",
    summary="Convert integer(s) to Roman numerals",
    description=(
        "Convert a single integer or a range of integers into Roman numerals.\n\n"
        "- Use `query` for single conversion\n"
        "- Use `min` and `max` for range conversion\n"
        "- Valid values: 1–255"
    ),
    response_model=RomanNumeralResponse | RomanNumeralRangeResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Invalid input or invalid range"
        }
    }
)
async def convert_roman(
    request: Request,
    query: Optional[int] = Query(
        None,
        description="Single integer to convert",
        examples=10
    ),
    min: Optional[int] = Query(
        None,
        description="Minimum value for range conversion",
        examples=1
    ),
    max: Optional[int] = Query(
        None,
        description="Maximum value for range conversion",
        examples=10
    ),
):
    logger = get_logger(__name__, request.state.request_id)
    start_time = time.time()
    endpoint = "/v1/romannumeral"
    HTTPstatus = 500  # safe default for metrics/logging

    if query is not None and (min is not None or max is not None):
        HTTPstatus = 400
        raise HTTPException(
            status_code=400,
            detail="Provide either 'query' or 'min' and 'max', not both"
        )

    try:
        logger.info("request_received")

        # ---- Single conversion ----
        if query is not None:
            CONVERSION_COUNT.labels(type="single").inc()

            result = {
                "input": str(query),
                "output": service.convert(query),
            }

            HTTPstatus = 200
            return result

        # ---- Range conversion ----
        if min is not None and max is not None:
            if min >= max:
                raise ValueError("min must be less than max")

            CONVERSION_COUNT.labels(type="range").inc()

            async def convert_async(n: int):
                return {
                    "input": str(n),
                    "output": service.convert(n),
                }

            tasks = [convert_async(i) for i in range(min, max + 1)]
            results = await asyncio.gather(*tasks)

            HTTPstatus = 200
            return {"conversions": results}

        raise ValueError("Invalid query parameters")

    except ValueError as e:
        HTTPstatus = 400
        logger.warning(
            "invalid_input",
            extra={"error": str(e), "query": query, "min": min, "max": max}
        )
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        latency = time.time() - start_time

        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status=str(HTTPstatus),
        ).inc()

        logger.info(
            "request_completed",
            extra={"latency_seconds": latency, "status": HTTPstatus}
        )
