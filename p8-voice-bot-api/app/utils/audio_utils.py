from __future__ import annotations

import base64
import os
from datetime import datetime
from pathlib import Path


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
