from __future__ import annotations

from pathlib import Path
from typing import Literal

from jinja2 import Environment, FileSystemLoader, select_autoescape

from postmortem_generator_ai.model import Postmortem

TEMPLATES = {
    "en": "sre_en.md.j2",
    "ru": "sre_ru.md.j2",
}

_env = Environment(
    loader=FileSystemLoader(Path(__file__).parent / "templates"),
    autoescape=select_autoescape(enabled_extensions=(".j2",)),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_markdown(postmortem: Postmortem, language: Literal["en", "ru"] = "en") -> str:
    template_name = TEMPLATES.get(language, TEMPLATES["en"])
    template = _env.get_template(template_name)
    return template.render(pm=postmortem)


__all__ = ["render_markdown"]
