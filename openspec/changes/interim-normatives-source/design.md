# Design

## Context

- **The read path today.** A calculation type gets its norm-given parameters from a
  `ParameterSource`. It is a `Protocol` with one method,
  `resolve(calculation_type, inputs) -> ResolvedParameters(parameters, method_range)`
  (`backend/app/services/parameter_source.py:8-32`).
  - The only implementation is `CatalogParameterSource`
    (`backend/app/services/catalog_source.py:259-401`). It reads five `catalog_read` views
    into the row records `FormulaRow`, `TableValueRow`, `ThresholdRow`, `CheckRow` and
    `MethodBoundRow` (`backend/app/schemas/normatives.py:11-70`).
  - It assembles them with `_check_binding`, `_formula`, `_threshold`, `_table_value`,
    `_selected` and `_bound` (`catalog_source.py:90-256`) into the type's parameter model,
    for example `foundations_shallow_r.Parameters` (`backend/app/engine/foundations_shallow_r.py:105-126`).
  - A breach of the data contract becomes `ParameterSourceUnavailableError`, which answers
    `503 parameter_source_unavailable` (`catalog_source.py:319-343`;
    `backend/app/api/errors.py:30`).
- **Wiring.** `create_app` builds one source per registered type with `catalog_sources(...)`,
  unless a test passes `sources` (`backend/app/main.py:67-78`;
  `catalog_source.py:404-426`). No setting chooses the source today.
  - Settings are split into classes (`backend/app/core/config.py:11-43`). The pre-commit hook
    checks that `.env.example` lists every field of every `BaseSettings` class
    (`backend/scripts/check_env_example.py:66-119`; `.pre-commit-config.yaml:10-17`).
- **Result.** The engine returns a `CalculationResult` (`backend/app/engine/result.py:128-140`).
  The service turns it into a `ResultEnvelope` by adding `result_id`
  (`backend/app/services/calculation.py:77-86`), and `submit` resolves the parameters before
  running the engine (`calculation.py:111-123`). The envelope carries no source description
  (`backend/app/schemas/calculation.py:420-485`).
- **Parameter-set identity.** It is the SHA-256 of the canonical JSON of the parameter values
  (`backend/app/engine/hashing.py:29-65`), so it does not depend on which source supplied
  them.
- **Report.** Section 4, "Подотчётность результата", is off (`ACCOUNTABILITY_SECTION = False`,
  `backend/app/reporting/docx_writer.py:53`), and the engineer-responsibility sentence is
  printed after the conclusion lines (`docx_writer.py:234-237`).
- **Result screen.** It shows the engine version in the stamp's description list
  (`frontend/src/components/VerdictStamp.tsx:110-138`).
- **The rule this change bounds.** It appears in four requirements. Decision 3 of
  `backend-layered-architecture`
  (`openspec/changes/backend-layered-architecture/design.md:104-129`) says: "Formulas and
  coefficients the norm does give do not go in `params/**/*.yaml`; they come from
  `dec_normatives` through the `parameters` layer's `provenance` gate". Its spec records it
  as "No hardcoding" and "Engineer-set parameters stored in YAML"
  (`specs/backend-architecture/spec.md:63-93`). `calculation-api` "Calculation parameter
  source" says the system "SHALL NOT take a norm-given value from code, from a `.yaml` file,
  or from the client" (`openspec/changes/calculation-api/specs/calculation-api/spec.md:231-262`),
  and `normative-catalog-backend` "Catalog parameter source" resolves "every registered
  calculation type from the catalog contract"
  (`openspec/changes/normative-catalog-backend/specs/normatives-catalog/spec.md:208-217`).
- **Reference status.** For the MVP the parameters layer does not reject `machine-extracted`
  values; every step built from them is shown as unverified
  (`openspec/changes/calculation-core-contract/design.md:338-363`). The backend never raises a
  reference's status (`openspec/changes/normative-catalog-backend/specs/normatives-catalog/spec.md:193-194`).
  A `NormRef` that is `machine-extracted` is always `unverified`
  (`backend/app/schemas/calculation.py:92-121`).
- **Prior analysis.** Akim's feasibility study of the interim base (untracked, so not a
  source of rationale here) compared four stores: YAML in `params/`, YAML in Akim's zone
  outside `params/`, a separate database, and a copy of Egor's schema. This design takes the
  second for the reasons given in decisions 1 and 2, and restates the extraction protocol and
  the verifier's portions in decision 11.

## Decisions

1. **Data directory: `backend/interim_normatives/<document>/`.**
   - It is in the backend zone and outside `params/`, so the engineer-set loader and its
     test of "no norm values in `params/`" stay as they are. It is outside `backend/app/`,
     because data are not code. It is not under `ml/` or `infra/`, which are Egor's zone.
   - `<document>` is a slug of the norm document. The first one is the document the pilot
     cites, named by the author as СП 22.13330.2016 (its edition `unverified` until checked
     against the source text). Each document directory holds:
     - `manifest.yaml`: document, edition as printed on the consolidated text (status
       `unverified`), `sunset` (decision 8), and `verifiers`, the names allowed to set
       `human-verified` (decision 10);
     - one `<calculation-type>.yaml` per calculation type, named as the type in the registry.
   - The root defaults to `backend/interim_normatives` and can be moved with
     `DEC_INTERIM_ROOT` (decision 7).

2. **Records repeat the catalog rows.**
   - A type file has five lists: `formulas`, `table_values`, `thresholds`, `checks` and
     `method_bounds`. Their fields are those of the row records
     (`backend/app/schemas/normatives.py:11-70`):
     - formulas: `parameter`, `result_symbol`, `latex`, `tree`, `units`;
     - table values: `parameter`, `symbol`, `latex`, `value`, `unit` and the optional heading
       fields;
     - thresholds: `parameter`, `latex`, `value`, `unit`;
     - checks: `parameter`;
     - method bounds: `quantity`, `kind`, `value`, `unit`, `inclusive`.
   - Every record also has `norm_refs` (one or more full `NormRef` objects), `page` (the page
     of the consolidated text the value was read from) and `verification` (decision 3).
   - The schema lives in the `parameters` layer (`backend/app/parameters/interim_schemas.py`,
     after the pattern of `backend/app/parameters/param_schemas.py:7-48`). Every model has
     `extra="forbid"`, and labels are length-limited.
   - There is no field for norm text. A file is read with `yaml.safe_load`, as the existing
     loader does (`backend/app/parameters/loader.py:10-40`).
   - Length limits, counted in Unicode code points: `latex` at most 500, and every symbol
     name and function name inside a `tree` at most 64 (the tree's size is bounded by the
     parser of the catalog path, which both sources share);
     `parameter`, `symbol`, `result_symbol`, `quantity`, unit symbols, `by` and `portion` at
     most 64; `comment` at most 300; manifest `document`, `edition` and `sunset.event` at most
     200. They hold LaTeX and identifiers, not passages of a norm. These are layout choices of
     this design, not norm values.
   - Why rows and not a grid of the norm's tables: the source turns records into the same
     row records and runs the same assembly. Selection of a table row, binding checks, unit
     checks and expression parsing are then one code path for both sources, and CH3 can
     compare the two sources record by record.

3. **Verification record next to the value.**
   - Each record carries `verification`, with these fields:
     - `status`: `pending`, `human-verified` or `rejected`;
     - `by`, `at` (a date), `portion` (the verifier's portion id) and `comment`;
     - `value_digest`: the SHA-256 of the record's canonical JSON without its `verification`,
       taken when the verifier set the status.
   - `human-verified` requires `by` (a name listed in the manifest's `verifiers`), `at`,
     `portion`, `value_digest` and a `page` on the record. `rejected` requires `by` (listed),
     `at` and a `comment` with the reason. A record that lacks any of them fails validation.
   - A `human-verified` record whose current `value_digest` differs from the recorded one is
     treated as `pending`. So a value edited after its check needs a new check, and nobody
     has to remember to reset the status. The loader reports such records at startup.

4. **Profiles gate on the verification record, not on the reference status.**
   - The `strict` profile, the default, uses a record only if it is `human-verified`.
   - The `draft` profile, set only explicitly, also uses `pending` records. It is for
     development and digitization.
   - A `rejected` record is never used.
   - In both profiles each `NormRef` reaches the result unchanged. The data store references
     as `unverified` / `machine-extracted`, as the catalog does until WP3, so the envelope's
     `norm_refs` and step references stay `unverified` even when the data passed the verifier.
     Whether the screen and the report print that status depends on the first-iteration
     settings of `frontend-app` (decision 12 there); this change does not alter them.
   - This keeps the rules of `calculation-core-contract` and `normative-catalog-backend`
     unchanged. What the verifier's mark means for a reference's status is left to WP3
     (`norm-source-traceability`).
   - Profiles have no meaning for the catalog source.

5. **`InterimParameterSource` reuses the catalog assembly.**
   - The assembly functions move from `catalog_source.py` into a module both sources import
     (`backend/app/services/parameter_assembly.py`). The catalog source keeps its repository
     calls and its error mapping, and its tests stay green unchanged.
   - `InterimParameterSource` loads all files once at startup. Per request it builds the row
     records of the type, removes records its profile may not use, and calls the shared
     assembly. It uses the same per-type parameter models and table selectors as the catalog
     source (`PARAMETER_MODELS`, `TABLE_SELECTORS`, `backend/app/services/catalog.py:51-68`),
     so a type needs no registration beyond its entries in those two tables to read interim
     data.
   - A parameter that has no usable record, because it is missing, `pending` under `strict`
     or `rejected`, breaks the binding. The answer is then
     `ParameterSourceUnavailableError` (`503 parameter_source_unavailable`), and one log line
     names the type and the parameter, as `catalog_data_invalid` does
     (`catalog_source.py:338-343`).
   - A type without a data file gets no interim source and answers
     `503 parameter_source_unavailable` through the existing path (`calculation.py:111-116`).
   - A data file of a type that is not registered is validated and skipped with one log line.
     The phase-1b data portion can then exist before its type does.
   - **Minimal contract change.** `ResolvedParameters` gains an optional
     `source: ParameterSourceInfo | None = None`. The `Protocol` itself and every existing
     caller stay as they are. Both sources of this change always set it; a source that does
     not (a test double) yields an envelope without `parameter_source`.

6. **Data digest.**
   - At startup the source computes one SHA-256 per document directory. It takes the
     validated manifest and type files as Python data, ordered by their path relative to the
     document directory, and serializes them with `canonical_json`
     (`backend/app/engine/hashing.py:29-47`: sorted keys, fixed separators, UTF-8).
   - The digest covers every value, reference, page and verification record. It does not
     depend on YAML comments, key order or whitespace.
   - Floats are serialized the way the engine's hash does. A value written as `1.0` and as
     `1` therefore has one digest when the schema types it as a float.

7. **Selection by setting.**
   - A new settings class in `backend/app/core/config.py` holds three variables:
     - `DEC_PARAMETER_SOURCE`: `catalog`, the default, or `interim`;
     - `DEC_INTERIM_PROFILE`: `strict`, the default, or `draft`;
     - `DEC_INTERIM_ROOT`: optional.
   - Any other value of the first two fails at startup.
   - `create_app` builds `catalog_sources(...)` or `interim_sources(...)` accordingly. The
     `sources` argument of tests keeps priority.
   - The setting is global: it switches every calculation type at once. In `catalog` mode a
     type that has interim data but no catalog data answers
     `503 parameter_source_unavailable`, as any type without usable catalog data does.
   - The normative search and document endpoints keep reading the catalog whatever the
     setting.
   - `.env.example` lists the three variables commented out, so the pre-commit hook passes.

8. **Sunset: a date and an event.**
   - The manifest's `sunset` has a `date` and an `event` in words, for example "the type is
     switched to the catalog in CH3". The author writes both.
   - When the interim source is selected and the date has passed, startup logs a warning that
     names the document, the date and the event.
   - A backend test fails after the date, so `backend/check.sh` asks for a decision: extend
     the date by a commit, or remove the data. This failing test is intended (Akim's choice,
     2026-10-19): it is the reminder. Until the real manifest exists (task 7.1), the sunset
     logic is tested with a fixture manifest.
   - The event closes the source by a task of the change that switches the service back to
     the catalog (CH3). That task deletes the data directory after the cross-check.

9. **Scoped, temporary exception to the catalog-only rule.**
   - Norm-given formulas, coefficients, thresholds, checks and method bounds may be read from
     YAML only if all of the following hold:
     - `DEC_PARAMETER_SOURCE=interim`;
     - only from the directory of decision 1;
     - only in records that carry `norm_refs`, `page` and a verification record;
     - only until the sunset event of decision 8.
   - `params/**/*.yaml` keeps rejecting norm values, and the catalog stays the source when
     the setting is `catalog`.
   - It bounds four requirements: "No hardcoding" and "Engineer-set parameters stored in
     YAML" (`backend-layered-architecture`), "Calculation parameter source"
     (`calculation-api`) and "Catalog parameter source" (`normative-catalog-backend`).
   - The exception is an ADDED requirement of `interim-normatives`, not MODIFIED deltas. A
     trial MODIFIED delta of "No hardcoding" passed `openspec validate --strict`, with the
     note "Archive would refuse this delta: backend-architecture: target spec does not exist"
     (run 2026-10-19), and none of the four requirements is in `openspec/specs/` yet. Task 1.4
     adds the MODIFIED deltas, or removes the exception, once those three changes are
     archived.
   - Agreement: Egor and the PM agreed orally to the interim base on 2026-10-18 (Akim's
     words).

10. **Who may set `human-verified`.**
    - Only a person named in `verifiers`, by a commit whose message cites the portion id
      (decision 11, portions). An agent writes records only as `pending` and never edits a
      `verification` block.
    - The schema checks the fields and the name. It cannot check who typed them, so this is
      a process control: it rests on the review of the diff, and it is recorded as a risk.

11. **Digitization is a working process, not product code.**
    - Protocol (restated from Akim's feasibility study):
      1. the text layer;
      2. an independent reading of page images;
      3. automatic comparison, cell by cell and token by token, with formulas compared for
         numeric equivalence on random inputs;
      4. a person checks 100% of the elements, discrepancies first.
    - Portions: P1 the formulas, their coefficients and the edition; P2 and P3 the tables
      and the control points, including `ex1`; P4 the re-check of every correction. Control
      points: two or three input sets per formula, and every branch and boundary of a
      threshold rule, chosen by the verifier.
    - Comparison scripts stay in the working session and do not enter `backend/`.
    - Whether amendment 5 changed formula (5.7) — the identifier is given by Akim and is
      checked by the verifier — is answered in portion P1. Until then `ex1` is a control
      point, not a WP4 gate: by the author's reading, its textbook follows the earlier
      amendments, a claim the verifier checks (`unverified`).
    - The first portion set is the pilot's R: the formula of R with its coefficients and
      tables, the threshold rule of `k_z`, the method bounds and the reference of the check.
      A separate portion holds the data phase 1b needs: the mean unit weight of the
      foundation with the soil above it, the formulas of the edge and corner pressures with
      their limits, and the condition of a trapezoidal pressure diagram. That portion lives on
      its own feature (`feature/interim-normatives-phase1b-data/backend`), does not gate the
      backend feature or `ex1`, and is needed for the DOR of phase 1b.

12. **The C/C++ boundary is unchanged.** The swap boundary of the engine
    (`calculation-engine` "Hot-swap boundary for C/C++") is the calculation function. The
    source runs before it, in the service layer, and adds nothing to the hot path.

13. **Source label.**
    - `ResultEnvelope` gains an optional `parameter_source` with three fields:
      - `kind`: `catalog` or `interim`;
      - `data_sha256`: 64 hex characters for `interim`, `null` for `catalog`;
      - `profile`: `strict` or `draft` for `interim`, `null` for `catalog`.
    - The service sets it from `ResolvedParameters.source` when it builds the envelope
      (`calculation.py:77-86`). The engine does not see it, and `input_hash` does not change.
    - Stored results without the field stay readable: the field is optional with default
      `null`.
    - The result screen shows it in the stamp's description list and in the refusal view: the
      first 12 hex characters of the digest, the full digest as screen-reader text, and a
      `draft` profile in words. A result without the field shows no label.
    - The report prints one line in the conclusion, before the responsibility sentence. While
      section 4 is off, this is the only place it can go (`docx_writer.py:234-237`). When
      section 4 is on, the line moves there and extends the content of
      `calculation-core-contract` "Result accountability block".

## Non-functional requirements

- **Security.**
  - YAML is read with `safe_load`.
  - `DEC_INTERIM_ROOT` is resolved once at startup, and only files directly under a document
    directory are read: no links followed outside the root, no other file types.
  - Labels are length-limited, so a file cannot carry norm text.
  - The digest and the profile are not secret. No data value is written to the log.
- **Performance.** All files load once at startup, and `resolve` works in memory. The latency
  budget of `POST /calculations` (`calculation-api`) is unchanged.
- **Coverage.** Branch coverage of the changed backend code at least 95% (`backend/check.sh`
  holds 100% today). Frontend branch coverage at least 95%.
- **Accessibility.** The label on the result screen is text, not colour alone, and the axe
  check of the screens passes.

## Risks

- **The verifier is the author of the digitization.** The check is not independent.
  Mitigations: two extractions, numeric equivalence of formulas, control points, and
  agreement with the textbook's intermediate values. Pilot materials do not call the data
  "independently verified".
- **Two sources of truth.** Mitigated by the source label on every result, the sunset, and
  CH3, which compares the sources before the move back.
- **Process-only control of `human-verified`** (decision 10).
- **The contract change touches unarchived changes.** The envelope field and the
  `ResolvedParameters` field are additive and optional. `frontend/src/api/schema.d.ts` is
  regenerated in the same feature.
- **Oral agreement only** (decision 9). A dated line here and in Akim's PM record (plan
  phase 9).

## Assumptions

- **Assumption:** the pilot's parameter names, from the fields of
  `foundations_shallow_r.Parameters`, are the binding keys in both sources, so CH3 compares
  without renaming.
- **Assumption:** the `catalog_read` row records do not change before CH3. If Egor extends
  them (categorical selector, interpolation), the interim schema follows in CH2.

## Open questions

| # | Question | Addressee |
|---|---|---|
| 1 | Tolerance of each output of `ex1` and its `tolerance_source` (the card's tolerance cells are empty, `docs/decisions/reference-examples-foundations.md:103-135`) | verifier |
| 2 | Does amendment 5 change formula (5.7) numerically (identifier given by Akim, checked by the verifier), and so is `ex1` a gate or only a control point | verifier |
| 3 | The verifier's name for `verifiers` (today: Akim, see Risks) | Akim |
| 4 | The sunset date | Akim |
| 5 | Acknowledgement of this change as the second developer (shared `openspec/`) and a look at the row format against `catalog_read` | Egor |
| 6 | The PM's dated record that norm values may be kept in git for the pilot (oral consent, 2026-10-18) | PM, recorded by Akim |
| 7 | A per-type source choice, if CH3 switches types one by one | Akim, in CH3 |
