from __future__ import annotations

import subprocess
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from incident_timeline_extractor.parsing.journald_parser import parse_journald_line
from incident_timeline_extractor.sources.base import LogSource
from incident_timeline_extractor.timeline.model import Event


class JournaldSource(LogSource):
    name = "journald"

    def __init__(self, *, units: list[str] | None = None, file: Path | None = None):
        self.units = units or []
        self.file = file

    def _read_lines(self, since: datetime | None, until: datetime | None) -> Iterable[str]:
        if self.file and self.file.exists():
            with self.file.open("r", encoding="utf-8") as f:
                yield from f
            return

        cmd = ["journalctl", "--output", "short-iso"]
        if since:
            cmd.extend(["--since", since.isoformat()])
        if until:
            cmd.extend(["--until", until.isoformat()])
        for unit in self.units:
            cmd.extend(["-u", unit])
        try:
            proc = subprocess.run(cmd, capture_output=True, check=True, text=True)
            yield from proc.stdout.splitlines()
        except Exception:
            return

    def collect(
        self, *, since: datetime | None = None, until: datetime | None = None
    ) -> Iterable[Event]:
        events: list[Event] = []
        idx = 0
        for line in self._read_lines(since, until):
            parsed = parse_journald_line(line)
            if not parsed:
                continue
            event = Event(
                id=f"journald-{idx:04d}",
                timestamp=parsed["timestamp"],
                source=self.name,
                host=None,
                service=parsed.get("metadata", {}).get("unit"),
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


__all__ = ["JournaldSource"]
