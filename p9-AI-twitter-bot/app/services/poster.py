from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional, Sequence

from app.config import Config
from app.models import can_post_now, update_last_post_time


class TwitterClient:
    """Thin wrapper over Tweepy (Twitter/X API v2) with optional media via v1.1.

    Requires the following env vars via Config:
      - TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    """

    def __init__(self) -> None:
        self.cfg = Config.load()

        self.consumer_key = self.cfg.twitter_api_key
        self.consumer_secret = self.cfg.twitter_api_secret
        self.access_token = self.cfg.twitter_access_token
        self.access_secret = self.cfg.twitter_access_secret

        missing = [
            name
            for name, val in [
                ("TWITTER_API_KEY", self.consumer_key),
                ("TWITTER_API_SECRET", self.consumer_secret),
                ("TWITTER_ACCESS_TOKEN", self.access_token),
                ("TWITTER_ACCESS_SECRET", self.access_secret),
            ]
            if not val
        ]
        if missing:
            self._init_error = f"Missing Twitter credentials: {', '.join(missing)}"
        else:
            self._init_error = None

        self._client = None
        self._api_v1 = None

    def _ensure_client(self):
        if self._init_error:
            raise RuntimeError(self._init_error)
        if self._client is None:
            try:
                import tweepy  # type: ignore

                self._client = tweepy.Client(
                    consumer_key=self.consumer_key,
                    consumer_secret=self.consumer_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_secret,
                )
            except Exception as e:  # pragma: no cover
                raise RuntimeError(f"Failed to init Tweepy Client: {e}")
        return self._client

    def _ensure_api_v1(self):
        if self._init_error:
            raise RuntimeError(self._init_error)
        if self._api_v1 is None:
            try:
                import tweepy  # type: ignore

                auth = tweepy.OAuth1UserHandler(
                    self.consumer_key,
                    self.consumer_secret,
                    self.access_token,
                    self.access_secret,
                )
                self._api_v1 = tweepy.API(auth)
            except Exception as e:  # pragma: no cover
                raise RuntimeError(f"Failed to init Tweepy API v1.1: {e}")
        return self._api_v1

    def _upload_media(self, media_paths: Sequence[str]) -> List[str]:
        media_ids: List[str] = []
        if not media_paths:
            return media_ids
        api = self._ensure_api_v1()
        for p in media_paths:
            res = api.media_upload(p)
            media_ids.append(res.media_id_string)
        return media_ids

    @staticmethod
    def _tweet_url(tweet_id: str) -> str:
        # Generic URL that redirects to the tweet without needing username
        return f"https://x.com/i/web/status/{tweet_id}"

    # --- Public methods -------------------------------------------------
    def post_tweet(
        self,
        text: str,
        media_paths: Optional[Sequence[str]] = None,
        in_reply_to_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Cooldown: one post per hour by default (override via env POST_COOLDOWN_SECONDS)
        cooldown_seconds = int(os.getenv("POST_COOLDOWN_SECONDS", "3600"))
        allowed, remaining = can_post_now("default_account", cooldown_seconds)
        if not allowed and not in_reply_to_id:
            return {"ok": False, "error": f"Rate limited. Try again in {remaining} seconds."}

        tries = int(os.getenv("POST_RETRIES", "3"))
        base_sleep = float(os.getenv("POST_BACKOFF_BASE", "1.0"))
        last_err: Optional[Exception] = None
        for attempt in range(tries):
            try:
                client = self._ensure_client()
                media_ids: Optional[List[str]] = None
                if media_paths:
                    media_ids = self._upload_media(list(media_paths))

                kwargs: Dict[str, Any] = {"text": text}
                if in_reply_to_id:
                    kwargs["in_reply_to_tweet_id"] = in_reply_to_id
                if media_ids:
                    kwargs["media"] = {"media_ids": media_ids}

                resp = client.create_tweet(**kwargs)
                tweet_id = str(resp.data.get("id"))
                if not in_reply_to_id:
                    update_last_post_time("default_account")
                return {"ok": True, "tweet_id": tweet_id, "url": self._tweet_url(tweet_id)}
            except Exception as e:
                last_err = e
                # naive transient detection: retry on generic exceptions
                if attempt < tries - 1:
                    time.sleep(base_sleep * (2 ** attempt))
                else:
                    return {"ok": False, "error": str(e)}

    def post_thread(
        self,
        list_of_texts: Sequence[str],
        list_of_media_paths_per_tweet: Optional[Sequence[Optional[Sequence[str]]]] = None,
    ) -> Dict[str, Any]:
        if not list_of_texts:
            return {"ok": False, "error": "list_of_texts is empty"}
        last_id: Optional[str] = None
        root_id: Optional[str] = None
        urls: List[str] = []

        try:
            for idx, text in enumerate(list_of_texts):
                media = None
                if list_of_media_paths_per_tweet and idx < len(list_of_media_paths_per_tweet):
                    media = list_of_media_paths_per_tweet[idx]
                res = self.post_tweet(text, media_paths=media, in_reply_to_id=last_id)
                if not res.get("ok"):
                    return res
                last_id = res.get("tweet_id")
                if root_id is None:
                    root_id = last_id
                urls.append(res.get("url", ""))

            return {
                "ok": True,
                "tweet_id": root_id,
                "url": self._tweet_url(root_id or ""),
                "items": [{"tweet_id": tid, "url": url} for tid, url in zip([root_id, *([None] * (len(urls) - 1))], urls)],
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}


__all__ = ["TwitterClient"]
