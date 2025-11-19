from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from incident_timeline_extractor.timeline.model import Event


class AIProvider(ABC):
    name: str = "base"

    @abstractmethod
    def tag_events(self, events: List[Event]) -> List[List[str]]:
        """Return list of tag lists corresponding to events."""

    def cluster_events(self, events: List[Event]) -> List[Dict[str, Any]]:  # pragma: no cover - optional
        return []

    def generate_postmortem(self, prompt: str, language: str = "en") -> Dict[str, Any]:  # pragma: no cover - optional
        raise NotImplementedError
