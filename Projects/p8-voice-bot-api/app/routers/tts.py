from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.tts_service import synthesize_speech, synthesize_speech_local_speecht5
from app.services.gtts_service import synthesize_speech_gtts
from app.utils.audio_utils import save_wav_bytes, save_audio_bytes, to_base64


router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str
    # Optional flags to control response
    return_base64: bool = False


class GTTSRequest(TTSRequest):
    lang: str = "en"
    slow: bool = False
    tld: str = "com"


@router.post("/generate")
async def generate_tts(payload: TTSRequest):
    try:
        audio_bytes = synthesize_speech(payload.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if payload.return_base64:
        b64 = to_base64(audio_bytes)
        return {"audio_base64": b64, "content_type": "audio/wav"}

    # default: save to file and return path
    path = save_wav_bytes(audio_bytes)
    return {"file_path": str(path)}


@router.post("/local")
async def generate_tts_local(payload: TTSRequest):
    try:
        audio_bytes = synthesize_speech_local_speecht5(payload.text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if payload.return_base64:
        b64 = to_base64(audio_bytes)
        return {"audio_base64": b64, "content_type": "audio/wav"}

    path = save_wav_bytes(audio_bytes)
    return {"file_path": str(path)}


@router.post("/gtts")
async def generate_tts_gtts(payload: GTTSRequest):
    try:
        audio_bytes = synthesize_speech_gtts(
            payload.text, lang=payload.lang, slow=payload.slow, tld=payload.tld
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if payload.return_base64:
        b64 = to_base64(audio_bytes)
        return {"audio_base64": b64, "content_type": "audio/mpeg"}

    path = save_audio_bytes(audio_bytes, ext=".mp3")
    return {"file_path": str(path)}
