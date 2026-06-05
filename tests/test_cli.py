from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from cultural_memory_reddit.cli import main
from cultural_memory_reddit.client import RateLimitSnapshot, RedditConfig, RedditPost


class FakeConnector:
    last_rate_limit = RateLimitSnapshot(used=1, remaining=99, reset_after_sec=600)

    def __init__(self, config: RedditConfig) -> None:
        self.config = config

    def top_posts(
        self,
        subreddits: list[str],
        *,
        limit: int,
        time_filter: str,
    ) -> list[RedditPost]:
        return [
            RedditPost(
                source="reddit",
                post_id="abc123",
                subreddit=subreddits[0],
                title=f"{time_filter}:{limit}",
                permalink="https://www.reddit.com/r/youtubehaiku/comments/abc123/example/",
                url="https://youtu.be/example",
                created_utc="2026-06-05T14:00:00+00:00",
                score=120,
                over_18=False,
            )
        ]


class TestCli(unittest.TestCase):
    def test_outputs_jsonl_and_optional_rate_limit_summary(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        config = RedditConfig("cid", "secret", "python:test:v1 (by /u/example)")

        with (
            patch("cultural_memory_reddit.cli.RedditConfig.from_env", return_value=config),
            patch("cultural_memory_reddit.cli.RedditConnector", FakeConnector),
            redirect_stdout(stdout),
            redirect_stderr(stderr),
        ):
            code = main(
                [
                    "--subreddit",
                    "youtubehaiku",
                    "--limit",
                    "10",
                    "--time-filter",
                    "year",
                    "--include-rate-limit",
                ]
            )

        self.assertEqual(code, 0)
        record = json.loads(stdout.getvalue())
        self.assertEqual(record["post_id"], "abc123")
        self.assertEqual(record["title"], "year:10")
        self.assertIn("rate_limit: used=1 remaining=99 reset_after_sec=600", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
