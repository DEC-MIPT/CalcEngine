# Shared configuration changed for the verifier's check sheets: to Egor

- Date: 2026-10-28
- From: Akim (backend zone). To: Egor.
- Change: `interim-normatives-source` (CH1), tasks 7.2c-7.4.
- Russian version: `2026-10-28-shared-config-changes-to-egor-rus.md`.

## What changed

The verifier's check sheets of interim normative data and the verified data file carry
SHA-256 digests in hex. `detect-secrets` reports each one as a high-entropy string, and the
promote step needs the sheets in git. So Akim changed two files we share:

| # | File | Change | Where | Commit |
|---|---|---|---|---|
| 1 | `.gitignore` | `!docs/verification/` and `!docs/verification/**`: git tracks the folder of check sheets, as it tracks `docs/decisions/` | `develop` | `b30ed49` |
| 2 | `.pre-commit-config.yaml` | `detect-secrets` skips `docs/verification/**.yaml` (sheets with `shown_digest` and the signature digest); the Markdown views are still scanned | `develop` | `b30ed49` |
| 3 | `.pre-commit-config.yaml` | `detect-secrets` also skips `backend/interim_normatives/**.yaml` (records with `value_digest`); the schema of these files forbids unknown fields | `feature/interim-normatives/backend`, merged with the feature | `f33df61` |

Changes 1 and 2 went straight to `develop`. `AGENTS.md`, section 2, counts both files as
code, which goes through a feature branch; Akim chose `develop` so the folder is tracked for
everyone at once (2026-10-27). `.secrets.baseline` did not change, and
`pre-commit run --all-files` passes.

## Questions

1. Do you agree with the three exclusions, or do you want another way to keep the digests out
   of the scan?
2. Is it acceptable that changes 1 and 2 went to `develop` directly, as a one-off, or should
   they be moved through a branch?
3. Added 2026-11-01: do you acknowledge the documentation-only change
   [`codex-context-navigation`](../../../openspec/changes/codex-context-navigation/proposal.md)
   as the second developer? It adds a repository map, sourced commands and context/quality
   guidance to [AGENTS.md](../../../AGENTS.md), plus a local navigation index in
   `docs/akim/README.md` (intentionally ignored by Git; shared instructions include a
   fallback). It changes no application code, product requirements or calculation
   methodology. Checks and review results are in the
   [verification record](../../../openspec/changes/codex-context-navigation/verification.md).
   Please name `codex-context-navigation` in your answer here; acknowledgement is still
   required for closure under the existing no-code gate, task 3.3.

## Answers

(to be filled in by Egor)
