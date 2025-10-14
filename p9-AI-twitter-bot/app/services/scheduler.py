from __future__ import annotations

import atexit
import logging
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
