from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routers.health import router as health_router
from app.routers.tts import router as tts_router
from app.routers.asr import router as asr_router
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("voice-bot")

app = FastAPI(title="voice-bot-api")

# Access settings once so they are loaded and cached
settings = get_settings()

# Include routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(tts_router)
app.include_router(asr_router)


@app.get("/")
async def root():
    return {"name": app.title, "env": settings.environment}


# Optional: run with `python -m app` if package
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
