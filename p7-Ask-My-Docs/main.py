from __future__ import annotations

from fastapi import FastAPI

from app.config import Settings, load_env
from app.routers.health import router as health_router

# Load environment early
load_env()

settings = Settings()

app = FastAPI(title=settings.app_name)

# Routers
app.include_router(health_router)


# Optional: root path could be same as health check; keeping only router mapping.
# If you want a separate /health path later, move the route there and add another handler for "/".
