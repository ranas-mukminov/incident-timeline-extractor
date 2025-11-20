from __future__ import annotations

from dataclasses import dataclass

from ai_providers.base import AIProvider
from incident_timeline_extractor.timeline.model import Event


@dataclass
class EventCluster:
    id: str
    name: str
    description: str
    event_ids: list[str]


def _fallback_clusters(events: list[Event]) -> list[EventCluster]:
    clusters: dict[str, EventCluster] = {}
    for event in events:
        key = event.service or event.source
        if key not in clusters:
            clusters[key] = EventCluster(
                id=key,
                name=key,
                description=f"Cluster based on {key}",
                event_ids=[],
            )
        clusters[key].event_ids.append(event.id)
    return list(clusters.values())


def cluster_events(events: list[Event], provider: AIProvider | None) -> list[EventCluster]:
    if provider:
        try:
            raw = provider.cluster_events(events)
            if raw:
                return [
                    EventCluster(
                        id=str(item.get("id") or item.get("name") or "cluster"),
                        name=item.get("name", "cluster"),
                        description=item.get("description", ""),
                        event_ids=item.get("event_ids", []),
                    )
                    for item in raw
                ]
        except Exception:
            pass
    return _fallback_clusters(events)


__all__ = ["EventCluster", "cluster_events"]
