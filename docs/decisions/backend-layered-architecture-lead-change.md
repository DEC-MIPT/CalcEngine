# `backend-layered-architecture` (WP5): lead moved from Egor to Akim

- Date: 2026-09-28
- From: Akim. To: Egor.

Russian version: `backend-layered-architecture-lead-change-rus.md`.

## Decision

`backend-layered-architecture` (WP5) is led by Akim from now on, not Egor. Rationale:
`AGENTS.md` section 5 assigns the `backend/` responsibility zone to Akim
(frontend/backend, calculation engine, report generator); this change is primarily
about `backend/`'s layout, so the zone owner leads it and takes responsibility for its
decisions, the way any other zone-owned change already works.

This changes who leads the change and decides its backend-zone content, not the
technical decisions already recorded in `design.md` — none of those are reopened by
this note.

## What stays Akim's, decided and implemented without asking Egor

Sections 1-3 and 5-6 of `tasks.md`: the layered `backend/app` scaffold, `core/config.py`
and its env vars, `dec_app`'s session/migrations, the parameters layer, and the
calculation engine interface. None of these cross into Egor's zones (normative
pipeline, ML/DL/NLP, DevOps).

## What still needs Egor — because it crosses into his zone, not because he leads WP5

- **Task 9.3** (open): where normative ingestion/catalog code lives — `backend/normatives/`
  with its own manual loader (this change's current plan, `design.md` decision 5), or
  Egor's existing `normatives_pipeline/`. This is section 4 of `tasks.md`; those tasks
  do not start until 9.3 is settled with Egor and the outcome is recorded in `design.md`,
  per section 9's own rule.
- **Task 9.6** (open, Egor's alone): renaming/splitting `docker-compose.yml`'s database
  into `dec_app`/`dec_normatives` and the role per zone — DevOps is Egor's zone.
- **Task 9.7** (open): `ml/`'s layout (section 7 of `tasks.md`) against Egor's existing
  `normatives_pipeline/ocr/` and model artifacts. ML/DL/NLP is Egor's zone per
  `AGENTS.md` section 5, independent of who leads this change — section 7 is his to
  decide and implement, the same as before this note.
- **Section 8** (Docker/local env, `docker-compose.yml` and its `.gitignore` entries):
  DevOps is Egor's zone; task 9.6 already named him as its owner.
- **The two open gaps of task 9.4** (`design.md` decision 5a): `Formula`/`Coefficient`
  need `NormRef` fields (`document`/`edition`/`clause`/`status`/`provenance`) his
  `coefficient` table does not have yet — tracked as questions 11-13 of
  `docs/decisions/normatives-formula-contract-review-egor.md`, not closed by this note.

## What this note does not change

- `retarget-mvp-domain` (WP1) stays led by Egor; this note is scoped to WP5 only.
- Section 9's existing rule stands: "the tasks of sections 3-8 that an item names are
  not implemented until Akim and Egor settle that item" (`tasks.md`, section 9
  preamble). Owning WP5 does not let Akim implement section 4 or 7 ahead of 9.3/9.7.
- The DOR gap already noted in `docs/reports/` (no `spec-reviewer` report, no `tester`
  spec-phase verdict recorded yet for this change): still open, lead change does not
  substitute for it.
