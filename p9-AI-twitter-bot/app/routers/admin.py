from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}
