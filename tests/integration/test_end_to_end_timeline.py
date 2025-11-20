from pathlib import Path

from incident_timeline_extractor.config import load_config
from incident_timeline_extractor.sources.journald import JournaldSource
from incident_timeline_extractor.sources.nginx import NginxSource
from incident_timeline_extractor.sources.prometheus import PrometheusSource
from incident_timeline_extractor.sources.syslog import SyslogSource
from incident_timeline_extractor.sources.zabbix import ZabbixSource
from incident_timeline_extractor.timeline.builder import build_timeline
from incident_timeline_extractor.timeline.serializer import to_json


def test_end_to_end_timeline(tmp_path: Path):
    cfg = load_config(Path("examples/config.yaml"))
    sources_cfg = cfg.incident_timeline_extractor.sources
    sources = [
        JournaldSource(file=sources_cfg.journald.file, units=sources_cfg.journald.units),
        NginxSource(access_log=sources_cfg.nginx.access_log, error_log=sources_cfg.nginx.error_log),
        SyslogSource(files=sources_cfg.syslog.files),
        ZabbixSource(file=sources_cfg.zabbix.file, mode=sources_cfg.zabbix.mode),
        PrometheusSource(file=sources_cfg.prometheus.file, url=sources_cfg.prometheus.url),
    ]

    events = []
    for source in sources:
        events.extend(source.collect())

    timeline = build_timeline("INC-INTEG", events)
    assert len(timeline.events) >= 6  # Actual events from example logs
    sorted_ids = [
        e.id for e in sorted(timeline.events, key=lambda e: (e.timestamp, e.source, e.id))
    ]
    assert [e.id for e in timeline.events] == sorted_ids

    output = tmp_path / "timeline.json"
    output.write_text(to_json(timeline), encoding="utf-8")
    assert output.exists()
