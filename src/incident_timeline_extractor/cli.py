from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from ai_providers.mock_provider import MockProvider
from incident_timeline_extractor.ai.clustering import cluster_events
from incident_timeline_extractor.ai.tagging import tag_events
from incident_timeline_extractor.config import Config, load_config
from incident_timeline_extractor.sources.journald import JournaldSource
from incident_timeline_extractor.sources.nginx import NginxSource
from incident_timeline_extractor.sources.prometheus import PrometheusSource
from incident_timeline_extractor.sources.syslog import SyslogSource
from incident_timeline_extractor.sources.zabbix import ZabbixSource
from incident_timeline_extractor.timeline.builder import build_timeline
from incident_timeline_extractor.timeline.serializer import (
    from_json,
    timeline_to_ascii,
    timeline_to_markdown,
    to_json,
)
from postmortem_generator_ai.generator import generate_postmortem
from postmortem_generator_ai.renderer import render_markdown
from postmortem_generator_ai.pdf_export import markdown_to_pdf

app = typer.Typer(help="Incident timeline extractor")
console = Console()


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _load_config(path: Optional[Path]) -> Config:
    if not path:
        # minimal default config
        return Config()
    return load_config(path)


def _enabled_sources(cfg: Config):
    sources = cfg.incident_timeline_extractor.sources
    instances = []
    if sources.journald.enabled:
        instances.append(JournaldSource(units=sources.journald.units, file=sources.journald.file))
    if sources.nginx.enabled:
        instances.append(
            NginxSource(
                access_log=sources.nginx.access_log,
                error_log=sources.nginx.error_log,
            )
        )
    if sources.syslog.enabled:
        instances.append(SyslogSource(files=sources.syslog.files))
    if sources.zabbix.enabled:
        instances.append(ZabbixSource(file=sources.zabbix.file, mode=sources.zabbix.mode))
    if sources.prometheus.enabled:
        instances.append(PrometheusSource(file=sources.prometheus.file, url=sources.prometheus.url))
    return instances


@app.command()
def collect(
    incident_id: str = typer.Option(..., help="Incident identifier"),
    config: Optional[Path] = typer.Option(None, exists=True, help="Path to config.yaml"),
    since: Optional[str] = typer.Option(None, help="Start time ISO8601"),
    until: Optional[str] = typer.Option(None, help="End time ISO8601"),
    output: Optional[Path] = typer.Option(None, help="Where to write JSON timeline"),
):
    """Collect events from configured sources and emit a JSON timeline."""

    cfg = _load_config(config)
    since_dt = _parse_dt(since)
    until_dt = _parse_dt(until)

    all_events = []
    for source in _enabled_sources(cfg):
        console.print(f"Collecting from {source.name} ...")
        all_events.extend(source.collect(since=since_dt, until=until_dt))

    timeline = build_timeline(incident_id, all_events)
    payload = to_json(timeline)
    if output:
        output.write_text(payload, encoding="utf-8")
        console.print(f"Timeline written to {output}")
    else:
        typer.echo(payload)


@app.command(name="to-markdown")
def to_markdown(
    timeline_path: Path = typer.Argument(..., exists=True, help="Timeline JSON"),
):
    """Convert JSON timeline to Markdown."""

    data = timeline_path.read_text(encoding="utf-8")
    timeline = from_json(data)
    typer.echo(timeline_to_markdown(timeline))


@app.command()
def analyze(
    timeline_path: Path = typer.Argument(..., exists=True, help="Timeline JSON"),
    output: Optional[Path] = typer.Option(None, help="Annotated JSON output"),
):
    """Run AI tagging and clustering on a timeline using the mock provider by default."""

    timeline = from_json(timeline_path.read_text(encoding="utf-8"))
    provider = MockProvider()
    events = tag_events(timeline.events, provider)
    clusters = cluster_events(events, provider)
    timeline.events = events
    timeline.metadata["clusters"] = [c.__dict__ for c in clusters]
    payload = to_json(timeline)
    if output:
        output.write_text(payload, encoding="utf-8")
        console.print(f"Annotated timeline written to {output}")
    else:
        typer.echo(payload)


@app.command()
def postmortem(
    timeline_path: Path = typer.Option(..., exists=True, help="Timeline JSON"),
    engineer_input: str = typer.Option("", "--input", help="Short engineer description"),
    lang: str = typer.Option("en", help="Language: en or ru"),
    output: Optional[Path] = typer.Option(None, help="Where to write postmortem Markdown"),
    pdf: Optional[Path] = typer.Option(None, help="Optional PDF output path"),
):
    """Generate a postmortem from a timeline using the mock AI provider."""

    timeline = from_json(timeline_path.read_text(encoding="utf-8"))
    provider = MockProvider()
    pm = generate_postmortem(timeline, engineer_input, provider, language=lang)
    markdown = render_markdown(pm, language=lang)
    if output:
        output.write_text(markdown, encoding="utf-8")
        console.print(f"Postmortem saved to {output}")
    else:
        typer.echo(markdown)
    if pdf:
        markdown_to_pdf(markdown, pdf)
        console.print(f"PDF saved to {pdf}")


@app.command()
def doctor(config: Optional[Path] = typer.Option(None, help="Config path")):
    """Basic sanity checks for configured sources."""

    cfg = _load_config(config)
    sources = cfg.incident_timeline_extractor.sources
    issues: list[str] = []
    if sources.nginx.enabled:
        if not (sources.nginx.access_log or sources.nginx.error_log):
            issues.append("Nginx enabled but no log paths provided")
    if sources.syslog.enabled and not sources.syslog.files:
        issues.append("Syslog enabled but no files configured")
    if sources.zabbix.enabled and sources.zabbix.mode == "file" and not sources.zabbix.file:
        issues.append("Zabbix file mode enabled without file")
    if sources.prometheus.enabled and not (sources.prometheus.file or sources.prometheus.url):
        issues.append("Prometheus enabled without file or url")

    if issues:
        for issue in issues:
            console.print(f"[red]- {issue}")
        raise typer.Exit(code=1)
    console.print("All sanity checks passed")


def main():  # pragma: no cover - entrypoint
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
