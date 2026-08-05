from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel


class HealthResponse(BaseModel):
    name: str
    status: str


router = APIRouter()


@router.get("/", response_model=HealthResponse, tags=["system"], summary="Service health check")
async def root_health() -> HealthResponse:
    return HealthResponse(name="ask-my-docs", status="ok")
