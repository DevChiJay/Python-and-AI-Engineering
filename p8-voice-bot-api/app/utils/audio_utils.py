from __future__ import annotations

import base64
import io
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np


def ensure_output_dir(base_dir: str | os.PathLike = "data/outputs") -> Path:
    path = Path(base_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def gen_timestamp_filename(prefix: str = "tts", ext: str = ".wav") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{ts}{ext}"


def save_wav_bytes(audio_bytes: bytes, *, base_dir: str | os.PathLike = "data/outputs") -> Path:
    out_dir = ensure_output_dir(base_dir)
    filename = gen_timestamp_filename()
    path = out_dir / filename
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path


def to_base64(audio_bytes: bytes) -> str:
    return base64.b64encode(audio_bytes).decode("utf-8")


def wav_bytes_from_array(audio: Any, sample_rate: int = 16000) -> bytes:
    """
    Convert a numpy array or torch tensor waveform into WAV bytes using soundfile.

    - audio: 1D array-like float waveform in range [-1, 1]
    - sample_rate: sampling rate of the waveform
    """
    try:
        import soundfile as sf
    except Exception as e:
        raise RuntimeError("soundfile is required to encode WAV bytes") from e

    # Convert to numpy float32 1D
    if hasattr(audio, "detach"):
        data = audio.detach().cpu().numpy()
    else:
        data = np.asarray(audio)
    data = data.astype(np.float32)

    with io.BytesIO() as buf:
        sf.write(buf, data, sample_rate, format="WAV")
        return buf.getvalue()
