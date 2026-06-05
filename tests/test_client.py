from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from cultural_memory_reddit.client import (
    OAUTH_TOKEN_URL,
    RedditConfig,
    RedditConnector,
    RedditConnectorError,
)


class TestRedditConfig(unittest.TestCase):
    def test_requires_oauth_and_user_agent(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RedditConnectorError):
                RedditConfig.from_env()

    def test_loads_from_environment(self) -> None:
        env = {
            "REDDIT_CLIENT_ID": "cid",
            "REDDIT_CLIENT_SECRET": "secret",
            "REDDIT_USER_AGENT": "python:test:v1 (by /u/example)",
        }
        with patch.dict(os.environ, env, clear=True):
            config = RedditConfig.from_env()
        self.assertEqual(config.client_id, "cid")
        self.assertEqual(config.client_secret, "secret")
        self.assertEqual(config.user_agent, env["REDDIT_USER_AGENT"])


class TestRedditConnector(unittest.TestCase):
    def test_uses_oauth_and_returns_sanitized_posts(self) -> None:
        calls: list[tuple[str, dict[str, str]]] = []

        def fake_post(url: str, body: bytes, headers: dict[str, str]):
            self.assertEqual(url, OAUTH_TOKEN_URL)
            self.assertIn("Authorization", headers)
            self.assertEqual(headers["User-Agent"], "python:test:v1 (by /u/example)")
            self.assertEqual(body.decode("utf-8"), "grant_type=client_credentials")
            return json.dumps({"access_token": "token"}).encode(), {}

        def fake_get(url: str, headers: dict[str, str]):
            calls.append((url, headers))
            payload = {
                "data": {
                    "children": [
                        {
                            "data": {
                                "id": "a",
                                "subreddit": "youtubehaiku",
                                "title": "kept",
                                "permalink": "/r/youtubehaiku/comments/a/kept/",
                                "url": "https://www.youtube.com/watch?v=a",
                                "created_utc": 1780668000,
                                "score": 5,
                                "over_18": False,
                                "is_self": False,
                                "is_gallery": False,
                                "post_hint": "rich:video",
                                "author": "not stored",
                            }
                        },
                        {
                            "data": {
                                "id": "b",
                                "subreddit": "youtubehaiku",
                                "title": "dropped image",
                                "permalink": "/r/youtubehaiku/comments/b/dropped/",
                                "url": "https://i.imgur.com/b.jpg",
                                "created_utc": 1780668000,
                                "score": 500,
                                "post_hint": "image",
                            }
                        },
                    ]
                }
            }
            headers_out = {
                "x-ratelimit-used": "1",
                "x-ratelimit-remaining": "99",
                "x-ratelimit-reset": "600",
            }
            return json.dumps(payload).encode(), headers_out

        connector = RedditConnector(
            RedditConfig(
                client_id="cid",
                client_secret="secret",
                user_agent="python:test:v1 (by /u/example)",
            ),
            http_get=fake_get,
            http_post=fake_post,
        )
        posts = connector.top_posts(["r/youtubehaiku"], limit=10)

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].post_id, "a")
        self.assertNotIn("author", posts[0].as_dict())
        self.assertEqual(calls[0][1]["Authorization"], "bearer token")
        self.assertTrue(calls[0][0].startswith("https://oauth.reddit.com/r/youtubehaiku/top.json"))
        self.assertIsNotNone(connector.last_rate_limit)
        assert connector.last_rate_limit is not None
        self.assertEqual(connector.last_rate_limit.remaining, 99)

    def test_rejects_bad_oauth_response(self) -> None:
        def fake_post(url: str, body: bytes, headers: dict[str, str]):
            return b"{}", {}

        connector = RedditConnector(
            RedditConfig("cid", "secret", "python:test:v1 (by /u/example)"),
            http_post=fake_post,
        )
        with self.assertRaises(RedditConnectorError):
            connector.top_posts(["x"])


if __name__ == "__main__":
    unittest.main()
