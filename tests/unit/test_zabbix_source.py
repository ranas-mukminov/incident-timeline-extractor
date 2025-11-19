from pathlib import Path

from incident_timeline_extractor.sources.zabbix import ZabbixSource


def test_zabbix_source_parses_events():
    source = ZabbixSource(file=Path("examples/logs/zabbix_events.json"))
    events = list(source.collect())
    assert len(events) == 2
    assert events[0].severity == "error"
    assert events[0].host == "db-1"
