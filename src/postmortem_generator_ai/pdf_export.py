from __future__ import annotations

from html import escape
from pathlib import Path


def markdown_to_pdf(markdown_content: str, output_path: Path) -> None:
    try:
        import weasyprint  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("weasyprint is required for PDF export") from exc

    html_body = f"<pre style='font-family: monospace;'>{escape(markdown_content)}</pre>"
    weasyprint.HTML(string=html_body).write_pdf(str(output_path))


__all__ = ["markdown_to_pdf"]
