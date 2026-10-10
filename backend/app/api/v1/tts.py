import base64
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.voice.tts import synthesize_speech

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Voice"])


class TTSRequest(BaseModel):
    text: str


@router.post("/synthesize")
async def synthesize_voice(request: TTSRequest):
    try:
        audio_bytes = synthesize_speech(request.text)

        return {
            "status": "success",
            "audio": base64.b64encode(audio_bytes).decode("utf-8"),
            "mime_type": "audio/wav",
        }

    except ValueError as exc:
        logger.warning("TTS validation failed: %s", exc)
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("TTS API failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to generate speech. Please try again.",
        ) from None