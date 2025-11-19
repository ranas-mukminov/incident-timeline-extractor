from datetime import datetime, timezone

from incident_timeline_extractor.timeline.model import Event, Timeline
from incident_timeline_extractor.timeline.serializer import from_json, to_json


def test_timeline_json_roundtrip():
    event = Event(
        id="evt-1",
        timestamp=datetime(2025, 11, 19, 8, 12, 1, tzinfo=timezone.utc),
        source="nginx",
        severity="error",
        category="web",
        message="502 Bad Gateway",
        raw={"status": 502},
        tags=["http_5xx"],
        correlation_id="corr-1",
    )
    timeline = Timeline("INC-1", event.timestamp, event.timestamp, [event], metadata={"services": ["frontend"]})
    data = to_json(timeline)
    restored = from_json(data)
    assert restored.incident_id == "INC-1"
    assert len(restored.events) == 1
    restored_event = restored.events[0]
    assert restored_event.message == event.message
    assert restored_event.raw["status"] == 502
