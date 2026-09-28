#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

npx eslint .
npx tsc -b
npx vitest run --coverage
