# Reply to Egor's answers on the pipeline follow-up, branching and repo layout

- Date: 2026-09-29
- From: Akim. To: Egor.
- Context: reply to `pipeline-followup-answers-egor-rus.md`.

Russian version: `pipeline-followup-answers-akim-rus.md`.

## A1, D. Formula status: auto-verified

I do not accept the flag button and the per-formula counters. Please take your fallback: set
every formula to "verified, correct" yourself. There is no per-formula manual verification on
my side and no user-side verification action, so I add no endpoint, counter or button for it.
This closes `formula-verification-akim.md`.

Consequence for the schema: `status` and `provenance` are still stored per formula and per
coefficient (findings 11-15), and the columns `shown_count` and `flagged_count` are not needed.

## A2. `docs/normative-base/` and `norm-docs/` in `.gitignore`

Agreed, the folder name stays `docs/normative-base/`. I do not edit `.gitignore` on
`develop`, for two reasons:

- On `feature/normative-parser/ml` the line `norm-docs/` is already replaced by
  `docs/normative-base/`, so it leaves `develop` when you merge that feature. An edit of mine
  on `develop` would conflict with yours in the same hunk.
- The code on `develop` (`normatives_pipeline/ingest.py`, `normatives_pipeline/parser/cli.py`,
  `tests/`) still reads `norm-docs/`. Without the ignore line, downloaded full texts there would
  show up as untracked files, and the full texts of norms must not be committed.

Please keep the line until your branch is merged, and do not download into `norm-docs/` in
the meantime.

## A3. `formulas.toml`

Agreed: delete it. No separate decision on `human-verified` for that file is needed.

## A4. Order of the pilot blockers

Agreed: `normatives-formula-contract` 1.4-1.7, then `retarget-mvp-domain` 3.1, then 1.3.

## A5. `DEC_NORMATIVES_DATABASE_URL`

Confirmed. My `Settings` keeps `DEC_DATABASE_URL` for the `dec_app` database only, so the two
names do not collide.

## B. Branching

Thanks for the confirmation. The formula-contract code stays on `feature/normative-parser/ml`.

## C. Repo layout

- C1: agreed. `backend/` and `frontend/` stay in the root, `ml/` is yours.
- C4: agreed, `backend/tests/` for my tests, no shared root `tests/`. The root `pyproject.toml`
  (`testpaths`, coverage `source`) has to change; it is shared, so I touch it only after you have
  moved your tests to `ml/tests/` and told me, and I show you the diff first.
- `infra/docker-compose.yml`: agreed. Please keep the service name `dec-postgres` and port 5433,
  my WP5 task 3.x verify clauses use them. I update my references once the move is on `develop`.

## Open for you

- Tell me when `tests/` and `docker-compose.yml` have moved.
- Tell me when the automatic "verified" status is in place.
