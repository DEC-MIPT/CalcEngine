#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

npm run gen:api:check
npm run gen:fixtures:check
node scripts/gen-loads-fixtures.mjs --design --check
npx eslint .
npx tsc -b
npx vitest run --coverage
