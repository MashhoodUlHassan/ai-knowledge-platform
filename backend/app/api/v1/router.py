from fastapi import APIRouter, Depends

from app.api.deps import get_settings
from app.core.settings import Settings

router = APIRouter()


@router.get("/health")
def health_check(settings: Settings = Depends(get_settings)):
    return {
        "status": "healthy",
        "message": "API v1 is working!",
        "environment": settings.environment,
    }