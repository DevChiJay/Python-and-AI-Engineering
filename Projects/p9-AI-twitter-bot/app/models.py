from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# --- Database setup --------------------------------------------------------

DB_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'twitter_bot.db'))}")

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


class PostRecord(Base):
    __tablename__ = "post_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String(20), nullable=False)  # tweet or thread
    topic = Column(String(500), nullable=True)
    prompt_used = Column(Text, nullable=True)
    request_json = Column(Text, nullable=False)
    response_json = Column(Text, nullable=True)
    root_tweet_id = Column(String(64), nullable=True)
    root_url = Column(String(1024), nullable=True)
    post_ok = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


def init_db() -> None:
    # Ensure parent directory exists for SQLite
    if DB_URL.startswith("sqlite:"):
        try:
            db_path = DB_URL.split("sqlite:///")[-1]
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        except Exception:
            pass
    Base.metadata.create_all(bind=engine)


def save_post_result(kind: str, request: Dict[str, Any], response: Optional[Dict[str, Any]]) -> int:
    init_db()
    rec = PostRecord(
        kind=kind,
        topic=(request.get("topic") if isinstance(request, dict) else None),
        prompt_used=(request.get("prompt_used") if isinstance(request, dict) else None),
        request_json=json.dumps(request or {}, ensure_ascii=False),
        response_json=json.dumps(response or {}, ensure_ascii=False) if response is not None else None,
        root_tweet_id=(response or {}).get("tweet_id") if isinstance(response, dict) else None,
        root_url=(response or {}).get("url") if isinstance(response, dict) else None,
        post_ok=(response or {}).get("ok") if isinstance(response, dict) else None,
    )
    with SessionLocal() as session:
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec.id


# --- Generated content records --------------------------------------------

class GeneratedRecord(Base):
    __tablename__ = "generated_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(500), nullable=True)
    style = Column(String(20), nullable=False, default="thread")
    prompt_used = Column(Text, nullable=True)
    content_json = Column(Text, nullable=False)  # stored JSON from generate_content
    status = Column(String(20), nullable=False, default="generated")  # generated|posted|failed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    posted_at = Column(DateTime, nullable=True)
    external_id = Column(String(64), nullable=True)
    external_url = Column(String(1024), nullable=True)


class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_key = Column(String(200), nullable=False, unique=True)
    last_posted_at = Column(DateTime, nullable=True)
    __table_args__ = (UniqueConstraint("account_key", name="uq_rate_limits_account_key"),)


def save_generated(topic: Optional[str], style: str, prompt_used: Optional[str], content: Dict[str, Any]) -> int:
    init_db()
    rec = GeneratedRecord(
        topic=topic,
        style=style,
        prompt_used=prompt_used,
        content_json=json.dumps(content, ensure_ascii=False),
        status="generated",
    )
    with SessionLocal() as session:
        session.add(rec)
        session.commit()
        session.refresh(rec)
        return rec.id


def get_generated(gen_id: int) -> Optional[GeneratedRecord]:
    init_db()
    with SessionLocal() as session:
        return session.get(GeneratedRecord, gen_id)


def mark_generated_post_result(gen_id: int, response: Dict[str, Any]) -> None:
    init_db()
    with SessionLocal() as session:
        rec = session.get(GeneratedRecord, gen_id)
        if not rec:
            return
        ok = bool(response.get("ok"))
        rec.status = "posted" if ok else "failed"
        rec.posted_at = datetime.utcnow()
        rec.external_id = response.get("tweet_id")
        rec.external_url = response.get("url")
        session.add(rec)
        session.commit()


def can_post_now(account_key: str, cooldown_seconds: int) -> tuple[bool, int]:
    """Return (allowed, seconds_remaining)."""
    init_db()
    from datetime import timedelta

    now = datetime.utcnow()
    with SessionLocal() as session:
        rl = session.query(RateLimit).filter_by(account_key=account_key).one_or_none()
        if rl is None:
            rl = RateLimit(account_key=account_key, last_posted_at=None)
            session.add(rl)
            session.commit()
        if rl.last_posted_at is None:
            return True, 0
        delta = (now - rl.last_posted_at).total_seconds()
        if delta >= cooldown_seconds:
            return True, 0
        return False, int(cooldown_seconds - delta)


def update_last_post_time(account_key: str) -> None:
    init_db()
    with SessionLocal() as session:
        rl = session.query(RateLimit).filter_by(account_key=account_key).one_or_none()
        if rl is None:
            rl = RateLimit(account_key=account_key)
        from datetime import datetime as _dt
        rl.last_posted_at = _dt.utcnow()
        session.add(rl)
        session.commit()


__all__ = [
    "PostRecord",
    "init_db",
    "save_post_result",
    "GeneratedRecord",
    "RateLimit",
    "save_generated",
    "get_generated",
    "mark_generated_post_result",
    "can_post_now",
    "update_last_post_time",
]
