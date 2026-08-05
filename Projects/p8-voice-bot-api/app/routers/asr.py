from __future__ import annotations

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.services.whisper_asr import save_upload, transcribe_audio, WhisperASRError

router = APIRouter(prefix="/asr", tags=["asr"])

ALLOWED_MIME = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"}
ALLOWED_EXT = {".wav", ".mp3"}


def _validate_upload(file: UploadFile):
    content_type = file.content_type or ""
    if content_type not in ALLOWED_MIME:
        # Some clients may not set a precise MIME; fallback to extension check
        import os
        _, ext = os.path.splitext(file.filename or "")
        if ext.lower() not in ALLOWED_EXT:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload .wav or .mp3")


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    _validate_upload(file)

    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file upload")
        saved_path = save_upload(file_bytes, file.filename or "audio_upload.wav")
        text = transcribe_audio(saved_path)
        return JSONResponse({"transcription": text, "file_path": str(saved_path)})
    except WhisperASRError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
