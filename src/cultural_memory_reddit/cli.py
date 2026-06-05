"""Command line entry point for manual research pulls."""

from __future__ import annotations

import argparse
import json
import sys

from cultural_memory_reddit.client import (
    MAX_LISTING_LIMIT,
    RedditConfig,
    RedditConnector,
    RedditConnectorError,
    SUPPORTED_TIME_FILTERS,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="cultural-memory-reddit",
        description="Read public Reddit post metadata for aggregate culture research."
    )
    parser.add_argument(
        "--subreddit",
        action="append",
        required=True,
        help="Subreddit name. May be passed multiple times.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help=f"Posts to request per subreddit, 1-{MAX_LISTING_LIMIT}.",
    )
    parser.add_argument(
        "--time-filter",
        default="all",
        choices=SUPPORTED_TIME_FILTERS,
    )
    parser.add_argument(
        "--include-rate-limit",
        action="store_true",
        help="Print Reddit rate-limit headers to stderr after the JSONL output.",
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
    if args.include_rate_limit and connector.last_rate_limit is not None:
        snapshot = connector.last_rate_limit
        print(
            "rate_limit: "
            f"used={_format_optional(snapshot.used)} "
            f"remaining={_format_optional(snapshot.remaining)} "
            f"reset_after_sec={_format_optional(snapshot.reset_after_sec)}",
            file=sys.stderr,
        )
    return 0


def _format_optional(value: float | None) -> str:
    return "unknown" if value is None else f"{value:g}"


if __name__ == "__main__":
    raise SystemExit(main())
