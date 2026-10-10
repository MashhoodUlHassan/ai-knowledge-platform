import io
import logging
import wave

from google import genai
from google.genai import types

from app.core.settings import settings

logger = logging.getLogger(__name__)

client = genai.Client(
    api_key=settings.gemini_api_key
)

TTS_MODEL = "gemini-2.5-flash-preview-tts"

# Gemini TTS PCM output settings
SAMPLE_RATE = 24000
CHANNELS = 1
SAMPLE_WIDTH = 2  # 16-bit PCM


def pcm_to_wav(pcm_data: bytes) -> bytes:
    """Convert raw PCM audio into a browser-compatible WAV file."""

    if not pcm_data:
        raise ValueError(
            "PCM audio data cannot be empty."
        )

    wav_buffer = io.BytesIO()

    with wave.open(wav_buffer, "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm_data)

    return wav_buffer.getvalue()


def synthesize_speech(text: str) -> bytes:
    text = text.strip()

    if not text:
        raise ValueError(
            "Text cannot be empty."
        )

    try:
        response = client.models.generate_content(
            model=TTS_MODEL,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"
                        )
                    )
                ),
            ),
        )

        audio_data = (
            response
            .candidates[0]
            .content
            .parts[0]
            .inline_data
            .data
        )

        if not audio_data:
            raise ValueError(
                "No audio was generated."
            )

        # Gemini returns raw PCM.
        # Convert it to a valid WAV file
        # so browsers can play it.
        wav_audio = pcm_to_wav(
            audio_data
        )

        logger.info(
            "Text-to-speech completed successfully: "
            "text_length=%s, pcm_size=%s, wav_size=%s",
            len(text),
            len(audio_data),
            len(wav_audio),
        )

        return wav_audio

    except Exception:
        logger.exception(
            "Text-to-speech failed"
        )
        raise
