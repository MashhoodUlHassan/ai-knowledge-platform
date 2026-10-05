from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="AI Knowledge Platform Backend API",
    version="1.0.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
allow_origins=[
    origin.strip()
    for origin in settings.allowed_origins.split(",")
    if origin.strip()
],    
allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    v1_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "AI Knowledge Platform API",
        "environment": settings.environment,
    }