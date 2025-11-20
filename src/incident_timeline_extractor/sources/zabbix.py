from __future__ import annotations

import json
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from incident_timeline_extractor.parsing.zabbix_parser import parse_zabbix_events
from incident_timeline_extractor.sources.base import LogSource
from incident_timeline_extractor.timeline.model import Event


class ZabbixSource(LogSource):
    name = "zabbix"

    def __init__(self, *, file: Path | None = None, mode: str = "file"):
        self.file = file
        self.mode = mode

    def _load_payload(self):
        if self.mode == "file" and self.file and self.file.exists():
            with self.file.open("r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def collect(
        self, *, since: datetime | None = None, until: datetime | None = None
    ) -> Iterable[Event]:
        events: list[Event] = []
        payload = self._load_payload()
        parsed_events = parse_zabbix_events(payload)
        for idx, parsed in enumerate(parsed_events):
            event = Event(
                id=f"zabbix-{idx:04d}",
                timestamp=parsed["timestamp"],
                source=self.name,
                host=parsed.get("metadata", {}).get("host"),
                service=None,
                severity=parsed.get("severity", "warning"),
                category=parsed.get("category"),
                message=parsed.get("message", ""),
                raw=parsed.get("metadata", {}),
            )
            if since and event.timestamp < since:
                continue
            if until and event.timestamp > until:
                continue
            events.append(event)
        return events


__all__ = ["ZabbixSource"]
