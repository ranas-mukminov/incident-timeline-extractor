from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from incident_timeline_extractor.parsing.prometheus_parser import parse_alertmanager
from incident_timeline_extractor.sources.base import LogSource
from incident_timeline_extractor.timeline.model import Event


class PrometheusSource(LogSource):
    name = "prometheus"

    def __init__(self, *, file: Path | None = None, url: str | None = None):
        self.file = file
        self.url = url

    def _load_payload(self):
        if self.file and self.file.exists():
            with self.file.open("r", encoding="utf-8") as f:
                return json.load(f)
        if self.url:
            with urllib.request.urlopen(self.url) as resp:  # nosec B310
                return json.load(resp)
        return None

    def collect(self, *, since: datetime | None = None, until: datetime | None = None) -> Iterable[Event]:
        payload = self._load_payload()
        events: List[Event] = []
        for idx, parsed in enumerate(parse_alertmanager(payload)):
            event = Event(
                id=f"prometheus-{idx:04d}",
                timestamp=parsed["timestamp"],
                source=self.name,
                host=parsed.get("metadata", {}).get("labels", {}).get("instance"),
                service=parsed.get("metadata", {}).get("labels", {}).get("job"),
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


__all__ = ["PrometheusSource"]
