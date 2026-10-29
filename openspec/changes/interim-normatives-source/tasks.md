# Tasks

Owner: Akim (backend and frontend zones). No task of this change is in Egor's zones.

Branches: three features, each merged into `develop` only when every task assigned to it is
checked off, the `tester` has declared GO for it and the review has passed (`AGENTS.md`,
Branching rules):

- `feature/interim-normatives/backend` (Akim, from `develop`): sections 2-5, tasks 7.1-7.4c
  (the R data files) and section 8.
- `feature/interim-normatives/frontend` (Akim, from `develop` after the backend feature is
  merged, or from the backend branch if it is still open): section 6.
- `feature/interim-normatives-phase1b-data/backend` (Akim, from `develop` after the backend
  feature is merged): task 7.5, the data phase 1b needs. It merges on its own; the change is
  archived when all three features are merged.

Spec work (section 1, tasks 9.4-9.5) is committed directly to `develop`. Section 7 is a
working process with the verifier; its data commits go to the branch that owns each task. Checkboxes are ticked in `develop` as tasks are done on the feature branches.

Code journal: `docs/akim/reports/interim-normatives-source-code-journal.md` (untracked, Akim's
zone), created before task 2.1.

Order: 1 → 2 → 3 → 4 → 5 → 6. Section 7 starts after task 2.2, so the schema exists, and runs
in parallel with 3-6. Task 8.1 needs 3, 5 and the R portions of 7 (7.1-7.4) plus open
question 1 of `design.md` (the tolerances of `ex1`). Task 7.5 (phase-1b data) is on its own
feature and does not gate the backend feature or section 8.

## 1. Spec readiness

- [x] 1.1 (spec) Run `openspec validate interim-normatives-source --strict` and
  `openspec validate --all --strict`; verify: both pass (2026-10-20, 21/21)
- [x] 1.2 (spec) Run `spec-reviewer` on this change until a report on the current version
  lists no blocker and no major finding; verify: the passes are recorded in
  `docs/decisions/backend/2026-10-20-interim-normatives-source-readiness.md` and its `-rus`
  version (2026-10-20: pass 2, 0 blockers, 0 major)
- [x] 1.3 (spec) Run `norm-traceability-checker`; verify: it confirms that no requirement
  fixes a norm value and that every norm reference is marked as data or `unverified`; recorded
  in the readiness file (2026-10-20: no norm value, 4 attribution minors fixed)
- [ ] 1.4 (spec) After `backend-layered-architecture`, `calculation-api` and
  `normative-catalog-backend` are archived, add MODIFIED deltas of "No hardcoding",
  "Engineer-set parameters stored in YAML", "Calculation parameter source" and "Catalog
  parameter source" that name the exception of "Scoped exception to the normative-database
  rule", or remove that requirement if the interim source is already gone (`design.md`,
  decision 9); verify: `openspec validate --all --strict` passes and OpenSpec reports no
  archive refusal for the deltas
- [x] 1.5 (spec) Get Egor's acknowledgement of this change as the second developer, with a
  look at the record format against the `catalog_read` rows (`design.md`, open question 5);
  verify: a commit or comment by Egor that names this change (2026-10-20: `7f394e4`, items
  1-3 acknowledged, 4a and 4b "Yes", in `docs/decisions/backend/2026-10-20-interim-normatives-source-ack-to-egor.md`)

## 2. Schema and data format (feature `interim-normatives/backend`)

- [x] 2.1 Add the Pydantic models of the manifest, the five record kinds and the verification
  record in `backend/app/parameters/interim_schemas.py`, every model with
  `extra="forbid"` and the length limits of `design.md` decision 2 (decisions 1-3); verify:
  tests of the scenarios "Record without a reference rejected", "Unknown field rejected" and
  "Over-long label rejected" (`interim-normatives` "Interim normative data files") (2026-10-21, `213b58d` on `feature/interim-normatives/backend`)
- [x] 2.2 Add the loader: resolve the root, read only manifests and type files directly under
  each document directory with `yaml.safe_load`, skip and log links outside the root and other
  files, validate, and report unknown types (`design.md`, decisions 1, 5; non-functional);
  verify: tests of the scenarios "File of an unregistered type", "File outside the root
  ignored" and "No data value in the log" (2026-10-21, `58caf4b` on `feature/interim-normatives/backend`)
- [x] 2.3 Validate verification records: the fields that `human-verified` requires, `by` in
  the manifest's `verifiers`, and `value_digest` against the record's canonical serialization,
  a mismatch counting as `pending` with a startup log line, and the startup warning of
  unchecked records under `strict` (`design.md`, decisions 3, 4); verify: tests of the
  scenarios "Verified record without its fields rejected", "Rejected record without its
  reason rejected", "Changed value needs a new check", "Pending record allowed without a
  verifier" and "Strict lists unchecked values at startup" (2026-10-21, `abc8a7f` on `feature/interim-normatives/backend`)
- [x] 2.4 Compute the data digest per document directory with `canonical_json`
  (`backend/app/engine/hashing.py:29-47`) over the validated content in path order
  (`design.md`, decision 6); verify: tests of the scenarios "Digest is deterministic" (a
  change of comments, key order and indentation only) and "Digest follows the data" (2026-10-21, `8878e71` on `feature/interim-normatives/backend`)
- [x] 2.5 Check the sunset at startup (`design.md`, decision 8); verify: tests of the
  scenarios "Date passed" and "Date not passed" on a fixture manifest with a fixed clock (the
  failing-after-date assertion is proved on the fixture); the test on the real manifest, the
  live reminder, is added by task 7.1 (2026-10-21, `97d1e71` on `feature/interim-normatives/backend`)

## 3. Source and contract tests (feature `interim-normatives/backend`)

- [x] 3.1 Move the assembly functions of `backend/app/services/catalog_source.py` (binding,
  formula, threshold, table value, row selection, bounds) into
  `backend/app/services/parameter_assembly.py`, used by the catalog source (`design.md`,
  decision 5); verify: every existing catalog test passes unchanged and `lint-imports` keeps
  the layer contracts (2026-10-21, `9fb5853` on `feature/interim-normatives/backend`)
- [x] 3.2 Add the optional `source` field (`ParameterSourceInfo`) to `ResolvedParameters` and
  set it in the catalog source; verify: existing callers and test doubles unchanged, a test
  that the catalog source returns kind `catalog` (2026-10-21, `1df10ca` on `feature/interim-normatives/backend`)
- [x] 3.3 Add `InterimParameterSource` and `interim_sources(...)`: records → row records →
  shared assembly, with the profile filter (`strict`, `draft`, `rejected` never used) and the
  log line that names type and parameter (`design.md`, decisions 4, 5); verify: tests of the
  scenarios "Strict refuses an unchecked value on request", "Draft uses pending values and
  marks the result" and "References not raised" (2026-10-21, `00c765b` on `feature/interim-normatives/backend`)
- [x] 3.4 Build one contract test battery parametrized over both sources, from the
  assertions of `backend/tests/test_services_catalog_source.py:59-157` and the data of
  `backend/tests/catalog_fixture.py`, with the same data written as interim files; catalog-only
  tests (SQL statements, connection errors) stay where they are; verify: the scenarios "Same
  data, same parameters", "Table row chosen by an input", "Input off every table row", "Input
  outside the method range" and "Broken binding" pass for both sources (2026-10-21, `270b1ca` on `feature/interim-normatives/backend`)

## 4. Settings and `.env.example` (feature `interim-normatives/backend`)

- [x] 4.1 Add the settings class with `DEC_PARAMETER_SOURCE`, `DEC_INTERIM_PROFILE` and
  `DEC_INTERIM_ROOT` in `backend/app/core/config.py`, and choose `catalog_sources` or
  `interim_sources` in `create_app` (`backend/app/main.py:67-78`), the `sources` argument
  keeping priority (`design.md`, decision 7); verify: tests of the scenarios "Default stays
  the catalog", "Interim chosen", "Catalog mode and a type with interim data only", "Unknown
  setting value", "Catalog setting ignores interim files" and "Interim mode and a type without
  a catalog source" (2026-10-21, `52ad2a6` on `feature/interim-normatives/backend`)
- [x] 4.2 List the three variables in `.env.example`, commented out with a one-line comment
  each; verify: `pre-commit run --all-files` passes, including the settings hook (2026-10-21, `52ad2a6` on `feature/interim-normatives/backend`)
- [x] 4.3 Keep the engineer-set loader unchanged; verify: the existing test that a formula or
  coefficient under `params/` is rejected still passes ("Norm value in params still rejected") (2026-10-21, `b1839c7` on `feature/interim-normatives/backend`)

## 5. Envelope and report (feature `interim-normatives/backend`)

- [x] 5.1 Add the optional `parameter_source` to `ResultEnvelope` and set it in the service
  from `ResolvedParameters.source` (`backend/app/services/calculation.py:77-123`); the engine
  and `input_hash` unchanged (`design.md`, decision 13); verify: tests of the scenarios "New
  interim result", "New catalog result", "Same inputs, same hash across sources", "Source
  without a description" and "Stored result without the field" (`calculation-api`), and
  "Digest in the result" (`interim-normatives`)
- [x] 5.2 Print the source line in the report: in the conclusion before the responsibility
  sentence while `ACCOUNTABILITY_SECTION` is off, in section 4 when it is on
  (`backend/app/reporting/docx_writer.py:53`, `:234-237`); verify: tests of the scenarios
  "Interim line in the conclusion", "Line printed once" and "Older result", with the flag in
  both states
- [x] 5.3 Run `backend/check.sh`; verify: it passes with branch coverage of `app` at 100% or
  at least 95%

## 6. Result screen (feature `interim-normatives/frontend`)

- [x] 6.1 Regenerate `frontend/src/api/schema.d.ts` with `npm run gen:api` after section 5;
  verify: `npm run gen:api:check` passes
- [x] 6.2 Show the source label in the stamp's description list
  (`frontend/src/components/VerdictStamp.tsx:110-138`) and in the refusal view, with Russian
  and English texts, the first 12 hex characters of the digest shown and the full digest as
  screen-reader text, and `draft` marked in words; update the mock fixtures with both kinds;
  verify: tests of the scenarios "Interim result labelled", "Draft marked in words",
  "Refusal labelled" and "Older result without the field", and the axe helper on the result
  screen in both kinds
- [x] 6.3 Run `frontend/check.sh` and the Playwright suite; verify: both pass, branch
  coverage at least 95%

## 7. Digitization with the verifier (working process, data on the branch that owns each task)

- [ ] 7.1 Write the manifest of the norm document with its edition as printed on the source
  text (status `unverified`), the sunset date and event, and the verifiers (`design.md`, open
  questions 3, 4, which must be answered before this task starts), and add the sunset test
  on the real manifest; verify: the loader accepts it, and the test passes before the date
- [ ] 7.2a Extract the pilot's R data (`design.md`, decision 11: the formula of R with its
  coefficients and tables, the threshold rule of `k_z`, the method bounds, the check) from the
  text layer; verify: every element is listed with its page in the working session's record
- [ ] 7.2b Extract the same data independently from page images, without seeing 7.2a; verify:
  every element is listed with its page in a second record
- [ ] 7.2c Compare 7.2a and 7.2b automatically (cell by cell and token by token; formulas by
  numeric equivalence on random inputs) and write every record as `pending` with its `page`;
  verify: the comparison report lists every element as match, difference or image-only, and
  the loader accepts the file in the `draft` profile
- [ ] 7.3a Portion P1: the verifier checks the formulas, their coefficients, their control
  points and the edition, and answers whether amendment 5 changed formula (5.7) (identifier
  given by Akim, checked by the verifier); each check is recorded in the record and committed
  with the portion id (`design.md`, decisions 3, 10); verify: every P1 record is
  `human-verified` or `rejected` with all its fields, and the answer on formula (5.7) is
  recorded in the readiness file
- [ ] 7.3b Portion P2: the verifier checks the tables and their control points, discrepancies
  first; verify: every P2 record is `human-verified` or `rejected` with all its fields
- [ ] 7.3c Portion P3: the verifier checks the threshold rule, the method bounds, the check's
  reference and the control points of `ex1`; verify: every P3 record is `human-verified` or
  `rejected` with all its fields
- [ ] 7.4 Re-check every correction (portion P4); verify: no R record is `pending` or
  `rejected`, and the `strict` startup warning lists no R record
- [ ] 7.5 (feature `interim-normatives-phase1b-data/backend`) Extract and check the data that
  phase 1b needs (`design.md`, decision 11) into the file of its future type, by the same
  protocol, with its own portion ids (P1b for formulas and limits, P2b for re-checks) and a
  listed verifier (`design.md`, open question 3), every record `human-verified` at the end; verify: the file validates and is
  skipped as an unregistered type ("File of an unregistered type"), and `backend/check.sh`
  passes

Deferred portion D-1 (Akim, 2026-10-27): the checks of six records that the pilot's type file
does not hold (the cap d_b = 2 m, the h_n allowances, b = √A, note 5 on d_1 > d, formula
(5.8) and k = 1.1 for characteristics taken from appendix A) and their control points
CP-D1-1, CP-K-2, CP-RULE-1 and CP-RULE-2 are not part of tasks 7.3a-7.4 and gate no feature
of this change. The type file has no rule record and no categorical selector for `k`, and the
pilot takes `d_1` as an input (`design.md`, decision 11). They move to the change that adds
structured inputs (C2); if phase 1b needs formula (5.8), it moves to task 7.5. The sheet
`docs/verification/interim-normatives-source/D-1.yaml` stays unsigned until then.

## 8. Integration test `ex1` (feature `interim-normatives/backend`)

- [ ] 8.1 Add a backend test that runs reference example `ex1`
  (`docs/decisions/reference-examples-foundations.md:103-135`) through `POST /calculations`
  and `POST /calculations/{result_id}/report` with `DEC_PARAMETER_SOURCE=interim` and the
  `strict` profile on the real interim data; verify: the result has kind `interim`, profile
  `strict` and the data digest, R lies within the tolerance the verifier set (design open
  question 1), and the report holds the source line; if the verifier answers in 7.3a that
  amendment 5 changes formula (5.7) (identifier given by Akim, checked by the verifier), the
  test records `ex1` as a control point and names that answer

## 9. Verify and close

- [ ] 9.1 `tester` GO for `feature/interim-normatives/backend`; verify: the verdict with the
  test count and the coverage is recorded in the readiness file
- [ ] 9.2 `tester` GO and `ui-ux-tester` confirmation for
  `feature/interim-normatives/frontend`; verify: both recorded in the readiness file
- [ ] 9.3 Review of each feature by the `orchestrator` or Egor, then the merge into `develop`
  with Akim's word; verify: the reviews are recorded with no open blocker or major finding,
  and `develop` passes both `check.sh`
- [ ] 9.3a `tester` GO, review and merge of `feature/interim-normatives-phase1b-data/backend`;
  verify: recorded in the readiness file
- [ ] 9.4 (spec) Record in the plan file and in Akim's PM record that the interim base is in
  use, with the oral consent of 2026-10-18 (`design.md`, decision 9, open question 6); verify:
  the dated line exists
- [ ] 9.5 (spec) `spec-keeper` syncs the deltas into `openspec/specs/` and archives this
  change after all three features are merged and task 1.4 is resolved; verify:
  `openspec validate --all --strict` passes after the archive

## Requirement coverage

| Requirement | Verified by |
|---|---|
| `interim-normatives` Interim normative data files | tasks 2.1, 2.2 |
| `interim-normatives` Verification record | task 2.3 (process part: 7.3a-7.3c, 7.4) |
| `interim-normatives` Interim source profiles | tasks 3.3, 2.3 (startup warning) |
| `interim-normatives` Interim parameter source contract | task 3.4 |
| `interim-normatives` Interim data digest | tasks 2.4, 5.1 |
| `interim-normatives` Parameter source selection | tasks 4.1, 4.2 |
| `interim-normatives` Interim source sunset | tasks 2.5, 7.1 |
| `interim-normatives` Scoped exception to the normative-database rule | tasks 4.1, 4.3, 1.4 |
| `interim-normatives` Non-functional — interim source | tasks 2.2, 5.3, 6.3 |
| `calculation-api` Parameter source in the result envelope | task 5.1 |
| `report-generator` Parameter source line in the report | task 5.2 |
| `transparent-output` Parameter source label on the result screen | task 6.2 |

## Dependencies

- `backend-layered-architecture`, `calculation-api` and `normative-catalog-backend` (not
  archived) hold the four requirements this change bounds; task 1.4 waits for their archive.
- `calculation-core-contract` and `calculation-api` (not archived) own the envelope; this
  change adds an optional field next to them.
- `frontend-app` is merged; section 6 builds on its result screen.
- Reference example `ex1` needs its tolerances from the verifier (`design.md`, open question 1)
  before task 8.1.
- No dependency on Egor's zones; Egor's acknowledgement (task 1.5) is part of the DOR.
- Task 7.1 needs the verifier's name and the sunset date (`design.md`, open questions 3, 4);
  sections 2-6 do not, since task 2.5 tests the sunset on a fixture manifest.

## DOR checklist

- [x] `proposal.md` (with "Non-goals"), `specs/…`, `design.md`, `tasks.md` exist
- [x] `openspec validate --strict` passes and a `spec-reviewer` report on the current version
  lists no blocker and no major finding (tasks 1.1, 1.2)
- [x] Functional requirements and scenarios recorded; each requirement is mapped to tasks
- [x] Non-functional requirements recorded (`design.md` and the requirement "Non-functional —
  interim source": security, performance, coverage, accessibility)
- [x] Each task fits one session and names how it is verified; every task with code belongs
  to one feature
- [x] Acceptance and Go/No-Go criteria written (below)
- [x] Feature branches named
- [x] Dependencies satisfied: Egor's acknowledgement (task 1.5, `7f394e4`). The verifier's name and the
  sunset date are not DOR items: they are needed only by task 7.1 (Akim, 2026-10-20)

## DOD and Go/No-Go

- **GO for `feature/interim-normatives/backend`:**
  - sections 2-5 and 8 done, and the R portions of section 7 (7.1-7.4) committed;
  - `backend/check.sh` passes with branch coverage at least 95%;
  - `pre-commit run --all-files` passes;
  - the contract battery passes for both sources;
  - `ex1` passes through the API and the report in the `strict` profile (task 8.1).
- **GO for `feature/interim-normatives/frontend`:**
  - section 6 done;
  - `frontend/check.sh` and Playwright pass with branch coverage at least 95%;
  - `ui-ux-tester` confirms the label (text, not colour alone; axe clean).
- **GO for `feature/interim-normatives-phase1b-data/backend`:** task 7.5 done; every record
  of the file `human-verified`; `backend/check.sh` passes.
- **NO-GO:**
  - any failing test;
  - coverage below 95%;
  - a norm value in a spec or in code;
  - a record set to `human-verified` by an agent or without its fields;
  - a reference whose status the source raised;
  - a `strict` result computed from a `pending` or `rejected` record;
  - a result from interim data without its source label;
  - an unvalidated OpenSpec artifact.
- **Archive:** all three features merged with their GO, task 1.4 resolved, specs synced.
