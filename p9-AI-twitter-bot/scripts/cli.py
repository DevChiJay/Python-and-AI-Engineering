from __future__ import annotations

import argparse

from app.services.content_generator import generate_tweet
from app.utils.text_utils import truncate


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Twitter Bot CLI")
    parser.add_argument("topic", nargs="?", help="Optional topic for tweet")
    args = parser.parse_args()

    text = generate_tweet(args.topic)
    print(truncate(text))


if __name__ == "__main__":
    main()
