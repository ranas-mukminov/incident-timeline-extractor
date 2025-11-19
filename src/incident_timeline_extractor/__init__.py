"""Incident timeline extractor package."""

from importlib.metadata import version

__all__ = ["__version__"]

try:
    __version__ = version("incident-timeline-extractor")
except Exception:  # pragma: no cover - package not installed
    __version__ = "0.0.0"
