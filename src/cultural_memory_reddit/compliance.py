"""Compliance-oriented helpers for downstream research storage."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetentionPolicy:
    """Default retention policy for Reddit-derived research records."""

    delete_unavailable_content_within_hours: int = 48
    store_author_fields: bool = False
    collect_full_comment_threads: bool = False
    train_general_purpose_ai_models: bool = False
    resell_reddit_data: bool = False
    build_user_level_marketing_audiences: bool = False


def tombstone_record(post_id: str, reason: str) -> dict[str, str]:
    """Return a minimal audit record after deleting stored Reddit content."""

    return {
        "source": "reddit",
        "post_id": post_id,
        "status": "deleted_from_research_store",
        "reason": reason,
    }
