# Normative Pipeline + NLP/ML in MVP — Plan (Egor)

## 0. Prerequisite — branching model change (delete `develop`, base = `main`)

Decision (Egor, confirmed): simplify to trunk-based (`main` + `feature/<task>/<zone>`).
`develop` is removed.

Git steps (implementation agent, NOT plan mode):

1. `git checkout main`
2. `git merge --no-ff develop` — required: `main` holds only `d15cb13 Initial commit`, so
   merging develop into main is the only coherent way to keep the work while branching
   future work from main.
3. `git branch -d develop` and `git push origin --delete develop`.
4. Verify `git log --oneline main` contains develop's commits (`49de2f9`, `472e962`, …)
   and `git branch -a` no longer lists `develop`/`origin/develop`.

Consequence: `main` is un-frozen — it becomes the integration trunk; the "main frozen
until MVP" rule is removed.

Files to update (develop → main, drop "main frozen", feature branches from main):

1. `AGENTS.md` §2 branching rules (`:51-68`) + session-start checks (`:74-82`).
2. `openspec/config.yaml:29-35`.
3. `.kilo/skills/branching-convention/SKILL.md`.
4. `.kilo/skills/sdd-workflow/SKILL.md` (`:19`, `:30`).
5. `.kilo/agent/orchestrator.md:28-30`.
6. `.kilo/agent/frontend-developer.md:11-12`.
7. `README.md:19-20`.

## 1. Final decisions (confirmed with Akim)

- **Zone split — unchanged** (rely on the files): `AGENTS.md:131` Akim =
  frontend/backend, engine, report generator; `AGENTS.md:132` Egor = normative pipeline,
  NLP/RAG, ML, **DevOps** (zones `data`/`ml`/`infra`). DevOps stays Egor.
- **ML/NLP → MVP** (reverses the "NLP non-goal"); "No ML in the calculation path" stays.
- **Branching**: `feature/<task>/<zone>` from `main` (section 0). Egor:
  `feature/normative-pipeline/data`, `feature/normative-parsing/ml`, `feature/<task>/infra`.
- **Compute**: CPU-only now; generative LLM deferred until GPU/budget.
- **Storage**: PostgreSQL `dec_normatives` + Docker — owned by Egor (infra).
- **Component**: separate `normatives-pipeline/` code (collector + parser), batch/CLI, no
  public API; backend reads `dec_normatives`.
- **Provenance**: human-in-the-loop stays — engine accepts only `human-verified`; NLP is
  a drafting aid, not a source of machine-verified values.

## 2. Scope change "ML in MVP" — files to update

Remove "NLP/RAG parsing = future/non-MVP" (keep "No ML in the calculation path"):

1. `openspec/changes/retarget-mvp-domain/proposal.md:53` — non-goal "NLP/RAG parsing of
   norms inside the product".
2. `openspec/changes/retarget-mvp-domain/specs/product-vision/spec.md:31` — the non-goal
   requirement list.
3. `openspec/config.yaml:40-41`.
4. `.kilo/agent/data-engineer.md:15-16`.
5. `AGENTS.md:27`.
6. `verified-roadmap.md:133` + `:372`.

Gate: the non-goals list is PM-owned ("DRAFT — the PM approves this list",
`retarget-mvp-domain/proposal.md:47`). Egor leads/reviews that change, but removing a
non-goal needs PM sign-off before implementation.

## 3. Work (simple → complex)

### Track A — Collector (`feature/normative-pipeline/data`)
1. Registry/discovery + statuses (faufcc.ru, minstroyrf.gov.ru, gost.ru,
   fgiscs.minstroyrf.ru, pravo.gov.ru) — H1/H3/H7.
2. Download + metadata (title/edition/status/date/source/sha256) + dedup/versioning →
   `dec_normatives` — H2/H4.

### Track B — Parser (`feature/normative-parsing/ml`)
3. Baseline: `pdfplumber`/`pdftotext` + regex for formulas/coefficient tables/clause
   refs; ground truth from методические пособия + spot manual markup; F1
   (formula/coefficient_table/clause_ref), exec_rate, T_digit — H5/H6.
4. Retrieval: `cointegrated/rubert-tiny2` → ONNX embeddings over parsed text + vector
   search; recall@k vs pg_trgm baseline; record in `docs/10` — CPU-only.
5. (Deferred) generative-LLM structured extraction — when GPU/budget.

### Track C — Infra (`feature/<task>/infra`)
6. Docker + PostgreSQL (`dec_app` + `dec_normatives`, extensions pg_trgm + pgvector) —
   matches `verified-roadmap.md` WP6 requirement 5.

### Cross-cutting
7. `norm-source-traceability` (WP3, DE leads): NormRef, provenance, status model, legal
   gate (C5). Aligns the data model that A and B fill.
8. Process: `AGENTS.md` §10 "ML research experiments" + `docs/10-модели-эксперименты-дневник.md`.

## 4. Risks / failure modes

- Scan-only PDFs (H4) → OCR (Surya, CPU) accuracy ceiling; classify text-layer vs scan
  first.
- Registry non-uniformity (H1) → multi-source aggregator + manual status review.
- Legal (H2/C5) → full text stored locally for research; product may expose structured
  entities only; PM's legal answer pending.
- Data loss during branching change → merge develop into main BEFORE deleting develop
  (section 0); verify log before `push --delete`.
- Provenance regression → machine-extracted values must never bypass the `human-verified`
  gate to the engine (enforced by `norm-source-traceability`).
- Zone overlap → collector/parser stay in `data`/`ml`; ORM/migrations/serving in Akim's
  backend; schema = shared spec only.

## 5. Open questions

- Change structure: how collector/parser map to OpenSpec changes (two new changes vs fold
  into roadmap WPs) — deferred by Egor.
- PM sign-off for the "ML in MVP" scope change.

## 6. Non-goals

- No ML in the calculation path.
- No generative LLM in this phase.
- No change to the zone split or the roadmap WP structure.

## 7. Validation

- Branching: `main` contains develop's history; `develop` gone (local + remote); files match.
- Collector: 5-doc pilot dataset downloadable + metadata stored; registry recall ≥ 95% (H1).
- Parser: F1/exec_rate reported; recall@k beats pg_trgm; recorded in `docs/10`.
- Process: scope files updated; `docs/10` exists; every experiment has a conclusion.
