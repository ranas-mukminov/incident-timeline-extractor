from pathlib import Path

from ai_providers.mock_provider import MockProvider
from incident_timeline_extractor.timeline.serializer import from_json
from postmortem_generator_ai.generator import generate_postmortem
from postmortem_generator_ai.renderer import render_markdown


def test_end_to_end_postmortem(tmp_path: Path):
    timeline_path = Path("examples/timelines/example_timeline.json")
    timeline = from_json(timeline_path.read_text(encoding="utf-8"))
    pm = generate_postmortem(timeline, "Synthetic outage", MockProvider())
    md = render_markdown(pm, language="en")
    output = tmp_path / "postmortem.md"
    output.write_text(md, encoding="utf-8")
    assert "Incident ID" in md
    assert "Action Items" in md
