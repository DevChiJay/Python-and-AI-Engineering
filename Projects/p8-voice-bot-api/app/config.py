from functools import lru_cache
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from a .env file if present
load_dotenv()

class Settings(BaseModel):
    # Define any settings you need here; placeholders for future voice-bot use
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    # Support both common env var names
    hf_token: str | None = os.getenv("HUGGINGFACEHUB_API_TOKEN") or os.getenv("HF_TOKEN")
    environment: str = os.getenv("ENVIRONMENT", "development")
    # Optional path to a local SpeechT5 speaker embedding (.npy or .pt)
    speecht5_xvector_path: str | None = os.getenv("SPEECHT5_XVECTOR_PATH")
    allowed_origins: list[str] = (
        [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()] or ["*"]
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
