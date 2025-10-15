from __future__ import annotations

import atexit
import logging
import os
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


class _SchedulerSingleton:
    _instance: Optional[BackgroundScheduler] = None

    @classmethod
    def get(cls) -> BackgroundScheduler:
        if cls._instance is None:
            # Configure the scheduler; daemon so it won't block process exit
            scheduler = BackgroundScheduler(daemon=True)
            cls._instance = scheduler
            # Ensure clean shutdown at interpreter exit
            atexit.register(cls._shutdown_if_running)
        return cls._instance

    @classmethod
    def start_once(cls) -> BackgroundScheduler:
        scheduler = cls.get()
        if not scheduler.running:
            logger.info("Starting BackgroundScheduler")
            scheduler.start()
            try:
                _ensure_jobs(scheduler)
            except Exception as e:
                logger.exception("Failed to initialize jobs: %s", e)
        else:
            logger.debug("BackgroundScheduler already running; skip start")
        return scheduler

    @classmethod
    def _shutdown_if_running(cls) -> None:
        try:
            sch = cls._instance
            if sch and sch.running:
                logger.info("Shutting down BackgroundScheduler at exit")
                sch.shutdown(wait=False)
        except Exception:  # best-effort on interpreter shutdown
            pass


get_scheduler = _SchedulerSingleton.get
start_scheduler_once = _SchedulerSingleton.start_once


# --- Jobs ------------------------------------------------------------------

def _ensure_jobs(scheduler: BackgroundScheduler) -> None:
    # Add a daily job at 09:00 UTC by default
    hour = int(os.getenv("JOB_HOUR_UTC", "9"))
    minute = int(os.getenv("JOB_MINUTE_UTC", "0"))
    job_id = "daily_generate_and_post"
    if not scheduler.get_job(job_id):
        scheduler.add_job(daily_generate_and_post, "cron", id=job_id, hour=hour, minute=minute)
        logger.info("Scheduled job '%s' at %02d:%02d UTC", job_id, hour, minute)


def daily_generate_and_post() -> None:
    """Generate content and post it once per day.

    Honors poster cooldown and records results to DB.
    """
    try:
        from app.services.content_generator import generate_content
        from app.services.poster import TwitterClient
        from app.models import save_generated, mark_generated_post_result

        # Generate
        result = generate_content(topic=None, style=os.getenv("DEFAULT_STYLE", "thread"))
        gen_id = save_generated(
            topic=result.get("metadata", {}).get("topic"),
            style=result.get("type", "thread"),
            prompt_used=result.get("prompt_used"),
            content=result,
        )

        # Post
        client = TwitterClient()
        if result.get("type") == "tweet":
            post_res = client.post_tweet((result.get("items") or [""])[0])
        else:
            post_res = client.post_thread(result.get("items") or [])

        # Persist
        mark_generated_post_result(gen_id, post_res)
        logger.info("Daily job posted: %s", post_res)
    except Exception:
        logger.exception("daily_generate_and_post failed")
