from __future__ import annotations

from typing import Optional

from huggingface_hub import InferenceClient

from app.config import get_settings
from app.utils.audio_utils import wav_bytes_from_array

# ===== Remote provider TTS (Kokoro via fal-ai) =====


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


# ===== Local TTS using SpeechT5 =====
_processor = None
_model = None
_vocoder = None
_speaker_embeddings = None
_device = None


def _load_local_speecht5_models():
    global _processor, _model, _vocoder, _speaker_embeddings, _device
    if _processor is not None:
        return

    try:
        import torch
        from transformers import (
            SpeechT5ForTextToSpeech,
            SpeechT5Processor,
            SpeechT5HifiGan,
        )
    except Exception as e:
        raise RuntimeError(
            "Missing dependencies for local SpeechT5. Please install 'torch' and 'transformers'."
        ) from e

    _device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    _model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(_device)
    _vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(_device)

    # Load speaker embedding
    settings = get_settings()
    _speaker_embeddings = _load_or_generate_speaker_embedding(settings.speecht5_xvector_path)


def synthesize_speech_local_speecht5(text: str) -> bytes:
    """
    Generate speech using local microsoft/speecht5_tts and return WAV bytes.
    """
    if not text or not text.strip():
        raise ValueError("Text must be a non-empty string")

    _load_local_speecht5_models()

    # Defer imports to after model load for type clarity
    import torch

    inputs = _processor(text=text, return_tensors="pt")
    input_ids = inputs["input_ids"].to(_device)

    with torch.no_grad():
        speech = _model.generate_speech(input_ids, _speaker_embeddings, vocoder=_vocoder)

    # speech is a 1D torch tensor (float32) sampled at 16kHz
    wav_bytes = wav_bytes_from_array(speech, sample_rate=16000)
    return wav_bytes


def _load_or_generate_speaker_embedding(path: Optional[str]):
    """Load xvector from a .pt or .npy file; otherwise generate a deterministic synthetic embedding.

    Returns a 2D tensor of shape (1, 512) on the proper device.
    """
    import torch
    import os
    import numpy as np

    dim = 512
    if path and os.path.exists(path):
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pt":
            vec = torch.load(path, map_location="cpu")
            if isinstance(vec, dict) and "xvector" in vec:
                vec = vec["xvector"]
            vec = torch.as_tensor(vec, dtype=torch.float32)
        elif ext == ".npy":
            vec = torch.from_numpy(np.load(path)).float()
        else:
            raise RuntimeError(f"Unsupported xvector file extension: {ext}. Use .pt or .npy")
        if vec.ndim == 1:
            vec = vec.unsqueeze(0)
        return vec.to(_device)

    # Fallback: deterministic pseudo-speaker embedding
    g = torch.Generator().manual_seed(42)
    vec = torch.randn((1, dim), generator=g)
    return vec.to(_device)
