from __future__ import annotations

import calendar
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

SYSLOG_REGEX = re.compile(
    r"(?P<month>[A-Za-z]{3})\s+(?P<day>\d{1,2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<host>[\w.-]+) (?P<app>[^:]+): (?P<message>.*)"
)

KEYWORD_SEVERITY = {
    "error": "error",
    "err": "error",
    "warn": "warning",
    "fail": "error",
    "crit": "critical",
    "notice": "info",
}


def _month_to_number(month: str) -> int:
    return list(calendar.month_abbr).index(month)


def parse_syslog_line(line: str, now: datetime | None = None) -> Optional[Dict[str, Any]]:
    match = SYSLOG_REGEX.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    current = now or datetime.now(timezone.utc)
    month = _month_to_number(data["month"])
    ts_str = f"{current.year}-{month:02d}-{int(data['day']):02d} {data['time']}"
    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)

    message = data.get("message", "")
    severity = "info"
    lowered = message.lower()
    for key, sev in KEYWORD_SEVERITY.items():
        if key in lowered:
            severity = sev
            break

    metadata: Dict[str, Any] = {
        "host": data.get("host"),
        "app": data.get("app"),
    }

    return {
        "timestamp": ts,
        "severity": severity,
        "category": "infra",
        "message": message,
        "metadata": metadata,
    }


__all__ = ["parse_syslog_line"]
