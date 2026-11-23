# Desktop browser compatibility matrix

This matrix records the inherited browser versions and manual verdicts for
review of `foundations-design-tools` frontend candidate
`bd9924478cf24f8e392f75efe7ee4a8289756c3b`. The version rows are source evidence,
not branded browser sessions run on this candidate.

## Inherited manual results

Akim confirmed browser acceptance and subsequently directed reuse of the
versions and verdicts from the previous matrix in the working conversation.
The [pressure-from-loads matrix](../foundations-pressure-from-loads/browser-matrix.md#required-version-slots)
records the original runs and their provenance. The reported journey covered
calculation type selection, input, computation, opening the result and report
download on that earlier candidate.

| Browser slot | Full version | Inherited manual verdict |
|---|---|---|
| Chrome C1 | 157.0.8103.38 | PASS |
| Chrome C2 | 158.0.8127.36 | PASS |
| Firefox F1 | 160.0.1 | PASS |
| Firefox F2 | 159.0 | PASS |
| Edge E1 | 158.0.4370.33 | PASS |
| Edge E2 | 157.0.4341.53 | PASS |
| Safari S1 | 27.2 | PASS |
| Safari S2 | 27.1 | PASS |

## Evidence on the design tools candidate

- Full Playwright: 154 passed, 68 configured skips, zero failures, using bundled Chromium, Firefox and WebKit. The local log `dec-accept-keyboard-fixed-e2e.log` (SHA-256 `e8c2b50a86f2ce75f4229b6368537aa3f0f6a38c3e4b99bd7b4499a9e37078cf`) names base commit `e9923c93c72c00f4fa7d0de93ebb2672fcc7e95b`. The run included the keyboard test patch, whose saved diff (SHA-256 `066458aaaf6fe37235762cea930cc2befb365ffc805d197aa43e61c8ddb4d534`) matches the complete diff from that base to `bd99244`, with no application source changes. The resulting commit tree is `9e13f8b39601ebb9c45f5ce48b32f5df8937e445`. This is evidence from the base plus patch, not a separate post-commit full run.
- Independent UI/UX: [review record below](#independent-uiux-review-record), PASS on `bd99244`.
- The inherited table does not establish fresh executions of branded Chrome, Firefox, Edge or Safari on `bd99244`, or independently verify version currency. Playwright WebKit is not branded Safari. No version slots are marked as newly executed.

Akim approved accepting the combined evidence in place of fresh branded browser
runs for `bd99244` only. The [OpenSpec evidence exception](../../../openspec/changes/foundations-design-tools/specs/web-platform/spec.md#requirement-revision-scoped-browser-acceptance-evidence)
records the boundary. This matrix does not issue feature GO or change the base
browser support requirement.

## Independent UI/UX review record

On 2026-11-24, `ui-ux-tester` McClintock reported PASS for
`bd9924478cf24f8e392f75efe7ee4a8289756c3b` in the working conversation
(agent task `01a20a93-5111-7fe3-b383-3a23a536c124`). The isolated mock-based
review ran 69 focused cases with 24 configured skips in bundled Chromium,
Firefox and WebKit. It inspected keyboard navigation, trace and MathJax,
mobile layout, the three work modes, the synthetic example and refusal,
and used axe and screenshot/accessibility-tree inspection. It did not
include a live screen reader or branded Edge or Safari runs.
