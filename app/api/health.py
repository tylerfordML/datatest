from fastapi import APIRouter

# Router dedicated to lightweight operational endpoints
# such as health and readiness checks.
router = APIRouter()

@router.get("/health")
def health_check():
    """
    Health check endpoint used by load balancers, container orchestrators,
    and monitoring systems to verify that the service is running.

    This endpoint performs no external dependency checks and returns
    immediately, making it suitable for liveness probes.
    """
    return {"status": "ok"}
