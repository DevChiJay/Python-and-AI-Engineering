from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import Config
from .routers.health import router as health_router
from .routers.admin import router as admin_router
from .services.scheduler import start_scheduler_once

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load configuration
    cfg = Config.load()

    # Start scheduler once per process (safe with uvicorn --reload)
    if cfg.scheduler_enabled:
        start_scheduler_once()

    yield

    # No explicit shutdown; scheduler uses atexit to stop cleanly


def create_app() -> FastAPI:
    app = FastAPI(title="AI Twitter Bot")

    # Include routers
    app.include_router(health_router)
    app.include_router(admin_router)

    return app


app = FastAPI(lifespan=lifespan, title="AI Twitter Bot")
app.include_router(health_router)
app.include_router(admin_router)
