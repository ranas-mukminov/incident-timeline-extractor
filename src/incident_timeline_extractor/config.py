from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class JournaldConfig:
    enabled: bool = False
    units: list[str] = field(default_factory=list)
    file: Path | None = None


@dataclass
class NginxConfig:
    enabled: bool = False
    access_log: Path | None = None
    error_log: Path | None = None
    log_format: str | None = None


@dataclass
class SyslogConfig:
    enabled: bool = False
    files: list[Path] = field(default_factory=list)


@dataclass
class ZabbixConfig:
    enabled: bool = False
    mode: str = "file"
    file: Path | None = None
    api_url: str | None = None


@dataclass
class PrometheusConfig:
    enabled: bool = False
    file: Path | None = None
    url: str | None = None


@dataclass
class SourcesConfig:
    journald: JournaldConfig = field(default_factory=JournaldConfig)
    nginx: NginxConfig = field(default_factory=NginxConfig)
    syslog: SyslogConfig = field(default_factory=SyslogConfig)
    zabbix: ZabbixConfig = field(default_factory=ZabbixConfig)
    prometheus: PrometheusConfig = field(default_factory=PrometheusConfig)


@dataclass
class ExtractorConfig:
    default_time_range_hours: int = 1
    sources: SourcesConfig = field(default_factory=SourcesConfig)


@dataclass
class AIConfig:
    provider: str = "mock"
    model: str | None = None


@dataclass
class Config:
    incident_timeline_extractor: ExtractorConfig = field(default_factory=ExtractorConfig)
    ai: AIConfig = field(default_factory=AIConfig)


def _as_path(value: Any) -> Path | None:
    if value is None:
        return None
    return Path(str(value))


def _load_sources(data: dict[str, Any]) -> SourcesConfig:
    journald_cfg = data.get("journald", {})
    nginx_cfg = data.get("nginx", {})
    syslog_cfg = data.get("syslog", {})
    zabbix_cfg = data.get("zabbix", {})
    prometheus_cfg = data.get("prometheus", {})

    return SourcesConfig(
        journald=JournaldConfig(
            enabled=bool(journald_cfg.get("enabled", False)),
            units=list(journald_cfg.get("units", []) or []),
            file=_as_path(journald_cfg.get("file")),
        ),
        nginx=NginxConfig(
            enabled=bool(nginx_cfg.get("enabled", False)),
            access_log=_as_path(nginx_cfg.get("access_log")),
            error_log=_as_path(nginx_cfg.get("error_log")),
            log_format=nginx_cfg.get("log_format"),
        ),
        syslog=SyslogConfig(
            enabled=bool(syslog_cfg.get("enabled", False)),
            files=[p for f in syslog_cfg.get("files", []) if (p := _as_path(f)) is not None],
        ),
        zabbix=ZabbixConfig(
            enabled=bool(zabbix_cfg.get("enabled", False)),
            mode=str(zabbix_cfg.get("mode", "file")),
            file=_as_path(zabbix_cfg.get("file")),
            api_url=zabbix_cfg.get("api_url"),
        ),
        prometheus=PrometheusConfig(
            enabled=bool(prometheus_cfg.get("enabled", False)),
            file=_as_path(prometheus_cfg.get("file")),
            url=prometheus_cfg.get("url"),
        ),
    )


def load_config(path: Path) -> Config:
    """Load configuration from YAML path and perform minimal validation."""

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    extractor_cfg = data.get("incident_timeline_extractor", {})
    sources_cfg = _load_sources(extractor_cfg.get("sources", {}))
    extractor = ExtractorConfig(
        default_time_range_hours=int(extractor_cfg.get("default_time_range_hours", 1)),
        sources=sources_cfg,
    )

    ai_cfg = data.get("ai", {})
    ai = AIConfig(provider=ai_cfg.get("provider", "mock"), model=ai_cfg.get("model"))

    cfg = Config(incident_timeline_extractor=extractor, ai=ai)
    _validate_config(cfg)
    return cfg


def _validate_config(cfg: Config) -> None:
    sources = cfg.incident_timeline_extractor.sources
    if sources.nginx.enabled and not (sources.nginx.access_log or sources.nginx.error_log):
        raise ValueError("Nginx source enabled but no access_log/error_log configured")
    if sources.syslog.enabled and not sources.syslog.files:
        raise ValueError("Syslog source enabled but no files are configured")
    if sources.zabbix.enabled and sources.zabbix.mode == "file" and not sources.zabbix.file:
        raise ValueError("Zabbix file mode enabled without file path")
    if sources.prometheus.enabled and not (sources.prometheus.file or sources.prometheus.url):
        raise ValueError("Prometheus source enabled but neither file nor url provided")


__all__ = [
    "Config",
    "ExtractorConfig",
    "AIConfig",
    "SourcesConfig",
    "JournaldConfig",
    "NginxConfig",
    "SyslogConfig",
    "ZabbixConfig",
    "PrometheusConfig",
    "load_config",
]
