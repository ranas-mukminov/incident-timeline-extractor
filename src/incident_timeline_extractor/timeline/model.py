from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class Event:
    id: str
    timestamp: datetime
    source: str
    host: Optional[str] = None
    service: Optional[str] = None
    severity: str = "info"
    category: Optional[str] = None
    message: str = ""
    raw: dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    correlation_id: Optional[str] = None


@dataclass
class Timeline:
    incident_id: str
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    events: List[Event] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


__all__ = ["Event", "Timeline"]
