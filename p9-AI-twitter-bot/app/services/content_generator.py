from __future__ import annotations

from typing import Optional

# Placeholder for content generation logic (e.g., using OpenAI)


def generate_tweet(topic: Optional[str] = None) -> str:
    base = "Hello, Twitter!"
    if topic:
        return f"{base} Here's a thought about {topic}."
    return base
