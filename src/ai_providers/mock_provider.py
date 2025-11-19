from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from .base import AIProvider
from incident_timeline_extractor.timeline.model import Event


class MockProvider(AIProvider):
    name = "mock"

    def tag_events(self, events: List[Event]) -> List[List[str]]:
        tagged: List[List[str]] = []
        for event in events:
            event_tags: List[str] = []
            if event.severity in {"error", "critical"}:
                event_tags.append("suspect")
            if isinstance(event.raw, dict) and event.raw.get("status") and int(event.raw.get("status")) >= 500:
                event_tags.append("http_5xx")
            if event.category == "alert":
                event_tags.append("alert")
            if not event_tags:
                event_tags.append("reviewed")
            tagged.append(event_tags)
        return tagged

    def cluster_events(self, events: List[Event]) -> List[Dict[str, Any]]:
        clusters: Dict[str, Dict[str, Any]] = {}
        for event in events:
            key = event.service or event.source
            if key not in clusters:
                clusters[key] = {"id": key, "name": key, "description": f"Cluster for {key}", "event_ids": []}
            clusters[key]["event_ids"].append(event.id)
        return list(clusters.values())

    def generate_postmortem(self, prompt: str, language: str = "en") -> Dict[str, Any]:
        return {
            "title": "Mock Postmortem",
            "summary": f"Auto-generated summary ({language}).",
            "impact": "Impact assessed via mock provider.",
            "root_cause": "Mock root cause based on timeline patterns.",
            "contributing_factors": "Limited mock context.",
            "what_went_well": "Early detection.",
            "what_can_be_improved": "Automate more checks.",
            "lessons_learned": "Consistency matters.",
            "action_items": [
                {"description": "Add monitoring", "owner": "sre", "due_date": date.today().isoformat(), "status": "open"}
            ],
        }
