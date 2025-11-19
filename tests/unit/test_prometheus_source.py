from pathlib import Path

from incident_timeline_extractor.sources.prometheus import PrometheusSource


def test_prometheus_source_reads_alerts():
    source = PrometheusSource(file=Path("examples/logs/prometheus_alerts.json"))
    events = list(source.collect())
    assert len(events) == 2
    assert events[0].severity == "critical"
    assert "HTTP 5xx" in events[0].message
