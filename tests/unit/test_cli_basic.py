from pathlib import Path

from typer.testing import CliRunner

from incident_timeline_extractor.cli import app

runner = CliRunner()


def test_to_markdown_command():
    result = runner.invoke(app, ["to-markdown", "examples/timelines/example_timeline.json"])
    assert result.exit_code == 0
    assert "Incident Timeline" in result.stdout


def test_analyze_command(tmp_path: Path):
    output = tmp_path / "annotated.json"
    result = runner.invoke(
        app, ["analyze", "examples/timelines/example_timeline.json", "--output", str(output)]
    )
    assert result.exit_code == 0
    assert output.exists()
