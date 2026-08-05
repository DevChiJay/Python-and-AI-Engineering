from __future__ import annotations

import os
import re
from typing import Any, Dict, Iterable, List, Optional

from app.config import Config
from app.utils.text_utils import truncate as _truncate


# --- Helpers ---------------------------------------------------------------

MAX_TWEET_LEN = 280


def _truncate_tweet(text: str, max_len: int = MAX_TWEET_LEN) -> str:
    return _truncate(text, max_len=max_len)


def _chunk_text(text: str, max_len: int = MAX_TWEET_LEN) -> List[str]:
    """Split text into <= max_len chunks, attempting to break on paragraph, sentence, then word.

    Guarantees each chunk length <= max_len.
    """
    # Normalize whitespace and split by paragraphs first
    paragraphs: List[str] = [p.strip() for p in re.split(r"\n{2,}|\r\n{2,}", text) if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]

    chunks: List[str] = []

    def _emit_chunk(c: str):
        if c:
            chunks.append(_truncate_tweet(c, max_len))

    for para in paragraphs:
        if len(para) <= max_len:
            _emit_chunk(para)
            continue

        # Split by sentences
        sentences = re.split(r"(?<=[.!?])\s+", para)
        buf = ""
        for s in sentences:
            if not s:
                continue
            if len(s) > max_len:
                # Fallback: word-based chunking for long sentences
                words = s.split()
                for w in words:
                    if not buf:
                        buf = w
                    elif len(buf) + 1 + len(w) <= max_len:
                        buf += " " + w
                    else:
                        _emit_chunk(buf)
                        buf = w
                if buf:
                    _emit_chunk(buf)
                    buf = ""
            else:
                if not buf:
                    buf = s
                elif len(buf) + 1 + len(s) <= max_len:
                    buf += " " + s
                else:
                    _emit_chunk(buf)
                    buf = s
        if buf:
            _emit_chunk(buf)
            buf = ""

    return chunks


def _top_words(corpus: str, limit: int = 3) -> List[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_]{2,}", corpus)
    # Simple scoring: longer words first, then frequency
    freq: Dict[str, int] = {}
    for w in words:
        key = w.lower()
        freq[key] = freq.get(key, 0) + 1
    scored = sorted(freq.items(), key=lambda kv: (kv[1], len(kv[0])), reverse=True)
    return [w for w, _ in scored[:limit]]


def _suggest_hashtags(topic: Optional[str], content: str, limit: int = 3) -> List[str]:
    seeds: List[str] = []
    if topic:
        seeds.extend(_top_words(topic, limit=limit))
    if len(seeds) < limit:
        more = _top_words(content, limit=limit)
        for m in more:
            if m not in seeds:
                seeds.append(m)
            if len(seeds) >= limit:
                break
    if not seeds:
        seeds = ["AI", "Python", "Tech"]
    # Format as hashtags (CamelCase-ish)
    tags = ["#" + re.sub(r"[^A-Za-z0-9]", "", s.title()) for s in seeds[:limit]]
    # Ensure uniqueness and non-empty
    uniq: List[str] = []
    for t in tags:
        if t and t not in uniq:
            uniq.append(t)
    return uniq[:limit]


# --- OpenAI call -----------------------------------------------------------

def _build_prompt(topic: Optional[str], style: str) -> str:
    topic_txt = topic.strip() if topic else "something interesting about AI or software engineering"
    if style == "tweet":
        return (
            "Write one concise, engaging tweet in plain text about '" + topic_txt + "'. "
            "Do NOT include hashtags, @mentions, links, or emojis. Keep it under 280 characters. "
            "Return only the tweet text without any labels or backticks."
        )
    else:
        return (
            "Write a concise Twitter thread in plain text about '" + topic_txt + "'. "
            "Target 3-6 short tweets. Each tweet should be a separate paragraph. "
            "Do NOT include hashtags, @mentions, links, or emojis. Avoid numbering. "
            "Return only the text paragraphs with blank lines between tweets."
        )


def _call_openai(prompt: str, api_key: Optional[str], model: Optional[str] = None) -> str:
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY")
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "400"))

    # Prefer new SDK
    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that writes concise, engaging Twitter content. "
                        "Keep tweets < 280 chars; for threads, each paragraph is one tweet."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        # Fallback to legacy API
        try:
            import openai  # type: ignore

            openai.api_key = api_key
            resp = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an assistant that writes concise, engaging Twitter content. "
                            "Keep tweets < 280 chars; for threads, each paragraph is one tweet."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return (resp["choices"][0]["message"]["content"] or "").strip()
        except Exception as e2:
            raise RuntimeError(f"OpenAI call failed: {e2}")


# --- Public API ------------------------------------------------------------

def generate_content(topic: str | None = None, style: str = "thread") -> Dict[str, Any]:
    """Generate tweet or thread content via OpenAI and return a normalized JSON dict.

    Returns:
        {
          "type": "tweet" | "thread",
          "items": ["..."],
          "prompt_used": "...",
          "metadata": {"model": str, "style": str, "topic": str|None, "hashtags": [str,...], ...}
        }
    """
    style_norm = (style or "thread").strip().lower()
    if style_norm not in {"tweet", "thread"}:
        style_norm = "thread"

    cfg = Config.load()
    prompt = _build_prompt(topic, style_norm)
    model_used = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    draft_text: str
    used_openai = True
    error_msg: Optional[str] = None
    try:
        draft_text = _call_openai(prompt, cfg.openai_api_key, model=model_used)
    except Exception as e:
        # Graceful fallback if OpenAI fails or key missing
        used_openai = False
        error_msg = str(e)
        if style_norm == "tweet":
            base = "Quick take"
            draft_text = f"{base}: {topic}" if topic else (
                "Quick tech tip: Keep it simple, test often, and ship iteratively."
            )
        else:
            if topic:
                draft_text = (
                    f"A quick thread on {topic}.\n\n"
                    f"1) Why it matters: focus on outcomes.\n\n"
                    f"2) How to start: pick a small goal.\n\n"
                    f"3) Iterate: measure, learn, improve."
                )
            else:
                draft_text = (
                    "A quick thread on building better software.\n\n"
                    "1) Keep PRs small.\n\n"
                    "2) Write tests that matter.\n\n"
                    "3) Automate repeatable tasks."
                )

    # Post-process into items
    if style_norm == "tweet":
        items = [_truncate_tweet(draft_text)]
    else:
        # Split by paragraphs first, then enforce 280-char chunks
        paras = [p.strip() for p in re.split(r"\n{2,}|\r\n{2,}", draft_text) if p.strip()]
        if paras:
            parts: List[str] = []
            for p in paras:
                if len(p) <= MAX_TWEET_LEN:
                    parts.append(p)
                else:
                    parts.extend(_chunk_text(p))
            items = parts
        else:
            items = _chunk_text(draft_text)

    hashtags = _suggest_hashtags(topic, "\n".join(items), limit=3)

    result: Dict[str, Any] = {
        "type": "tweet" if style_norm == "tweet" else "thread",
        "items": items,
        "prompt_used": prompt,
        "metadata": {
            "model": model_used,
            "style": style_norm,
            "topic": topic,
            "used_openai": used_openai,
            "hashtags": hashtags,
        },
    }
    if error_msg:
        result["metadata"]["error"] = error_msg

    return result


__all__ = ["generate_content"]
