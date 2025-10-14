from __future__ import annotations

import io
from typing import Optional

from gtts import gTTS


def synthesize_speech_gtts(text: str, *, lang: str = "en", slow: bool = False, tld: str = "com") -> bytes:
    if not text or not text.strip():
        raise ValueError("Text must be a non-empty string")
    # gTTS writes only MP3; capture into bytes buffer
    tts = gTTS(text=text, lang=lang, slow=slow, tld=tld)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    return buf.getvalue()
