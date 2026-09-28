#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

ruff check .
mypy .
if [ -d app ]; then
  pytest --cov=app --cov-branch --cov-fail-under=95
else
  pytest
fi
