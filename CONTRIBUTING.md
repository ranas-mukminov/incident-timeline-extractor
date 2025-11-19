# Contributing

Thanks for helping improve `incident-timeline-extractor`!

## Development setup
- Python 3.10+
- Install editable + dev deps: `pip install -e .[dev]`
- Run tests: `pytest`
- Lints/format: `./scripts/lint.sh`

## Guidelines
- Keep code typed, small, and well-documented; prefer pure functions for parsing.
- Add unit tests for new features; update integration tests/examples when changing formats.
- Avoid introducing hard-coded secrets or network calls in code paths used by tests.
- Respect the Apache-2.0 license for all contributions.

## Pull requests
- Describe the problem, approach, and validation steps.
- Include CLI examples or docs for user-facing changes.
- CI must pass (lint + tests). Security checks should be clean.

## Code of conduct
Be respectful and collaborative. Blamelessly discuss issues and incidents; focus on learning and improvement.
