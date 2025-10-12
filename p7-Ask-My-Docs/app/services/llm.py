from __future__ import annotations

import os
from typing import Optional

from langchain.chat_models import init_chat_model

from ..config import Settings, load_env


load_env()


def get_chat_model(model_name: Optional[str] = None):
    """Initialize and return a LangChain chat model using OpenAI provider.

    Respects OPENAI_API_KEY from environment. Model name can be overridden.
    """
    settings = Settings()
    name = model_name or settings.model_name
    # Ensure key is present; if not, LangChain/OpenAI will raise at first call.
    if not os.environ.get("OPENAI_API_KEY") and settings.openai_api_key:
        os.environ["OPENAI_API_KEY"] = settings.openai_api_key
    return init_chat_model(name, model_provider="openai")
