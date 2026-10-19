#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

npm run gen:api:check
npx eslint .
npx tsc -b
npx vitest run --coverage
