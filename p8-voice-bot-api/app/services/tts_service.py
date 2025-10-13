from __future__ import annotations

import io
from typing import Literal

from huggingface_hub import InferenceClient

from app.config import get_settings


def synthesize_speech(
    text: str,
    *,
    model: str = "hexgrad/Kokoro-82M",
    provider: str = "fal-ai",
) -> bytes:
    """
    Generate speech audio bytes for the provided text using Hugging Face Inference providers.

    Returns raw audio bytes (usually WAV/PCM for Kokoro via fal-ai provider).
    """
    if not text or not text.strip():
        raise ValueError("Text must be a non-empty string")

    settings = get_settings()
    if not settings.hf_token:
        raise RuntimeError(
            "Missing Hugging Face token. Set HUGGINGFACEHUB_API_TOKEN or HF_TOKEN in your .env"
        )

    client = InferenceClient(provider=provider, api_key=settings.hf_token)
    # For providers, text_to_speech returns audio bytes
    audio_bytes: bytes = client.text_to_speech(text, model=model)
    return audio_bytes
