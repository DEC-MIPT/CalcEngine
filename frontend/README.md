# DEC frontend

React 19, TypeScript, Vite, React Router, Tailwind CSS 4 with shadcn base tokens. Spec: `openspec/changes/frontend-app/`.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Dev server against the real backend at `VITE_API_BASE_URL` (default `http://127.0.0.1:8000` in development only; a production build without it calls its own origin). The backend needs `DEC_CORS_ORIGINS` with the dev server's origin. |
| `npm run dev:mock` | Dev server with MSW answering the API in the browser; no backend needed. |
| `npm run test:e2e` | Playwright in Chromium, Firefox and WebKit against its own `dev:mock` server on port 5179 (never an already running server). Not part of `check.sh`. One-time: `npx playwright install chromium firefox webkit`, and on Linux the system packages that `npx playwright install-deps` names. |
| `npm run gen:api` | Regenerates `src/api/schema.d.ts` from the backend's OpenAPI description. |
| `npm run gen:api:check` | Fails when the committed `schema.d.ts` is out of date (used by `check.sh`). |
| `./check.sh` | `gen:api:check`, `eslint`, `tsc -b`, `vitest run --coverage` (branch coverage >= 95%). |

## Mocks

`npm run dev:mock` runs the app with no backend: the handlers in `src/mocks/handlers.ts` serve `GET /calculation-types`, `POST /calculations`, `GET /calculations/{id}` and `POST /calculations/{id}/report` in the browser. The real backend computes the pilot only with the catalog (`DEC_NORMATIVES_DATABASE_URL`); without it `POST /calculations` answers `503 parameter_source_unavailable`.

- `POST /calculations` picks the envelope from the inputs: `b` above the method's bound gives the refusal, `b` above the validated range the warning, otherwise `p` of 172.5 kPa or less the pass and above it the fail. A missing input or an unknown type gives a `422` that names its place.
- `GET /calculations/{id}` returns the stored envelope for `11111111-1111-4111-8111-111111111111` (pass), `22222222-…` (fail), `33333333-…` (refused) and `44444444-…` (warning); any other id is a `404`. `POST /calculations/{id}/report` answers those ids with a stub `.docx` named `report.docx`.
- The same handlers run in Vitest (`src/test/setup.ts`); a test replaces one with `server.use(...)`, for example `serviceUnavailable` for the `503`.
- `public/mockServiceWorker.js` serves only the mock mode: a build in any other mode drops it from `dist/` (`vite.config.ts`).

`src/mocks/fixtures.ts` was generated from the backend (`calculation_types(...)` and `backend/tests/fixtures/pilot_envelope_before_metadata.json`) and is checked against the generated types by `tsc`.

## Backend types

`npm run gen:api` runs `backend/.venv/bin/python` (override with `DEC_PYTHON`) to read `create_app().openapi()` and writes `src/api/schema.d.ts`. Regenerate it after any change of the backend's API schemas.

## Layout

- `src/api/`: generated types, `createApi`, `unwrap` (structured API errors).
- `src/mocks/`: MSW handlers, fixtures, Node and browser setup.
- `src/components/`: the screen parts; `Formula.tsx` and `typeset.ts` render LaTeX through MathJax (SVG, TeX base and ams only, safe handler with no URLs, classes, ids or styles), with a raw-text fallback.
- `src/screens/`, `src/routes.tsx`: the four screens (type selection, form, result, report) and the not-found screen.
- `src/form/`: the input draft, value parsing (decimal comma accepted) and the mapping of server `422`s to fields.
- `src/lib/`: trace symbols, output rounding (same rule as the backend's `RoundingRule.apply`), trace playback, unit factors, motion.
- `src/report/`: the report file name from `Content-Disposition`, the download, report errors.
- `src/i18n/`: the Russian and English dictionaries and the unit designations; the language switch is hidden in the pilot's first iteration.
- `src/test/`, `e2e/`: Vitest setup and the axe helper; the Playwright specs and the formula harness.
- `src/index.css`: the design tokens (drafting-sheet direction, `openspec/changes/frontend-app/design.md`, decision 5).
- First-iteration settings (`frontend-app` design decision 12): `SHOW_LANGUAGE_SWITCH` in `src/components/AppShell.tsx`, `SHOW_NORM_STATUS` and `SHOW_ROUNDING_SOURCE` in `src/screens/ResultScreen.tsx`; all off until the first outside showing.
