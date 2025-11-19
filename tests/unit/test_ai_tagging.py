from datetime import datetime, timezone

from ai_providers.mock_provider import MockProvider
from incident_timeline_extractor.ai.tagging import tag_events
from incident_timeline_extractor.timeline.model import Event


def test_mock_provider_adds_tags():
    events = [
        Event(
            id="evt-1",
            timestamp=datetime.now(timezone.utc),
            source="nginx",
            severity="error",
            message="502 on /",
            raw={"status": 502},
        )
    ]
    tagged = tag_events(events, MockProvider())
    assert "suspect" in tagged[0].tags or "http_5xx" in tagged[0].tags
