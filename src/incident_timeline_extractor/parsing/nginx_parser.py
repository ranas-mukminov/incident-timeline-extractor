from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional


ACCESS_REGEX = re.compile(
    r"(?P<remote>\S+) - (?P<user>\S+) \[(?P<time>[^\]]+)\] \"(?P<method>\S+) (?P<path>[^\s]+) (?P<proto>[^\"]+)\" (?P<status>\d{3}) (?P<size>\S+)(?: \"(?P<referrer>[^\"]*)\" \"(?P<ua>[^\"]*)\")?"
)

ERROR_REGEX = re.compile(
    r"(?P<date>\d{4}/\d{2}/\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) \[(?P<level>[a-z]+)\] (?P<pid>\d+)(?:#\d+)?: (?P<message>.*)"
)

LEVEL_MAP = {
    "debug": "debug",
    "info": "info",
    "notice": "info",
    "warn": "warning",
    "error": "error",
    "crit": "critical",
    "alert": "critical",
    "emerg": "critical",
}


def _parse_access_time(value: str) -> datetime:
    return datetime.strptime(value, "%d/%b/%Y:%H:%M:%S %z")


def parse_access_line(line: str) -> Optional[Dict[str, Any]]:
    match = ACCESS_REGEX.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    ts = _parse_access_time(data["time"])
    status = int(data["status"])
    severity = "info"
    if status >= 500:
        severity = "error"
    elif status >= 400:
        severity = "warning"

    message = f"{status} {data['method']} {data['path']}"
    metadata: Dict[str, Any] = {
        "remote_addr": data.get("remote"),
        "user": data.get("user"),
        "status": status,
        "method": data.get("method"),
        "path": data.get("path"),
        "protocol": data.get("proto"),
        "size": data.get("size"),
    }
    if data.get("referrer") is not None:
        metadata["referrer"] = data.get("referrer")
    if data.get("ua") is not None:
        metadata["user_agent"] = data.get("ua")

    return {
        "timestamp": ts,
        "severity": severity,
        "category": "web",
        "message": message,
        "metadata": metadata,
    }


def parse_error_line(line: str) -> Optional[Dict[str, Any]]:
    match = ERROR_REGEX.match(line.strip())
    if not match:
        return None
    data = match.groupdict()
    ts_str = f"{data['date']} {data['time']}"
    ts = datetime.strptime(ts_str, "%Y/%m/%d %H:%M:%S").replace(tzinfo=timezone.utc)
    level = data.get("level", "error")
    severity = LEVEL_MAP.get(level, "error")

    metadata: Dict[str, Any] = {
        "pid": data.get("pid"),
    }
    message = data.get("message", "").strip()
    return {
        "timestamp": ts,
        "severity": severity,
        "category": "web",
        "message": message,
        "metadata": metadata,
    }


__all__ = ["parse_access_line", "parse_error_line"]
