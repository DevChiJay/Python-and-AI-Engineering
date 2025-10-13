from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.tts import router as tts_router
from app.config import get_settings

app = FastAPI(title="voice-bot-api")

# Access settings once so they are loaded and cached
settings = get_settings()

# Include routers
app.include_router(health_router)
app.include_router(tts_router)


@app.get("/")
async def root():
    return {"name": app.title, "env": settings.environment}


# Optional: run with `python -m app` if package
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
