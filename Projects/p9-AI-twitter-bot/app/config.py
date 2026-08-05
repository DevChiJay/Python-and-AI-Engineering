from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


# Load nearest .env starting from workspace root
_ENV_LOADED = False


def _load_env() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return

    # Try to find a .env in current working directory or any parent
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        env_path = parent / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path, override=False)
            _ENV_LOADED = True
            break

    # If not found, still call load_dotenv to respect system-level .env
    if not _ENV_LOADED:
        load_dotenv(override=False)
        _ENV_LOADED = True


@dataclass(frozen=True)
class Config:
    # OpenAI
    openai_api_key: Optional[str]

    # Twitter
    twitter_api_key: Optional[str]
    twitter_api_secret: Optional[str]
    twitter_access_token: Optional[str]
    twitter_access_secret: Optional[str]

    # App
    app_env: str
    log_level: str
    scheduler_enabled: bool

    @staticmethod
    def load() -> "Config":
        _load_env()
        return Config(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            twitter_api_key=os.getenv("TWITTER_API_KEY"),
            twitter_api_secret=os.getenv("TWITTER_API_SECRET"),
            twitter_access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            twitter_access_secret=os.getenv("TWITTER_ACCESS_SECRET"),
            app_env=os.getenv("APP_ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            scheduler_enabled=os.getenv("SCHEDULER_ENABLED", "true").lower() in {"1", "true", "yes", "on"},
        )
