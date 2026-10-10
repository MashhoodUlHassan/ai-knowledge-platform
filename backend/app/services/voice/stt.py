import logging
import tempfile
from pathlib import Path

from google import genai

from app.core.settings import settings

logger = logging.getLogger(__name__)

client = genai.Client(api_key=settings.gemini_api_key)

STT_MODEL = "gemini-3.5-transcribe"


def transcribe_audio(
    audio_bytes: bytes,
    mime_type: str = "audio/webm",
) -> str:
    if not audio_bytes:
        raise ValueError("Audio data cannot be empty.")

    temp_path = None

    try:
        # Normalize MIME type and determine file extension.
        mime_type = mime_type.split(";")[0].strip().lower()

        mime_extensions = {
            "audio/webm": ".webm",
            "audio/mp3": ".mp3",
            "audio/mpeg": ".mp3",
            "audio/wav": ".wav",
            "audio/x-wav": ".wav",
            "audio/ogg": ".ogg",
            "audio/m4a": ".m4a",
            "audio/mp4": ".m4a",
            "audio/aac": ".aac",
            "audio/flac": ".flac",
        }

        suffix = mime_extensions.get(mime_type, ".webm")

        # Save uploaded audio temporarily.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = Path(temp_file.name)

        # Explicitly set MIME type during upload.
        audio_file = client.files.upload(
            file=str(temp_path),
            config={"mime_type": mime_type},
        )

        # Transcribe audio using Gemini.
        interaction = client.interactions.create(
            model=STT_MODEL,
            input=[
                {
                    "type": "audio",
                    "uri": audio_file.uri,
                    "mime_type": mime_type,
                }
            ],
        )

        transcript = (interaction.output_text or "").strip()

        if not transcript:
            raise ValueError(
                "No speech was detected in the audio."
            )

        logger.info(
            "Audio transcription completed successfully: length=%s",
            len(transcript),
        )

        return transcript

    except Exception:
        logger.exception("Audio transcription failed")
        raise

    finally:
        # Always remove the temporary local audio file.
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                logger.warning(
                    "Could not remove temporary audio file: %s",
                    temp_path,
                )