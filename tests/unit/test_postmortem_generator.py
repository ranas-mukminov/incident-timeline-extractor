from datetime import datetime, timezone

from ai_providers.mock_provider import MockProvider
from incident_timeline_extractor.timeline.model import Event, Timeline
from postmortem_generator_ai.generator import generate_postmortem


def test_generate_postmortem_returns_fields():
    event = Event(
        id="evt-1",
        timestamp=datetime(2025, 11, 19, 8, 12, 1, tzinfo=timezone.utc),
        source="nginx",
        severity="error",
        message="502 on /",
        raw={},
    )
    timeline = Timeline("INC-TEST", event.timestamp, event.timestamp, [event])
    pm = generate_postmortem(timeline, "frontend outage", MockProvider())
    assert pm.summary
    assert pm.action_items
    assert "Timeline" in pm.timeline_md
