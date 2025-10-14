from __future__ import annotations


def truncate(text: str, max_len: int = 280) -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - 1] + "\u2026"  # ellipsis
