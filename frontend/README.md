# DEC frontend

React 19, TypeScript, Vite, React Router, Tailwind CSS 4 with shadcn base tokens. Spec: `openspec/changes/frontend-app/`.

## Commands

| Command | What it does |
|---|---|
| `npm run dev` | Dev server against the real backend at `VITE_API_BASE_URL` (default `http://127.0.0.1:8000`). |
| `npm run dev:mock` | Dev server with MSW answering the API in the browser; no backend needed. |
| `npm run gen:api` | Regenerates `src/api/schema.d.ts` from the backend's OpenAPI description. |
| `npm run gen:api:check` | Fails when the committed `schema.d.ts` is out of date (used by `check.sh`). |
| `./check.sh` | `gen:api:check`, `eslint`, `tsc -b`, `vitest run --coverage` (branch coverage >= 95%). |

## Mocks while the backend answers 503

Until `normative-catalog-backend` is merged, `POST /calculations` for the pilot answers `503 parameter_source_unavailable`. Run `npm run dev:mock`: the handlers in `src/mocks/handlers.ts` serve `GET /calculation-types`, `POST /calculations`, `GET /calculations/{id}` and `POST /calculations/{id}/report`.

- A `POST /calculations` with `p` of 172.5 kPa or less returns the passing envelope, above that the failing one; a missing input gives a `422` that names its place; an unknown type gives a `422`.
- `GET /calculations/11111111-1111-4111-8111-111111111111` (pass) and `.../22222222-2222-4222-8222-222222222222` (fail) return the stored envelopes; any other id is a `404`.
- The same handlers run in Vitest (`src/test/setup.ts`); a test replaces one with `server.use(...)`, for example `serviceUnavailable` for the `503`.
- Refused and warning envelopes are not mocked yet.

`src/mocks/fixtures.ts` was generated from the backend (`calculation_types(...)` and `backend/tests/fixtures/pilot_envelope_before_metadata.json`) and is checked against the generated types by `tsc`.

## Backend types

`npm run gen:api` runs `backend/.venv/bin/python` (override with `DEC_PYTHON`) to read `create_app().openapi()` and writes `src/api/schema.d.ts`. Regenerate it after any change of the backend's API schemas.

## Layout

- `src/api/`: generated types, `createApi`, `unwrap` (structured API errors).
- `src/mocks/`: MSW handlers, fixtures, Node and browser setup.
- `src/components/Formula.tsx`: LaTeX through MathJax (SVG, TeX base and ams only), raw-text fallback.
- `src/screens/`, `src/routes.tsx`: the four routes (placeholders until the screens are built).
- `src/index.css`: the design tokens (drafting-sheet direction, `openspec/changes/frontend-app/design.md`, decision 5).
