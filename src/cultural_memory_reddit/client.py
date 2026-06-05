"""OAuth-only Reddit Data API client.

The connector deliberately exposes only read-only listing access needed for
aggregate cultural-memory research. It does not implement write endpoints.
"""

from __future__ import annotations

import base64
import json
import os
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from cultural_memory_reddit.records import sanitize_listing_child

OAUTH_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
OAUTH_BASE_URL = "https://oauth.reddit.com"
DEFAULT_TIMEOUT = 30

HttpGet = Callable[[str, dict[str, str]], tuple[bytes, dict[str, str]]]
HttpPost = Callable[[str, bytes, dict[str, str]], tuple[bytes, dict[str, str]]]


class RedditConnectorError(RuntimeError):
    """Raised when the connector cannot safely access the Reddit Data API."""


@dataclass(frozen=True)
class RateLimitSnapshot:
    used: float | None = None
    remaining: float | None = None
    reset_after_sec: float | None = None

    @classmethod
    def from_headers(cls, headers: dict[str, str]) -> "RateLimitSnapshot":
        lowered = {k.lower(): v for k, v in headers.items()}
        return cls(
            used=_to_float(lowered.get("x-ratelimit-used")),
            remaining=_to_float(lowered.get("x-ratelimit-remaining")),
            reset_after_sec=_to_float(lowered.get("x-ratelimit-reset")),
        )


@dataclass(frozen=True)
class RedditConfig:
    client_id: str
    client_secret: str
    user_agent: str

    @classmethod
    def from_env(cls) -> "RedditConfig":
        client_id = os.environ.get("REDDIT_CLIENT_ID", "").strip()
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "").strip()
        user_agent = os.environ.get("REDDIT_USER_AGENT", "").strip()
        if not client_id or not client_secret or not user_agent:
            raise RedditConnectorError(
                "REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and "
                "REDDIT_USER_AGENT are required"
            )
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )


@dataclass(frozen=True)
class RedditPost:
    source: str
    post_id: str
    subreddit: str
    title: str
    permalink: str
    url: str
    created_utc: str
    score: int
    over_18: bool
    signal_context: str = "public_culture_research"

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "post_id": self.post_id,
            "subreddit": self.subreddit,
            "title": self.title,
            "permalink": self.permalink,
            "url": self.url,
            "created_utc": self.created_utc,
            "score": self.score,
            "over_18": self.over_18,
            "signal_context": self.signal_context,
        }


class RedditConnector:
    """Small read-only connector for public subreddit listing research."""

    def __init__(
        self,
        config: RedditConfig,
        *,
        http_get: HttpGet | None = None,
        http_post: HttpPost | None = None,
    ) -> None:
        self.config = config
        self._http_get = http_get or _default_http_get
        self._http_post = http_post or _default_http_post
        self._access_token: str | None = None
        self.last_rate_limit: RateLimitSnapshot | None = None

    def top_posts(
        self,
        subreddits: Iterable[str],
        *,
        limit: int = 25,
        time_filter: str = "all",
    ) -> list[RedditPost]:
        """Return sanitized public post metadata sorted by score descending."""

        token = self._token()
        headers = {
            "Authorization": f"bearer {token}",
            "User-Agent": self.config.user_agent,
        }
        posts: list[RedditPost] = []
        for subreddit in subreddits:
            clean = _clean_subreddit(subreddit)
            if not clean:
                continue
            url = (
                f"{OAUTH_BASE_URL}/r/{urllib.parse.quote(clean)}/top.json"
                f"?t={urllib.parse.quote(time_filter)}&limit={int(limit)}"
            )
            raw, response_headers = self._http_get(url, headers)
            self.last_rate_limit = RateLimitSnapshot.from_headers(response_headers)
            payload = _decode_json(raw)
            children = ((payload.get("data") or {}).get("children")) or []
            for child in children:
                post = sanitize_listing_child(child)
                if post is not None:
                    posts.append(
                        RedditPost(
                            source="reddit",
                            post_id=post["post_id"],
                            subreddit=post["subreddit"],
                            title=post["title"],
                            permalink=post["permalink"],
                            url=post["url"],
                            created_utc=post["created_utc"],
                            score=post["score"],
                            over_18=post["over_18"],
                        )
                    )
        by_id: dict[str, RedditPost] = {}
        for post in posts:
            existing = by_id.get(post.post_id)
            if existing is None or post.score > existing.score:
                by_id[post.post_id] = post
        return sorted(by_id.values(), key=lambda p: p.score, reverse=True)

    def _token(self) -> str:
        if self._access_token:
            return self._access_token
        credentials = f"{self.config.client_id}:{self.config.client_secret}"
        encoded = base64.b64encode(credentials.encode("utf-8")).decode("ascii")
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode(
            "utf-8"
        )
        headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": self.config.user_agent,
        }
        raw, _headers = self._http_post(OAUTH_TOKEN_URL, body, headers)
        payload = _decode_json(raw)
        token = payload.get("access_token")
        if not isinstance(token, str) or not token:
            raise RedditConnectorError("OAuth response did not contain access_token")
        self._access_token = token
        return token


def _default_http_get(url: str, headers: dict[str, str]) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
        return response.read(), dict(response.headers.items())


def _default_http_post(
    url: str, body: bytes, headers: dict[str, str]
) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT) as response:
        return response.read(), dict(response.headers.items())


def _decode_json(raw: bytes | str) -> dict[str, Any]:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RedditConnectorError(f"Reddit API returned invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RedditConnectorError("Reddit API returned a non-object JSON payload")
    return payload


def _clean_subreddit(value: str) -> str:
    return value.strip().lstrip("/").removeprefix("r/")


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


