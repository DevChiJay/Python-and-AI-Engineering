from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body

from app.models import save_post_result
from app.services.content_generator import generate_content
from app.services.poster import TwitterClient

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@router.post("/generate")
async def generate(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    topic = payload.get("topic")
    style = (payload.get("style") or "thread").lower()
    result = generate_content(topic=topic, style=style)
    # Include topic in result for easier persistence later
    result.setdefault("metadata", {})
    result["metadata"]["topic"] = topic
    return result


@router.post("/post")
async def post_content(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Post content JSON previously generated; expects shape from generate_content.

    payload example:
      {
        "type": "tweet"|"thread",
        "items": ["..."],
        "prompt_used": "...",
        "metadata": {"topic": "...", "hashtags": ["#...", ...]},
        // optional media: [ ["path1","path2"], ["pathA"] ] aligned to items
        "media": [ ["..."], null, ... ]
      }
    """
    kind = (payload.get("type") or "thread").lower()
    items: List[str] = payload.get("items") or []
    media: Optional[List[Optional[List[str]]]] = payload.get("media")

    client = TwitterClient()
    if kind == "tweet":
        media_paths = media[0] if media and len(media) > 0 else None
        res = client.post_tweet(items[0] if items else "", media_paths=media_paths)
    else:
        res = client.post_thread(items, list_of_media_paths_per_tweet=media)

    record_id = save_post_result(kind=kind, request=payload, response=res)
    return {"record_id": record_id, "result": res}
