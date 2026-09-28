# Follow-up questions for Egor (2026-09-28)

- Date: 2026-09-28
- From: Akim. To: Egor.
- Context: your answers to `normatives-formula-contract-review-egor.md` (findings 11-15)
  and `backend-layered-architecture-split-egor-ack.md`, applied on
  `feature/normative-parser/ml`, not merged into `develop` yet; my answer in
  `formula-verification-akim.md` (verification stays an internal team step for MVP, not
  a customer-facing one). Five smaller items came up while reading that state against
  our plan. None of these blocks WP5's current implementation tasks; they will block
  `normative-catalog-backend` and the pilot if left open.

Russian version: `pipeline-followup-questions-egor-rus.md`.

## 1. Write path for a formula/coefficient's `status`/`provenance`

Since verification stays an internal step for MVP (`formula-verification-akim.md`), the
team marks a formula or coefficient `human-verified` by hand on a small, closed set. Your
answer to question 8 gives the backend a read-only function and a read-only role into
`dec_normatives`; `design.md` decision 5 of `backend-layered-architecture` still marks the
loader/read-access question as "needs a joint decision", and a write for verification
wasn't part of that answer at all.

- **Proposal.** For MVP scale, no new write path: when the team marks a formula or
  coefficient reviewed, I tell you which one (document, edition, clause) and you run the
  update in your pipeline, the same way ingestion already writes these columns. A
  dedicated write role or a review API is a `normative-catalog-backend` question, once the
  catalog is bigger than a handful of MVP formulas.
- **Your side.** Agree for MVP, or propose a lighter path (e.g. a small CLI you expose
  that either of us runs, so it's not always you by hand).

## 2. Storage directory for downloaded normative documents

Three different values exist for the same purpose:

- `develop`'s `.gitignore`: `norm-docs/`
- `feature/normative-collector/data`: `norm-base/`
- `feature/normative-parser/ml`: `docs/normative-base/`

`normatives-formula-contract` task 3.1 ("`norm-base` → `norm-docs`") is unchecked and
matches neither branch. Merging either branch as-is conflicts with `develop`'s
`.gitignore` line and with each other.

- **Your side.** Which value is final? I'll wait for your answer before touching any
  `.gitignore` line or document that names this path (`CLAUDE.md`,
  `normatives-pilot-usage-akim.md`).

## 3. `formulas.toml` entries marked `human-verified` at ingestion

Your answer 12 stores hand-registry entries as `human-verified` at ingestion time, since a
person wrote them. Given the internal-review decision in `formula-verification-akim.md`,
I want to check this stays consistent: a registry entry gets that status because someone
who could check it against the source text wrote it, not because ingestion itself is a
verification step.

- **Your side.** Confirm that reading, or say if you see it differently. If it's fine, no
  action needed; I mention it only so the two decisions (yours on storage, mine on who
  verifies) don't drift apart silently.

## 4. Timing for the pilot-chain items

Three of your open items gate `calculation-core-contract` task 7.1 (the pilot):
`retarget-mvp-domain` task 3.1 (in-scope list for `foundations-shallow`), its task 1.3
(rewriting your parts of WP1), and `normatives-formula-contract` tasks 1.4-1.7 (`NormRef`
on coefficients, stored `status`/`provenance`, agreed but not yet implemented).

- **Your side.** A rough order or ETA, even approximate, so I know whether to start
  preparing the pilot now or hold off. Not asking for a date, just which of the three
  comes first.

## 5. Env var name for the normative-catalog connection

`backend-layered-architecture` task 2.1 already reserves `DEC_NORMATIVES_DATABASE_URL` as
an optional setting, read-only for now (question 1 above may add a write path later).

- **Your side.** Confirm this name matches what your infra change will produce (role per
  zone, per your answer to question 5 in the formula-contract review), so I don't need to
  rename it in code later.

## Not asked here

Anything about `ml-model-storage` or your infra change; both are still yours and not
created yet. The repository-layout question (`normatives_pipeline/` under its own
`normatives/` directory) is a separate note,
`repo-layout-symmetric-zones-egor.md`, committed alongside this one.
