from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

JOURNALD_REGEX = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})) (?P<unit>[\w\-.@]+)\[(?P<pid>\d+)\]: (?P<message>.*)"
)

LEVEL_KEYWORDS = {
    "error": "error",
    "err": "error",
    "warn": "warning",
    "crit": "critical",
    "alert": "critical",
}


def parse_journald_line(line: str) -> Optional[Dict[str, Any]]:
    match = JOURNALD_REGEX.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    message = data.get("message", "")
    severity = "info"
    lowered = message.lower()
    for key, sev in LEVEL_KEYWORDS.items():
        if key in lowered:
            severity = sev
            break

    metadata: Dict[str, Any] = {
        "unit": data.get("unit"),
        "pid": data.get("pid"),
    }

    return {
        "timestamp": ts.astimezone(timezone.utc),
        "severity": severity,
        "category": "app",
        "message": message,
        "metadata": metadata,
    }


__all__ = ["parse_journald_line"]
