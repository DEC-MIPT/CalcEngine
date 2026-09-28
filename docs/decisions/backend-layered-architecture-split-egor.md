# `backend-layered-architecture` (WP5): split, acknowledgement requested from Egor

- Date: 2026-09-28
- From: Akim. To: Egor.

Russian version: `backend-layered-architecture-split-egor-rus.md`.

## Decision

WP5 is split so that it holds only what Akim decides and implements in `backend/` with no
wait on Egor or WP1. Reason: `AGENTS.md` section 4 wants every task in `tasks.md` checked
off before GO, and section 3 wants dependencies "listed and satisfied". The second
`spec-reviewer` pass (finding N4) showed WP5 could meet neither while it carried tasks that
wait on your decisions and on WP1's list.

## What stays in WP5 (Akim)

Layered scaffold, `GET /health`, configuration, `DECError`, the `dec_app` session and
migration tree, the parameters layer for engineer-set values (`.yaml`), and the
`Calculator` interface and registry. Tasks 1.1-3.2, 5.1, 6.1.

## What moves out, and to whom

| Old task | Content | Goes to | Owner |
|---|---|---|---|
| 4.1-4.3, 5.1 (second half), 9.3 | `normatives/` package, `dec_normatives` migrations, loader, search, the parameters layer's reading of formulas and coefficients through the `provenance` gate; first decision: where this code lives | planned `normative-catalog-backend` | Akim and Egor |
| 7.1, 7.2, 9.7 | `ml/` layout, registry, ML `.gitignore`, layout against `normatives_pipeline/ocr/` | planned `ml-model-storage` | Egor |
| 8.1, 8.2, 9.6 | `docker-compose.yml` with `dec_app` + `dec_normatives`, extensions, `backend` service; the `dec` -> `dec_normatives` rename and a role per zone | your infra change (name is yours) | Egor |
| 5.2, 6.2 | Pilot parameter file and pilot implementation | `calculation-core-contract` task 7.1 | Akim |

None of the moved changes is created yet. Decisions 4-6 in WP5's `design.md` keep the
record of what you confirmed on 2026-09-27; nothing you confirmed is reopened.

## What Akim asks of Egor

1. Acknowledge that the sections in your zones (ML, Docker/DevOps) and the open items
   9.3, 9.6, 9.7 now live outside WP5, and that you own the ML and infra changes. Reply
   in a tracked file, or by a commit that names this note.
2. Note that WP5's task 3.x verify clauses use a `dec_app` database created by hand on
   the existing `dec-postgres` service. Nothing in `docker-compose.yml` is touched.
3. Nothing else is asked of you now. Question 9.3 (where the normative code lives) is
   not settled by this note; it is the first decision of `normative-catalog-backend`.
