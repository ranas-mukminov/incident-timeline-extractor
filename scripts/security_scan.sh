#!/usr/bin/env bash
set -euo pipefail

pip-audit || exit 1
bandit -r src || exit 1
