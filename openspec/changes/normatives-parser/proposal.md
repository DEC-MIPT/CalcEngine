# Proposal

## Why

The collector downloads normative documents, but the engine needs the *structure* inside
them: formulas (executable), coefficient tables, clause references, notation, and
applicability bounds. Without it every calculation's parameters are hardcoded — the exact
failure mode of the competitors. This change adds the parser (Track B): deterministic
extraction of structured entities from the downloaded СП, with a human-in-the-loop
verification gate.

## What Changes

- New capability `normatives-parser`: extraction of formulas, tables, clauses, notation,
  applicability bounds, and cross-references.
- New component `normatives-pipeline/parser/` (batch/CLI, no public API): per-type
  adapters (text PDF vs scan); `pdfplumber`/regex baseline + ML fallback (`pix2tex`,
  Table Transformer).
- Formula → executable validation (H6): a throwaway SymPy executor proves extracted
  formulas compute on a control example. Production binding/execution is the engine
  (Akim's zone), out of scope.

## Non-goals

- No production calculation engine (Akim's zone).
- No generative-LLM extraction (deferred).
- No public API.
- No ML in the calculation path.

## Capabilities

### New Capabilities

- `normatives-parser`: structured extraction of calculation-bearing entities.

## Impact

- New code under `normatives-pipeline/parser/` and `ml/` artifacts. No change to Akim's
  engine/backend beyond consuming the extracted schema.
