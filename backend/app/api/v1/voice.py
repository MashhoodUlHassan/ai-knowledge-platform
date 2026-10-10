import logging

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.voice.stt import transcribe_audio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/transcribe")
async def transcribe_voice(
    audio: UploadFile = File(...),
):
    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Audio file is empty.",
            )

        mime_type = audio.content_type or "audio/webm"

        transcript = transcribe_audio(
            audio_bytes=audio_bytes,
            mime_type=mime_type,
        )

        logger.info(
            "Voice transcription API completed: filename=%s",
            audio.filename,
        )

        return {
            "status": "success",
            "transcript": transcript,
        }

    except ValueError as exc:
        logger.warning("Voice transcription validation failed: %s", exc)
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except HTTPException:
        raise

    except Exception:
        logger.exception("Voice transcription API failed")
        raise HTTPException(
            status_code=500,
            detail="Unable to transcribe audio. Please try again.",
        ) from None