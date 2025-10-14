from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from app.config import get_settings
from typing import Any

try:
    from openai import OpenAI  # type: ignore
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore


INPUT_DIR = Path("data/inputs")
INPUT_DIR.mkdir(parents=True, exist_ok=True)


class WhisperASRError(RuntimeError):
    pass


def _get_client() -> Any:
    settings = get_settings()
    api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise WhisperASRError("Missing OPENAI_API_KEY in environment or .env file")
    if OpenAI is None:
        raise WhisperASRError("openai package not installed. Add 'openai' to requirements.")
    return OpenAI(api_key=api_key)


def save_upload(file_bytes: bytes, filename: str) -> Path:
    """Persist uploaded audio into data/inputs and return path."""
    safe_name = filename.replace("..", "_").replace("/", "_").replace("\\", "_")
    path = INPUT_DIR / safe_name
    with open(path, "wb") as f:
        f.write(file_bytes)
    return path


def transcribe_audio(file_path: Path, *, model: str = "whisper-1", language: Optional[str] = None) -> str:
    """
    Transcribe audio using OpenAI Whisper API.
    Returns transcription text.
    """
    client = _get_client()

    # New OpenAI Python SDK (>=1.0) usage pattern
    with open(file_path, "rb") as audio_f:
        params = {
            "model": model,
            "file": audio_f,
        }
        if language:
            params["language"] = language
        try:
            response = client.audio.transcriptions.create(**params)  # type: ignore[attr-defined]
        except Exception as e:  # pragma: no cover
            raise WhisperASRError(f"Whisper API call failed: {e}") from e

    # Response format: object with 'text'
    text = getattr(response, "text", None)
    if not text:
        # Fallback: older dict-like
        if isinstance(response, dict) and "text" in response:
            text = response["text"]
    if not text:
        raise WhisperASRError("No transcription text returned by API")
    return text
