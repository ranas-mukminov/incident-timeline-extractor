from __future__ import annotations

from ai_providers.base import AIProvider
from incident_timeline_extractor.timeline.model import Event

KEYWORD_TAGS = {
    "timeout": "network_timeout",
    "latency": "latency",
    "error": "error",
    "5xx": "http_5xx_spike",
    "database": "db_issue",
    "db": "db_issue",
}


def _heuristic_tags(event: Event) -> list[str]:
    tags: list[str] = []
    msg_lower = event.message.lower()
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in msg_lower:
            tags.append(tag)
    if event.severity in {"error", "critical"}:
        tags.append("suspect")
    return tags


def tag_events(events: list[Event], provider: AIProvider | None) -> list[Event]:
    provider_tags: list[list[str]] = []
    if provider:
        try:
            provider_tags = provider.tag_events(events)
        except Exception:
            provider_tags = []

    for idx, event in enumerate(events):
        existing = list(event.tags)
        if provider_tags:
            existing.extend(provider_tags[idx] if idx < len(provider_tags) else [])
        existing.extend(_heuristic_tags(event))
        # deduplicate while preserving order
        seen = set()
        deduped: list[str] = []
        for tag in existing:
            if tag in seen:
                continue
            seen.add(tag)
            deduped.append(tag)
        event.tags = deduped
    return events


__all__ = ["tag_events"]
