"""Command line entry point for manual research pulls."""

from __future__ import annotations

import argparse
import json
import sys

from cultural_memory_reddit.client import (
    RedditConfig,
    RedditConnector,
    RedditConnectorError,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read public Reddit post metadata for aggregate culture research."
    )
    parser.add_argument(
        "--subreddit",
        action="append",
        required=True,
        help="Subreddit name. May be passed multiple times.",
    )
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument(
        "--time-filter",
        default="all",
        choices=("hour", "day", "week", "month", "year", "all"),
    )
    args = parser.parse_args(argv)

    try:
        connector = RedditConnector(RedditConfig.from_env())
        posts = connector.top_posts(
            args.subreddit,
            limit=args.limit,
            time_filter=args.time_filter,
        )
    except RedditConnectorError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for post in posts:
        print(json.dumps(post.as_dict(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

