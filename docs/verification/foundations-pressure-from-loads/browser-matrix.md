# Desktop browser compatibility matrix

Status: COMPLETE under the approved manual protocol. This worksheet records manual evidence for task 3.6 of
[foundations-pressure-from-loads archive](../../../openspec/changes/archive/2026-11-23-foundations-pressure-from-loads/tasks.md).
The acceptance requirement is in [web-platform](../../../openspec/specs/web-platform/spec.md),
"Non-functional — language, accessibility, browsers".

Akim reported access to a test environment in the working conversation on
2026-11-22 and requested stepwise collection. The first Chrome environment
and B1 manual result were reported on 2026-11-23. Installed Playwright engines
remain separate evidence.

## Revision and environment

The candidate is `feature/foundations-loads/frontend`, base commit
`2b70c6923c497523c1b1fb70d2592b46a30a084e`, plus these working-tree files:

| File | SHA-256 |
|---|---|
| `frontend/src/components/Trace.tsx` | `ebd028c88b11343e770d27c0942c6c0494bdbe1363d22585834583c14c6df735` |
| `frontend/src/components/Trace.compact.test.tsx` | `bc84aceece4a60493ea4968aa61abeecaf845b78a544d058c90194ff451837fc` |
| `frontend/e2e/loads-compact-trace.spec.ts` | `612dafbb9df5c705635b83c0526dbbc80e27cb1e43f44e0fe42f89d93c2440cd` |
| `frontend/src/api/schema.d.ts` | `16d79bf0448aecbdcf89805d07a49ee71f701fe6cf65cec5b6a278656efd0654` |

The reported C1 OS is Windows 11 Pro 26H2. On 2026-11-23 Akim explicitly
simplified manual recording to browser version and whether the complete journey
works. The reports are associated with the candidate discussed in this
conversation. Its four file hashes still match the reviewed manifest.
The served-build identity, site address and backend mode were not independently
observed; this limitation is retained rather than represented as automated
verification.

## Required version slots

The eight versions below are Akim's supplied environments for the requested
two-version-per-browser matrix. Under the explicitly approved simplified
protocol, the record contains the version and reported end-to-end result.
Independent vendor release-currency verification was not collected as manual
evidence. Compatibility observations apply to these exact reported versions;
they are not independently executed branded-browser observations.

| Browser slot | Full version | End-to-end result |
|---|---|---|
| Chrome C1 | 157.0.8103.38 | PASS |
| Chrome C2 | 158.0.8127.36 | PASS |
| Firefox F1 | 160.0.1 | PASS |
| Firefox F2 | 159.0 | PASS |
| Edge E1 | 158.0.4370.33 | PASS |
| Edge E2 | 157.0.4341.53 | PASS |
| Safari S1 | 27.2 | PASS |
| Safari S2 | 27.1 | PASS |

## Scenario sequence for each version

Issue one check at a time in the conversation. Record the exact slot, scenario,
date, verifier, observed result and evidence reference for every answer.
Environment identification alone is not a scenario PASS.

| Check | Required observations |
|---|---|
| E2E | Choose a calculation type, enter valid inputs, run the calculation, open the result and download the report. Record whether the complete journey works. |

## Recorded results

| Date | Slot | Check | Result | Evidence |
|---|---|---|---|---|
| 2026-11-23 | C1 | Earlier B1 | PASS | User-reported form check under the earlier protocol; does not certify the complete E2E journey. |
| 2026-11-23 | C1 | E2E | PASS | User-confirmed complete journey: type selection, valid input, calculation, result opening and report download. |
| 2026-11-23 | C2 | E2E | PASS | User-confirmed complete journey on Chrome 158.0.8127.36: type selection, valid input, calculation, result opening and report download. |
| 2026-11-23 | F1 | E2E | PASS | Akim reported that the complete journey works in Firefox 160.0.1. |
| 2026-11-23 | F2 | E2E | PASS | Akim reported that the complete journey works in Firefox 159.0. |
| 2026-11-23 | E1 | E2E | PASS | Akim reported that the complete journey works in Edge 158.0.4370.33. |
| 2026-11-23 | E2 | E2E | PASS | Akim reported that the complete journey works in Edge 157.0.4341.53. |
| 2026-11-23 | S1 | E2E | PASS | Akim reported that the complete journey works in Safari 27.2. |
| 2026-11-23 | S2 | E2E | PASS | Akim reported that the complete journey works in Safari 27.1. |

Use the existing admitted pressure references and captured fixtures; do not
derive new expected calculations from the browser under test. Record
unavailable scenarios as NOT RUN and defects as FAIL. Reported manual results
remain distinguishable from automated observations.

## Matrix result

All eight browser-version rows have a reported PASS for the approved simplified
E2E journey. UI/UX confirms the reviewed candidate and installed-engine evidence.
Tester issued scoped GO for task 3.6. This record does not claim independently
operated branded-browser sessions, served-build observation, official vendor
release qualification or screen-reader testing.
