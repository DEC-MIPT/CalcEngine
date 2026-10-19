# `interim-normatives-source`: readiness record, 2026-10-20

- Owner: Akim (backend and frontend zones). No part of the change is in Egor's zones.
- Russian version: `2026-10-20-interim-normatives-source-readiness-rus.md`.
- Phase 1 (CH1) of Akim's plan for the second-limit-state calculation of shallow foundations:
  a temporary source of norm-given parameters in Akim's zone, read through `ParameterSource`.

## Verdict

**Spec review criterion met (2026-10-20); DOR not yet met.**
- `openspec validate interim-normatives-source --strict` passes, and so does
  `openspec validate --all --strict` (21/21).
- The second `spec-reviewer` pass lists no blocker and no major finding.
- `norm-traceability-checker` finds no norm value in the change.

DOR still needs:
- Egor's acknowledgement (task 1.5);
- the verifier's name and the sunset date, before task 7.1 (`design.md`, open questions 3
  and 4).

## Akim's decisions (2026-10-19)

1. **Verifier's mark.** The verifier's mark is a separate verification record, used as the
   gate of the `strict` profile. `NormRef` stays `unverified` / `machine-extracted` until
   WP3, so `calculation-core-contract` and `normative-catalog-backend` are not changed.
2. **Data format.** YAML records repeat the `catalog_read` rows. The assembly code is shared,
   so both sources yield the same parameter objects.
3. **Where the verification record lives.** It sits next to its value. An edited value falls
   back to `pending` through `value_digest`.
4. **What `strict` does.** It refuses on request: `503 parameter_source_unavailable`, with
   the parameter named in the log. A broken file stops startup.
5. **Sunset.** It is a date plus an event. After the date, startup logs a warning and a
   backend test fails on purpose.
6. **Data scope.** The pilot's R data gate the change (`ex1` in `strict`). The phase-1b data
   form a separate portion on a third feature.
7. **Exception to decision 3 of `backend-layered-architecture`.** It is decided after a trial
   validate. A trial MODIFIED delta of "No hardcoding" passes `openspec validate --strict`,
   but OpenSpec notes "Archive would refuse this delta: backend-architecture: target spec does
   not exist". So the exception is an ADDED requirement that names the four requirements it
   bounds:
   - "No hardcoding" and "Engineer-set parameters stored in YAML" (`backend-layered-architecture`);
   - "Calculation parameter source" (`calculation-api`);
   - "Catalog parameter source" (`normative-catalog-backend`).

   Task 1.4 adds the MODIFIED deltas once those changes are archived.
8. **Agreement.** Egor and the PM agreed orally to the interim base on 2026-10-18 (Akim's
   words). This is recorded as one line in `design.md`, with no question round.

## `spec-reviewer`

| Pass | Blocker | Major | Minor | Result |
|---|---|---|---|---|
| 1 | 0 | 4 | 8 | NOT READY |
| 2 | 0 | 0 | 8 | READY (spec-reviewer criterion) |

Pass 1 majors and their fixes:

- **Major 1: the catalog-only rule was bounded in only one change.** The exception bounded
  only the `backend-architecture` requirements. `calculation-api` "Calculation parameter
  source" and `normative-catalog-backend` "Catalog parameter source" state the same rule.
  - Fixed: all four requirements are named in the exception requirement, the proposal,
    design decision 9 and task 1.4.
  - Two scenarios were added: "Interim mode and a type without a catalog source" and
    "Catalog mode and a type with interim data only".
- **Major 2: task 7.5 sat on the backend branch without gating it.** The phase-1b data were
  on the backend branch but did not gate its merge.
  - Fixed: task 7.5 is a third feature, `feature/interim-normatives-phase1b-data/backend`,
    with its own GO (task 9.3a).
  - The change is archived after all three features are merged.
- **Major 3: "always carries the field" did not hold.** The envelope field was said to be
  always present, while the source description is optional.
  - Fixed: the field is present whenever the source describes itself, which both new sources
    do.
  - A scenario was added: "Source without a description".
- **Major 4: per-type promise versus a global switch.** The text promised that each type
  could move back separately, but the switch is global.
  - Fixed: the selection is stated as global.
  - A per-type choice is a Non-goal and open question 7.

Pass 1 minors, all fixed:
- the "References not raised" scenario is limited to the envelope (the first-iteration
  settings hide the status on the screen and in the report);
- label limits are given in numbers;
- every task's verify clause names its scenarios by title;
- the sunset logic is tested on a fixture manifest, with the real-manifest test in task 7.1;
- record kinds and fields are listed in the spec;
- the report line extends "Result accountability block" when that section is on;
- rules and a scenario were added for `rejected` records;
- citation ranges were unified;
- untracked analysis is no longer cited as rationale.

Pass 2 minors, all fixed:
- the heading of section 7 is reworded;
- tasks 7.2 and 7.3 are split per extraction and per portion (7.2a-c, 7.3a-c);
- portions and a verifier are named for task 7.5;
- the label limits are restated in the spec, and it is said what is measured inside a tree;
- the last untracked citation is removed;
- "a type needs no registration beyond its entries in `PARAMETER_MODELS` and
  `TABLE_SELECTORS`";
- the open questions are reordered;
- the sunset scenario is tied to the fixture test.

## `norm-traceability-checker`

- Blocker 0, major 0, minor 4. No requirement fixes a norm value, and nothing is cited from
  memory.
- The minors were attributions, all fixed:
  - the document is named by the author, edition `unverified`;
  - the claim about which edition the `ex1` textbook follows is attributed to the author and
    marked `unverified`;
  - "identifier given by Akim, checked by the verifier" is repeated at every use of formula
    (5.7).
- The checker notes that editions of СП 22.13330.2016 differ across the repository: "2016" in
  most changes, and "2016 с Изм. N 1, 2, 3, 4, 5" in `frontend-app` `tasks.md`. This change
  takes the edition as printed on the source text, marked `unverified`, and the verifier
  records it in portion P1.

## Open before DOR

| Item | Who |
|---|---|
| Acknowledgement of this change as the second developer, and a look at the record format against `catalog_read` (task 1.5) | Egor |
| The verifier's name and the sunset date (`design.md`, open questions 3, 4), before task 7.1 | Akim |
| The PM's dated record that norm values may be kept in git for the pilot (open question 6, task 9.4) | PM, recorded by Akim |
| Tolerances of `ex1`, and whether amendment 5 changes formula (5.7) (identifier given by Akim) (open questions 1, 2); needed for task 8.1, not for DOR | verifier |
