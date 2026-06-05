"""Time formatting helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any


def iso_from_epoch(value: Any) -> str:
    try:
        timestamp = float(value)
    except (TypeError, ValueError):
        timestamp = 0.0
    return datetime.fromtimestamp(timestamp, UTC).replace(microsecond=0).isoformat()

