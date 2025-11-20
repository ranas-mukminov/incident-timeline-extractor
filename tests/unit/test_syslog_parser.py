from datetime import timezone

from incident_timeline_extractor.parsing.syslog_parser import parse_syslog_line

SYSLOG_LINE = "Nov 19 08:12:30 db-1 postgres[2345]: restart completed"


def test_parse_syslog_line_default_severity():
    parsed = parse_syslog_line(SYSLOG_LINE)
    assert parsed is not None
    assert parsed["severity"] == "info"
    assert parsed["timestamp"].tzinfo == timezone.utc
    assert parsed["metadata"]["host"] == "db-1"
