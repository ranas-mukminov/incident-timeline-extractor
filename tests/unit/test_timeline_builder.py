from datetime import datetime, timezone

from incident_timeline_extractor.timeline.builder import build_timeline
from incident_timeline_extractor.timeline.model import Event


def test_build_timeline_sorts_and_sets_bounds():
    events = [
        Event(
            id="b",
            timestamp=datetime(2025, 11, 19, 8, 12, 5, tzinfo=timezone.utc),
            source="nginx",
        ),
        Event(
            id="a",
            timestamp=datetime(2025, 11, 19, 8, 12, 1, tzinfo=timezone.utc),
            source="syslog",
        ),
        Event(
            id="c",
            timestamp=datetime(2025, 11, 19, 8, 12, 6, tzinfo=timezone.utc),
            source="zabbix",
        ),
    ]
    timeline = build_timeline("INC-1", events)
    assert timeline.started_at == events[1].timestamp
    assert timeline.ended_at == events[2].timestamp
    assert [e.id for e in timeline.events] == ["a", "b", "c"]
