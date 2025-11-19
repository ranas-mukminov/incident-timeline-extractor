from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from incident_timeline_extractor.parsing.nginx_parser import parse_access_line, parse_error_line
from incident_timeline_extractor.sources.base import LogSource
from incident_timeline_extractor.timeline.model import Event


class NginxSource(LogSource):
    name = "nginx"

    def __init__(
        self,
        *,
        access_log: Path | None = None,
        error_log: Path | None = None,
        host: str | None = None,
        service: str | None = None,
    ) -> None:
        self.access_log = access_log
        self.error_log = error_log
        self.host = host
        self.service = service or "frontend"

    def _wrap_event(self, parsed: dict, idx: int, kind: str) -> Event:
        return Event(
            id=f"nginx-{kind}-{idx:04d}",
            timestamp=parsed["timestamp"],
            source=self.name,
            host=self.host,
            service=self.service,
            severity=parsed.get("severity", "info"),
            category=parsed.get("category"),
            message=parsed.get("message", ""),
            raw=parsed.get("metadata", {}),
            tags=[],
        )

    def _read_lines(self, path: Path | None) -> Iterable[str]:
        if path and path.exists():
            with path.open("r", encoding="utf-8") as f:
                yield from f

    def collect(self, *, since: datetime | None = None, until: datetime | None = None) -> Iterable[Event]:
        events: List[Event] = []
        idx = 0
        for line in self._read_lines(self.access_log):
            parsed = parse_access_line(line)
            if not parsed:
                continue
            event = self._wrap_event(parsed, idx, "access")
            idx += 1
            if since and event.timestamp < since:
                continue
            if until and event.timestamp > until:
                continue
            events.append(event)

        for line in self._read_lines(self.error_log):
            parsed = parse_error_line(line)
            if not parsed:
                continue
            event = self._wrap_event(parsed, idx, "error")
            idx += 1
            if since and event.timestamp < since:
                continue
            if until and event.timestamp > until:
                continue
            events.append(event)

        return events


__all__ = ["NginxSource"]
