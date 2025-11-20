from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Event:
    id: str
    timestamp: datetime
    source: str
    host: str | None = None
    service: str | None = None
    severity: str = "info"
    category: str | None = None
    message: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    correlation_id: str | None = None


@dataclass
class Timeline:
    incident_id: str
    started_at: datetime | None
    ended_at: datetime | None
    events: list[Event] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["Event", "Timeline"]
