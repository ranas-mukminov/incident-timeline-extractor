from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

SEVERITY_MAP = {
    "critical": "critical",
    "warn": "warning",
    "warning": "warning",
    "info": "info",
    "error": "error",
}


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def parse_alertmanager(payload: Any) -> list[dict[str, Any]]:
    if payload is None:
        return []
    alerts: list[Any] = []
    if isinstance(payload, dict):
        alerts = payload.get("alerts") or []
    elif isinstance(payload, list):
        alerts = payload
    result: list[dict[str, Any]] = []
    for alert in alerts:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        status = alert.get("status", "firing")
        severity = SEVERITY_MAP.get(labels.get("severity", "info").lower(), "info")
        ts = _parse_time(alert.get("startsAt")) or datetime.now(timezone.utc)
        message = (
            annotations.get("summary")
            or annotations.get("description")
            or labels.get("alertname")
            or "Prometheus alert"
        )
        metadata = {
            "labels": labels,
            "annotations": annotations,
            "status": status,
        }
        result.append(
            {
                "timestamp": ts,
                "severity": severity,
                "category": "alert",
                "message": message,
                "metadata": metadata,
            }
        )
    return result


__all__ = ["parse_alertmanager"]
