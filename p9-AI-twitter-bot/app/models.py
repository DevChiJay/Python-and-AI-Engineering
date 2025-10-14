from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ScheduledPost:
    id: str
    text: str
    scheduled_at: datetime
    posted_at: Optional[datetime] = None


__all__ = ["ScheduledPost"]
