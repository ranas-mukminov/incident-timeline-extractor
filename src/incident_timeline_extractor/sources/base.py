from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

from incident_timeline_extractor.timeline.model import Event


class LogSource(ABC):
    """Abstract log source."""

    name: str = "base"

    @abstractmethod
    def collect(self, *, since: datetime | None = None, until: datetime | None = None) -> Iterable[Event]:
        """Collect events in the given time window."""

    def __iter__(self):  # pragma: no cover - helper
        return self.collect()
