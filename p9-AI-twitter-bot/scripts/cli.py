from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from app.models import get_generated, mark_generated_post_result, save_generated
from app.services.content_generator import generate_content
from app.services.poster import TwitterClient


def _cmd_generate(args: argparse.Namespace) -> None:
    result = generate_content(topic=args.topic, style=args.style)
    gen_id = save_generated(topic=result.get("metadata", {}).get("topic"), style=result.get("type", "thread"), prompt_used=result.get("prompt_used"), content=result)
    print(json.dumps({"id": gen_id, "content": result}, ensure_ascii=False, indent=2))


def _cmd_post(args: argparse.Namespace) -> None:
    rec = get_generated(int(args.id))
    if not rec:
        raise SystemExit(f"No generated record with id={args.id}")
    content: Dict[str, Any] = json.loads(rec.content_json)
    client = TwitterClient()
    if content.get("type") == "tweet":
        res = client.post_tweet((content.get("items") or [""])[0])
    else:
        res = client.post_thread(content.get("items") or [])
    mark_generated_post_result(int(args.id), res)
    print(json.dumps(res, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Twitter Bot CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("generate", help="Generate content")
    p_gen.add_argument("--topic", type=str, default=None)
    p_gen.add_argument("--style", type=str, default="thread", choices=["tweet", "thread"])
    p_gen.set_defaults(func=_cmd_generate)

    p_post = sub.add_parser("post", help="Post by generated id")
    p_post.add_argument("--id", type=int, required=True)
    p_post.set_defaults(func=_cmd_post)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
