"""Sanitize Reddit listing records for aggregate research storage."""

from __future__ import annotations

import urllib.parse
from typing import Any

from cultural_memory_reddit.time import iso_from_epoch

ALLOWED_MEDIA_HOSTS = (
    "youtube.com",
    "youtu.be",
    "m.youtube.com",
    "streamable.com",
    "v.redd.it",
)


def sanitize_listing_child(child: dict[str, Any]) -> dict[str, Any] | None:
    """Return a limited research record or None when the post is out of scope."""

    data = child.get("data") or {}
    if not isinstance(data, dict) or not _is_media_signal(data):
        return None

    post_id = str(data.get("id") or "").strip()
    subreddit = str(data.get("subreddit") or "").strip()
    title = str(data.get("title") or "").strip()
    permalink = _absolute_permalink(str(data.get("permalink") or ""))
    url = str(data.get("url") or "").strip()
    if not post_id or not subreddit or not permalink or not url:
        return None

    return {
        "source": "reddit",
        "post_id": post_id,
        "subreddit": subreddit,
        "title": title,
        "permalink": permalink,
        "url": url,
        "created_utc": iso_from_epoch(data.get("created_utc")),
        "score": _to_int(data.get("score")),
        "over_18": bool(data.get("over_18")),
        "signal_context": "public_culture_research",
    }


def _is_media_signal(data: dict[str, Any]) -> bool:
    if data.get("is_self") or data.get("is_gallery"):
        return False
    if data.get("removed_by_category") or data.get("banned_by"):
        return False
    post_hint = data.get("post_hint")
    if post_hint in {"self", "image", "gallery"}:
        return False
    url = data.get("url")
    return isinstance(url, str) and _host_allowed(url)


def _host_allowed(url: str) -> bool:
    try:
        host = (urllib.parse.urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    if host.startswith("www."):
        host = host[4:]
    return any(host == allowed or host.endswith("." + allowed) for allowed in ALLOWED_MEDIA_HOSTS)


def _absolute_permalink(permalink: str) -> str:
    if permalink.startswith("https://www.reddit.com/"):
        return permalink
    if permalink.startswith("/"):
        return f"https://www.reddit.com{permalink}"
    return ""


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0

