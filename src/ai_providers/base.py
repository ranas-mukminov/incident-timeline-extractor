from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from incident_timeline_extractor.timeline.model import Event


class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    def tag_events(self, events: list[Event]) -> list[list[str]]:
        """Return list of tag lists corresponding to events."""

    def cluster_events(
        self, events: list[Event]
    ) -> list[dict[str, Any]]:  # pragma: no cover - optional
        return []

    def generate_postmortem(
        self, prompt: str, language: str = "en"
    ) -> dict[str, Any]:  # pragma: no cover - optional
        raise NotImplementedError
