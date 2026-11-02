# Tasks

Owner: Akim. Feature: `codex-claude-mirror`.
Branch: `feature/codex-claude-mirror/backend`, from develop.
All configuration/mirror implementation belongs to this one feature. Specs are
maintained on develop; no commits or merges without explicit user consent.

## DOR

- [x] Proposal, design, requirements/scenarios and session-sized plan exist.
- [x] Strict validation passes and spec-reviewer reports no blocker/major (pass 2).
- [x] Dependencies: source Claude files and installed Codex CLI are available.
- [x] Acceptance and security requirements and branch assignment are explicit.

## Implementation

- [x] 1. Mirror source files and add native role TOML, config, rules and command skills.
- [x] 2. Add discovery symlinks and ignore local JSON; document compatibility limits.
- [x] 3. Validate source equality, formats, discovery, CLI loading and preservation.
- [x] 4. Tester verdict and independent review recorded with validation evidence.

## Closure

- [x] 5. User-approved commit, feature review and merge into develop
  (2026-11-03: feature `6df6917`, merge `4c3297d`; tester GO and review recorded).
- [ ] 6. Spec-keeper sync and archive after merge.

## DOD and GO/NO-GO

GO requires checks in requirement Codex mirror permission boundaries passing,
no security finding and a tester verdict. Application tests, performance and UI/UX are N/A: no application or UI changes.
This is a change with code (settings/ignore), using feature GO. Coverage has no
executable statement/branch denominator; no helper scripts are shipped. Any added
executable helpers require >=95% branch coverage.
NO-GO: missing source copy/role/skill, invalid formats, local settings tracked,
unsupported settings advertised as enforced, or changed Claude/prior-task files.
Full change DOD additionally requires approved merge and spec sync/archive.
