from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from incident_timeline_extractor.timeline.model import Event, Timeline


def build_timeline(incident_id: str, events: Iterable[Event]) -> Timeline:
    """Merge events from multiple sources into a sorted timeline."""

    events_list: list[Event] = list(events)
    events_list.sort(key=lambda e: (e.timestamp, e.source, e.id))

    started_at = events_list[0].timestamp if events_list else None
    ended_at = events_list[-1].timestamp if events_list else None

    return Timeline(
        incident_id=incident_id,
        started_at=started_at,
        ended_at=ended_at,
        events=events_list,
        metadata={},
    )


def filter_by_window(
    events: Iterable[Event], since: datetime | None, until: datetime | None
) -> list[Event]:
    result: list[Event] = []
    for event in events:
        if since and event.timestamp < since:
            continue
        if until and event.timestamp > until:
            continue
        result.append(event)
    return result


__all__ = ["build_timeline", "filter_by_window"]
