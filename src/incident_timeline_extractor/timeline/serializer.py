from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from incident_timeline_extractor.timeline.model import Event, Timeline

VERSION = "1.0"


def _dt_to_str(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.astimezone().isoformat()


def to_json(timeline: Timeline) -> str:
    payload: dict[str, Any] = {
        "version": VERSION,
        "incident_id": timeline.incident_id,
        "started_at": _dt_to_str(timeline.started_at),
        "ended_at": _dt_to_str(timeline.ended_at),
        "events": [
            {
                "id": e.id,
                "timestamp": _dt_to_str(e.timestamp),
                "source": e.source,
                "host": e.host,
                "service": e.service,
                "severity": e.severity,
                "category": e.category,
                "message": e.message,
                "tags": e.tags,
                "correlation_id": e.correlation_id,
                "raw": e.raw,
            }
            for e in timeline.events
        ],
        "metadata": timeline.metadata,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def from_json(data: str | dict[str, Any]) -> Timeline:
    if isinstance(data, str):
        payload = json.loads(data)
    else:
        payload = data
    events = []
    for raw_event in payload.get("events", []):
        events.append(
            Event(
                id=raw_event["id"],
                timestamp=_parse_dt(raw_event.get("timestamp")) or datetime.now(timezone.utc),
                source=raw_event.get("source", "unknown"),
                host=raw_event.get("host"),
                service=raw_event.get("service"),
                severity=raw_event.get("severity", "info"),
                category=raw_event.get("category"),
                message=raw_event.get("message", ""),
                raw=raw_event.get("raw", {}),
                tags=list(raw_event.get("tags", [])),
                correlation_id=raw_event.get("correlation_id"),
            )
        )

    return Timeline(
        incident_id=payload.get("incident_id", "unknown"),
        started_at=_parse_dt(payload.get("started_at")),
        ended_at=_parse_dt(payload.get("ended_at")),
        events=events,
        metadata=payload.get("metadata", {}),
    )


def timeline_to_markdown(timeline: Timeline) -> str:
    lines = ["## Incident Timeline", ""]
    for event in timeline.events:
        ts = event.timestamp.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
        source = f"{event.source}/{event.host}" if event.host else event.source
        msg = event.message.replace("\n", " ")
        lines.append(f"- **{ts}** [{source}][{event.severity}] {msg}")
    return "\n".join(lines)


def timeline_to_ascii(timeline: Timeline) -> str:
    header = f"{'Time':25} | {'Source':15} | {'Severity':8} | Message"
    sep = "-" * len(header)
    rows = [header, sep]
    for event in timeline.events:
        ts = event.timestamp.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        source = f"{event.source}/{event.host}" if event.host else event.source
        rows.append(f"{ts:25} | {source:15} | {event.severity:8} | {event.message}")
    return "\n".join(rows)


__all__ = ["to_json", "from_json", "VERSION", "timeline_to_markdown", "timeline_to_ascii"]
