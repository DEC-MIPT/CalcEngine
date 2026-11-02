---
name: test-process
description: Automated testing process for DEC. Defines pytest/Vitest/Playwright coverage and the >= 95% branch coverage gate. Use when writing or running tests for any change.
---

# Test Process

## Stack

- Backend: `pytest` (unit + integration), coverage via `coverage.py`
- Frontend: `Vitest` + React Testing Library
- E2E: `Playwright`

## Coverage gate

- Target: >= 95% **branch** coverage for the changed code.
- This is a hard gate: below 95% is NO-GO.

## Verdict

- **GO** — all tests pass with >= 95% branch coverage and, for a change that adds or
  modifies a calculation, the correctness gate of `development-process` holds.
- **NO-GO** — any test failure, coverage < 95%, or a failed correctness gate.

## Workflow

1. Write tests for the change (unit, integration, E2E as appropriate).
2. Run the full relevant suite.
3. Measure branch coverage for the changed code.
4. Attach the correctness metrics, for a change that adds or modifies a calculation.
5. Report the verdict (GO/NO-GO) with the coverage number.

## Rules

- Only the tester agent declares GO (with ui-ux-tester confirmation for UI).
- Keep tests deterministic and free of flakiness.
- Never skip the coverage gate.
