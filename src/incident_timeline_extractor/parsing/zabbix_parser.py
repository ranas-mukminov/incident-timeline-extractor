from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timezone
from typing import Any

SEVERITY_MAP = {
    0: "info",
    1: "info",
    2: "warning",
    3: "error",
    4: "critical",
    5: "critical",
}


def parse_zabbix_events(payload: Any) -> list[dict[str, Any]]:
    """Parse Zabbix event JSON payload into normalized dicts."""

    if payload is None:
        return []
    events: Iterable[Any]
    if isinstance(payload, dict):
        events = payload.get("events") or payload.get("alert") or payload.get("result") or []
    elif isinstance(payload, list):
        events = payload
    else:
        return []

    normalized: list[dict[str, Any]] = []
    for idx, event in enumerate(events):
        clock = event.get("clock") or event.get("timestamp") or event.get("event_time")
        try:
            ts = datetime.fromtimestamp(int(clock), tz=timezone.utc)
        except Exception:
            continue
        severity = SEVERITY_MAP.get(int(event.get("severity", 1)), "info")
        name = event.get("name") or event.get("event") or "Zabbix event"
        host = None
        if isinstance(event.get("hosts"), list) and event["hosts"]:
            host = event["hosts"][0].get("host")
        host = host or event.get("host")

        metadata = {
            "triggerid": event.get("triggerid"),
            "eventid": event.get("eventid") or event.get("id") or str(idx),
            "status": event.get("status") or event.get("value") or event.get("state"),
            "host": host,
        }

        normalized.append(
            {
                "timestamp": ts,
                "severity": severity,
                "category": "alert",
                "message": name,
                "metadata": metadata,
            }
        )
    return normalized


__all__ = ["parse_zabbix_events"]
