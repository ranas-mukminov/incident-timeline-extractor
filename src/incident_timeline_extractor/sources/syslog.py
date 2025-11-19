from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from incident_timeline_extractor.parsing.syslog_parser import parse_syslog_line
from incident_timeline_extractor.sources.base import LogSource
from incident_timeline_extractor.timeline.model import Event


class SyslogSource(LogSource):
    name = "syslog"

    def __init__(self, *, files: list[Path] | None = None, host: str | None = None):
        self.files = files or []
        self.host = host

    def _read_lines(self) -> Iterable[str]:
        for path in self.files:
            if not path.exists():
                continue
            with path.open("r", encoding="utf-8") as f:
                yield from f

    def collect(self, *, since: datetime | None = None, until: datetime | None = None) -> Iterable[Event]:
        events: List[Event] = []
        idx = 0
        for line in self._read_lines():
            parsed = parse_syslog_line(line)
            if not parsed:
                continue
            event = Event(
                id=f"syslog-{idx:04d}",
                timestamp=parsed["timestamp"],
                source=self.name,
                host=parsed.get("metadata", {}).get("host") or self.host,
                service=parsed.get("metadata", {}).get("app"),
                severity=parsed.get("severity", "info"),
                category=parsed.get("category"),
                message=parsed.get("message", ""),
                raw=parsed.get("metadata", {}),
            )
            idx += 1
            if since and event.timestamp < since:
                continue
            if until and event.timestamp > until:
                continue
            events.append(event)
        return events


__all__ = ["SyslogSource"]
