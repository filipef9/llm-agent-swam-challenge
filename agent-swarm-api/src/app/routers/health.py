from datetime import datetime

from fastapi import APIRouter

from app.domain.models import HealthCheckResponse

health_router = APIRouter()


@health_router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify if the API is running.

    Returns:
        dict: A dictionary with service status and current timestamp.
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
