from datetime import timezone
from pathlib import Path

from incident_timeline_extractor.sources.journald import JournaldSource


def test_journald_source_reads_file():
    source = JournaldSource(file=Path("examples/logs/journald_export.txt"))
    events = list(source.collect())
    assert len(events) == 2
    first = events[0]
    assert first.service == "nginx.service"
    assert first.timestamp.tzinfo == timezone.utc
    assert first.severity == "info"
