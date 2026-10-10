import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.agent import router as agent_router
from app.api.v1.chat import router as chat_router
from app.api.v1.documents import router as documents_router
from app.api.v1.retrieval import router as retrieval_router
from app.api.v1.router import router as v1_router
from app.api.v1.tts import router as tts_router
from app.api.v1.voice import router as voice_router
from app.core.settings import settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


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


# Chat API
app.include_router(chat_router)


# API v1
app.include_router(
    v1_router,
    prefix="/api/v1",
)


# Document APIs
app.include_router(
    documents_router,
    prefix="/api/v1",
)


# Retrieval APIs
app.include_router(
    retrieval_router,
    prefix="/api/v1",
)


# AI Agent APIs
app.include_router(
    agent_router,
    prefix="/api/v1",
)


# Voice APIs - Speech-to-Text
app.include_router(
    voice_router,
    prefix="/api/v1",
)


# Voice APIs - Text-to-Speech
app.include_router(
    tts_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "message": "AI Knowledge Platform API",
        "environment": settings.environment,
    }
