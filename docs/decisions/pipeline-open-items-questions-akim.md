# Pipeline open items: repo layout move and formula status (questions for Egor, 2026-10-03)

- Date: 2026-10-03
- From: Akim. To: Egor.
- Context: the two items under "Open for you" in `pipeline-followup-answers-akim.md`
  (2026-09-29) have no answer yet. `pipeline-followup-answers-egor-rus.md` predates them, and
  `a01af6f` (your answers on `normative-catalog-backend` and formula execution) does not
  cover them. Checked against `origin/feature/normative-parser/ml` at `a507529` (2026-09-29).
- How to answer: append an `## Answers` section to this file (`AGENTS.md`, section 7).

Russian version: `pipeline-open-items-questions-akim-rus.md`.

## 1. Repo layout move (`ml/`, `infra/`)

Agreed layout (`pipeline-followup-answers-egor-rus.md`, C1-C4): `backend/` and `frontend/` in
the root, `ml/` yours (`pyproject.toml`, `src/normatives_pipeline/`, `configs/`, `research/`,
`tests/`), `infra/docker-compose.yml` shared. You wrote in C2 that you move now, before the
merge into `develop`.

What I see on your branch: `infra/docker-compose.yml` is there and the root
`docker-compose.yml` is gone. There is no `ml/` yet: `pyproject.toml` (project
`normatives-pipeline`), `src/`, `tests/`, `configs/` and `research/` are still in the root. On
`develop` nothing has moved.

Why I need it: after your move I edit the root `pyproject.toml` (`testpaths`, coverage
`source`) with a diff shown to you first, update the paths in `CLAUDE.md`, and point my
`dec-postgres` references to `infra/`. I do none of this before the move is on `develop`.

- **Question 1a.** Is the target still `ml/` as agreed, with all of `pyproject.toml`, `src/`,
  `tests/`, `configs/` and `research/` inside it?
- **Question 1b.** Does a root `pyproject.toml` stay after the move? If your project moves to
  `ml/pyproject.toml` and the root file is deleted, my edit is not needed (the backend has its
  own `backend/pyproject.toml`). If a root file stays, what is in it?
- **Question 1c.** Please confirm that `infra/docker-compose.yml` keeps the service name
  `dec-postgres` and port 5433.
- **Your side.** When the move is merged into `develop`, write the merge commit here.

## 2. Formula status: the automatic "verified" mark

On 2026-09-29 I accepted your fallback: you mark every formula "verified" automatically
(`pipeline-followup-answers-akim.md`, A1). Then the formula-execution audit narrowed it
(`calculation-core-contract-formula-execution-akim.md`, item 3, acknowledged by you in
`a01af6f`): the mark does not become `NormRef.status`, `provenance = machine-extracted` always
means `status = unverified`, and the backend reads `provenance`, not the mark.

What I see on your branch: `src/normatives_pipeline/db.py:320-321` still writes the constants
`"status": "unverified"` and `"provenance": "machine-extracted"`; there is no automatic mark.

In `a01af6f`, item 3, you also wrote: "For the pilot, we accept for now that all its formulas
are treated as verified." With the backend rule above, every pilot step resting on a
`machine-extracted` formula is shown as unverified and counted in `unverified_step_count`.

- **Question 2a.** Is the automatic mark still planned? If yes: which column and which value,
  and does it go in with `normatives-formula-contract` 1.4-1.7?
- **Question 2b.** What does "treated as verified" mean for the pilot? Either (a) it is only
  the agreement between us and the data keep `provenance = machine-extracted`, so the pilot
  report shows its steps as unverified; or (b) the pilot formulas and coefficients get a
  `provenance` other than `machine-extracted` in the data, and then which value and on what
  basis (a check against the primary text of СП 22.13330.2016, as in your item 2 for the
  coefficients)?
- **Your side.** When the status columns are filled as decided, write the merge commit here.

Neither item blocks `calculation-api`: its tests use synthetic parameters. Both block
`normative-catalog-backend` and the pilot R on catalog data (WP2 task 7.1c).

## Answers

- Date: 2026-10-03
- From: Egor. To: Akim.

1. **Repo layout move (`ml/`, `infra/`).**

   - 1a. Yes — the target stays `ml/`, containing `pyproject.toml`,
     `src/normatives_pipeline/`, `configs/`, `research/`, `tests/`.
   - 1b. No root `pyproject.toml` stays after the move: the project moves to
     `ml/pyproject.toml`, and the backend has its own `backend/pyproject.toml`, so your
     edit to a root file is not needed.
   - 1c. Confirmed: the service is named `dec-postgres` and keeps port 5433. I rename the
     compose service key from `postgres` to `dec-postgres` so the name matches.
   - Merge commit: to be written here when the move is merged into `develop`.

2. **Formula status.**

   - 2a. Yes, the automatic mark is still planned, as the ingestion default. It writes the
     honest values, not "verified": `status = "unverified"` and
     `provenance = "machine-extracted"` into stored columns on `formula` and
     `coefficient` (replacing the constants in `build_formula_payload`). Columns: `status`,
     `provenance`. It lands with `normatives-formula-contract` 1.4-1.7 (task 1.6).
   - 2b. Option (a): for the pilot, mark as unverified. The data keep
     `provenance = "machine-extracted"` / `status = "unverified"`; the pilot report shows
     its steps as unverified and counts them in `unverified_step_count`. No pilot formula
     or coefficient gets a `human-verified` provenance.
   - Merge commit: to be written here when the status columns are filled as decided.
