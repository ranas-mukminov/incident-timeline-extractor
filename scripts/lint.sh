#!/usr/bin/env bash
set -euo pipefail

ruff check src tests || exit 1
black --check src tests || exit 1
isort --check-only src tests || exit 1
mypy src || exit 1
