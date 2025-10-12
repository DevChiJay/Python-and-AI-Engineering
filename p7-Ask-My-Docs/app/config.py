from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


def load_env(override: bool = False) -> None:
    """Load environment variables from a .env file if present.

    Parameters
    ----------
    override: bool
        If True, values from .env will override existing environment variables.
    """
    load_dotenv(override=override)


def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable with an optional default."""
    return os.environ.get(key, default)


@dataclass(frozen=True)
class Settings:
    app_name: str = get_env("APP_NAME", "Ask My Docs") or "Ask My Docs"
    model_name: str = get_env("MODEL_NAME", "gpt-5-mini") or "gpt-5-mini"
    openai_api_key: Optional[str] = get_env("OPENAI_API_KEY")
