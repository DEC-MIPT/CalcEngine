# Proposal

Owner: Akim (backend and frontend zones). No task of this change is in Egor's zones (`ml/`,
`infra/`, `dec_normatives`). Phase 1 (CH1) of Akim's plan for the second-limit-state
calculation of shallow foundations; not one of WP1-WP9. The parts of that plan and of its
feasibility study this change relies on are restated in `design.md`.

## Why

Every norm-given value of a calculation type comes from Egor's catalog
(`backend/app/services/catalog_source.py:259-401`), and the catalog covers only the pilot's R:
one numeric selector per table, no categorical selector, no interpolation, no sum nodes. The
next blocks of the shallow-foundation calculation (base pressures, stresses, settlement) need
norm data the catalog will not hold for some time, and the calculation work should not wait
for it.

This change adds a second, temporary source of norm-given parameters in Akim's zone. It is
read through the same `ParameterSource` protocol (`backend/app/services/parameter_source.py:24-32`)
and yields the same parameter objects as the catalog, so the engine does not change and the
service can move back to the catalog by one setting, for all calculation types at once. Its data are digitized
from the primary source by a recorded double-extraction protocol, and a profile decides
whether data not yet checked by a person may be used. Each result says which source and
which data it was computed from.

The first slice is the pilot's R: the pilot type `foundations_shallow_r` computed on interim
data, with reference example `ex1` passing through the API and the report in the `strict`
profile.

## What Changes

- **New capability `interim-normatives`**: a data directory in the backend zone, outside
  `params/`, with one manifest per norm document and one file per calculation type; a typed
  schema that rejects unknown fields and records without a `NormRef`; a verification record
  next to each value; two profiles, `strict` and `draft`; a SHA-256 digest of the data over a
  canonical serialization; a sunset date and event; and a scoped, temporary exception to the
  rule that norm-given values come only from the normative database.
- **`InterimParameterSource`**, built from the same row records and the same assembly code as
  `CatalogParameterSource`, and one contract test battery that both sources pass.
- **Source selection by setting** (`DEC_PARAMETER_SOURCE`, `DEC_INTERIM_PROFILE`,
  `DEC_INTERIM_ROOT`), with lines in `.env.example`.
- **Source label in the result**: an optional `parameter_source` object in the result envelope
  (kind, data digest, profile), shown on the result screen and printed in the report's
  conclusion next to the engineer-responsibility sentence, because section 4 of the report is
  off in the pilot's first iteration (`backend/app/reporting/docx_writer.py:53`, `:234-237`).
- **Data**: the pilot's R digitized and checked in full by a verifier; a second, separate
  portion with the data that phase 1b (`foundations-pressure-from-loads`) needs, as a
  continuation on `feature/interim-normatives/backend` by Akim's explicit instruction of
  2026-11-06 (`design.md`, decision 14). Its acceptance is separate from the original
  backend integration recorded in task 9.3.
- **Storage of applicability and diagram conditions**: two optional typed lists preserve
  exact fractional conditions and printed diagram forms for the future type. They use the
  same verification and digest controls as existing records. They are stored and validated;
  a registered type containing them cannot resolve parameters until its executable contract
  is specified in a later change (`design.md`, decision 14).
- Code uses `feature/interim-normatives/backend` and
  `feature/interim-normatives/frontend` (`tasks.md`). The storage-format and phase-1b data
  continuation reuses the existing backend branch; no separate phase-1b branch is created.
  The continuation requires its own tester GO, review and integration gate (task 9.3a).

## Capabilities

### New Capabilities

- `interim-normatives`: the interim data, their validation, verification records, profiles,
  digest, sunset, the source selection and the scoped exception.

### Modified Capabilities

- `transparent-output`: ADDED requirement "Parameter source label on the result screen".
- `report-generator`: ADDED requirement "Parameter source line in the report".
- `calculation-api`: ADDED requirement "Parameter source in the result envelope".

These are ADDED, not modifications, because the requirements they sit next to are still in the
active changes `calculation-core-contract` and `calculation-api`, not in `openspec/specs/`;
they add an optional field and its display and do not contradict them.

The rule that norm-given values come only from the normative catalog is stated in four
requirements of three active changes:
- `backend-layered-architecture`: "No hardcoding" and "Engineer-set parameters stored in
  YAML" (`specs/backend-architecture/spec.md:63-93`; its decision 3, `design.md:104-129`);
- `calculation-api`: "Calculation parameter source" (`specs/calculation-api/spec.md:231-262`);
- `normative-catalog-backend`: "Catalog parameter source"
  (`specs/normatives-catalog/spec.md:208-217`).

A trial MODIFIED delta of "No hardcoding" passes `openspec validate --strict`, but OpenSpec
reports that archive would refuse it, since `backend-architecture` is not in `openspec/specs/`
yet; the other three requirements are likewise not in `openspec/specs/`. The exception is
therefore an ADDED requirement of `interim-normatives` that names the four requirements it
bounds; task 1.4 adds the MODIFIED deltas once those changes are archived (`design.md`,
decision 9).

## Non-goals

- **Norm values in specs or in this change's documents.** Values, coefficients, limits,
  tolerances and clause numbers are data set by the engineer and the verifier, not spec text.
- **Norm texts or PDFs** in the repository or a database: only values, `NormRef`s, page
  numbers and short labels.
- **Raising a `NormRef`'s status.** A value checked by the verifier still reaches the result as
  `unverified` / `machine-extracted`; the verification record is a gate of the `strict`
  profile, not a reference status (`design.md`, decision 4).
- **A product pipeline for digitization.** Extraction and comparison run in working sessions;
  their scripts are not part of the backend.
- **Writing to `dec_normatives` or changing Egor's views**, `ml/`, `infra/` or `params/`.
- **CH2** (data of the settlement blocks), **CH3** (cross-check with the catalog and the move
  back), and **phase 1b** (the type that computes base pressures from loads).
- **New engine mechanisms** (categorical selectors, interpolation, sums), or execution of
  stored applicability and diagram conditions. The five executable record lists continue to
  use the catalog row contract; the two additional lists are storage-only (decision 14).
- **Choosing the source per calculation type.** One setting switches all types; a per-type
  choice is a later change if CH3 needs it.

## Impact

- New: `backend/interim_normatives/` (data), `backend/app/parameters/interim_schemas.py` and a
  loader in the same layer, `backend/app/services/interim_source.py`, a shared assembly module
  extracted from `backend/app/services/catalog_source.py`.
- Changed: `backend/app/services/parameter_source.py` (an optional source description in
  `ResolvedParameters`), `backend/app/services/calculation.py` (the envelope),
  `backend/app/schemas/calculation.py` (the envelope field), `backend/app/core/config.py`,
  `backend/app/main.py`, `backend/app/reporting/` (the conclusion line), `.env.example`,
  `frontend/src/api/schema.d.ts` (regenerated), `frontend/src/components/VerdictStamp.tsx` and
  the refusal view.
- Tests: a contract battery parametrized over both sources, built from
  `backend/tests/test_services_catalog_source.py:59-157` and `backend/tests/catalog_fixture.py`.
- No change of the engine (`backend/app/engine/`), of the catalog views, or of the stored
  results already in `dec_app`: the new envelope field is optional.
