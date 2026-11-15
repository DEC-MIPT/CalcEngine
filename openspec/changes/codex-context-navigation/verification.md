# Context navigation verification

## Scope and evidence

Audit checkpoint: 2026-11-01, `develop` at `34eb49a`. This change edits instructions and
navigation only. It does not certify calculation methodology or application correctness.

- `git fetch --all` succeeded after sandbox escalation. No remote updates arrived;
  `git rev-list --left-right --count develop...origin/develop` returned `8 0`, and
  `main...origin/main` returned `0 0`. No pull, commit, merge or push was performed.
- Initial user work: modified `docs/verification/interim-normatives-source/P2-1.yaml`
  and two untracked `2026-10-28-shared-config-changes-to-egor` decision files (English
  and Russian). Their content hashes were saved outside the repository for preservation
  checks, together with Claude files and configuration; no private contents are copied here.
- Instruction discovery found only the root `AGENTS.md`, no nested `AGENTS.md` or
  `AGENTS.override.md` outside dependency/environment directories. The root contains
  no managed OpenSpec block. OpenSpec configuration and generated commands stay unchanged.
- `CLAUDE.md` and relevant local instructions were read for this audit. They are not
  a required Codex startup dependency and are not edited.
- Required skills are available except `docx` in this session's catalog. The user was
  given the existing install command; no skill was installed and no settings changed.

## Findings that affect routing

| Finding | Direct evidence | Treatment |
|---|---|---|
| Foundation pilot, API, frontend and DOCX reporting exist on `develop` | `backend/app/engine/foundations_shallow_r.py`, `backend/app/main.py`, `frontend/src/`, `backend/app/reporting/` | Map real components; keep broader stack/product statements marked as targets |
| Worker is a package stub; backend venv is not activated by the check script | `backend/app/worker/__init__.py`, `backend/check.sh` | No invented worker command; explicit check prerequisite |
| CH1 work exceeds the integration branch | `git log -1` on `feature/interim-normatives/backend` (`f33df61`) and frontend (`a8fb64e`); `git merge-base --is-ancestor` returned 1 for each against `develop`; feature trees contain interim files absent on `develop` | Explain checkboxes versus branch state; link existing readiness and journal |
| Catalog source is implemented despite the older inventory's current-branch claim | `docs/akim/analysis-sls/04-impl-inventory.md` names its branch; `backend/app/main.py` wires `catalog_sources` | Index dates/scopes the report rather than rewriting history |
| Plan 09 contains stale unmerged-status claims and points to 08 for detail | `docs/akim/analysis-sls/09-sls2-approved-plan.md`; current code and readiness records | Treat approval and implementation as separate evidence; 08 routes expansion planning |
| CH1 early pending questions have later answers | CH1 readiness's DOR/verifier sections, design "Open questions", acknowledgement Answers | Route to later answers, preserve the original decision records |
| Base specs retain the beam placeholder | `openspec/specs/calculation-engine/spec.md`, `retarget-mvp-domain/tasks.md` | Read applicable active deltas with base specs; do not change product requirements |
| Digitization utility is feature-only | `git ls-tree feature/digitization-tools/backend:tools/digitization`; only ignored caches under this checkout's tools directory | Name branch/path explicitly; no command advertised as available on `develop` |
| Local documentation is not distributed | `.gitignore` excludes `docs/*` except decisions and verification | Keep `docs/akim/README.md` ignored, provide a shared fallback in `AGENTS.md` |

## Checks

- `openspec validate codex-context-navigation --strict`: passed.
- `openspec validate --all --strict`: passed, 22 items, 0 failures. Existing informational
  notices include long requirements and an archive-target mismatch in
  `formula-extractor-fix`; these are outside this change.
- `git diff --check`: passed. A separate check covered whitespace and final newlines in
  all seven Markdown documents, including new and ignored files.
- All 69 relative Markdown links/anchors resolved. Feature-only paths were separately
  checked with `git ls-tree` on the named branches.
- Privacy/path pattern checks and manual reading found no copied local preferences,
  credentials or machine-specific paths. Hash comparisons confirmed all eight saved
  user/Claude/configuration files were unchanged. Root managed-block comparison passed
  (no such block exists in either version); no generated command was edited.
- Targeted `backend/.venv/bin/pre-commit run --files ...` passed Detect secrets for
  the edited Markdown documents. The environment-settings hook skipped because no
  matching file changed. The full all-files hook run was not needed for this scope.
- Final diff/scope review found only `AGENTS.md`, the new OpenSpec change and ignored
  `docs/akim/README.md` authored by this task; original user work remains separate.

Application commands in `AGENTS.md` were checked against their named scripts,
configuration and setup documentation. Servers, migrations, application test suites and
browser tests were not run for this documentation change. Automatic instruction loading
in a new Codex CLI session was not tested.

## Reviews and closure

- 2026-11-01 `spec-reviewer`: blocker 0, major 0, minor 0; READY for DOR. Reviewed change
  artifacts, shared instructions, local index and process/source consistency. The reviewer
  did not run validation; its mechanical results are recorded above. Final rereview after
  the reader clarifications confirmed the same counts and verdict.
- 2026-11-01 independent reader rehearsal: engine, API, frontend, DOCX and spec routes
  reached their requirements/code/checks; current CH1 and the tracked-only fallback were
  usable. No blocker or broken link. Two optional clarifications were applied: selective
  decision reading at session start and historical status snapshots in plan 08.

## Tester verdict (2026-11-01)

NO-GO for closure, solely because the other developer's acknowledgement naming
`codex-context-navigation` has not been received. No document defect remains.

- tests: N/A, this change has no application code.
- coverage: N/A, this change has no application code.
- UI/UX: N/A, this change has no application code or interface changes.

The tester independently reran strict selected/full OpenSpec validation (22 passed,
0 failed), the seven-document/69-link check, whitespace/final-newline checks and
`git diff --check`, and reviewed scope and both reader clarifications. Preservation
hashes, privacy checks and targeted hooks were parent-run evidence, not repeated by
the tester. No application suite was run.

After a tracked second-developer acknowledgement, request tester reassessment under
the existing no-code gate. No GO, spec sync or archive is claimed. Task 3.3 and archive
task 4.1 remain open; this session does not commit, merge, push or publish.

## Operational index lifecycle amendment, 2026-11-15

Akim approved the clarified operational-index approach and explicitly authorized
recording it in AGENTS.md, this existing change and the local index. This amendment
codifies the rule only. It does not consolidate historical index text, remove any
feature card, sync main specs, archive the change or authorize Git delivery.

### Updated scope

- AGENTS.md now owns the shared local-context-index lifecycle rule: durable routes
  and working agreements, compact unfinished-work cards, evidence-backed removal,
  preserved source history and outstanding obligations, and durable dependency links.
- The proposal/design/tasks and development-process delta define the same policy.
  One new requirement adds seven observable scenarios. Both original requirements
  and all five original scenarios remain verbatim.
- docs/akim/README.md contains a short linked reminder near the start. Its original
  historical sections remain unchanged, with consolidation explicitly outside scope.
- No numeric size limit or fixed template is introduced. Code-free work retains
  its existing gates and needs a journal link only where one is required.
- Preparation stays in the existing checkout to preserve user work. Any later
  document commit belongs directly on develop under the existing consent rules;
  no new branch, commit, merge or push was made for this amendment.

### Checks and preservation

- Selected strict validation PASS; all strict validation PASS, 22/22. Existing
  informational notices do not establish archive eligibility for unrelated changes.
- Whitespace and final-newline checks PASS for all seven scoped Markdown files,
  including the ignored local index. git diff --check PASS.
- Original AGENTS.md and local index contents are recovered byte-for-byte after
  removing only the inserted policy sections. This verifies that no retrospective
  cleanup or removal of existing user text occurred.
- All 17 previously modified/untracked files retain their original content hashes.
  No application, settings, Claude entry-point, OpenSpec configuration or generated
  instruction changes were made.
- The new local-index link resolves to the AGENTS lifecycle heading. Relative links
  in the current change resolve. Historical links in retained old index snapshots
  were not re-audited; the original 69-link audit above remains historical evidence.
- Targeted pre-commit checks on the seven scoped documents PASS: Detect secrets
  passed; the settings-example hook skipped because no matching file changed.
- Document-case rehearsal PASS for all seven new scenarios: compact unfinished
  routing; switched/paused work; GO/commit without integration; completed code
  feature removal with preserved evidence; code-free gates; unfinished features
  or change-level closure work; durable history and dependency routes.

### Current reviews and no-code verdict

Current independent spec-reviewer: 0 blockers, 0 major, 0 minor, READY for DOR.
Final confirmation includes the conditional journal wording for code-free cards.
The tester independently repeated strict validation, preservation, whitespace,
link and scenario checks; targeted hooks are parent-run evidence.

Tester amendment verification PASS. Change closure remains NO-GO because the
other developer's acknowledgement naming codex-context-navigation is missing.
Question 3 in the existing file to Egor still has a placeholder Answers section;
Akim's approval of this amendment is not that acknowledgement.

- tests: N/A, no application code changed; document checks were performed.
- coverage: N/A, no application code changed.
- UI/UX: N/A, no interface changed.

Tasks 2.3-2.5 are complete. Task 3.3 and archive task 4.1 remain open. No change GO,
spec sync or archive is claimed. The current policy is recorded in all three
requested locations; applying it to the accumulated history remains separate work.

## Sole-developer policy applicability, 2026-11-15

Akim has confirmed that Egor left and no second developer is available. The
[recorded decision](../../../docs/decisions/backend/2026-11-15-solo-developer-document-workflow.md)
waives second-human confirmations while this mode applies and requires actual
checkouts of develop for all documentation edits. The previous NO-GO entries for
missing acknowledgement are historical; no Egor signature or acknowledgement is
invented. Task 3.3 is now N/A under the policy. Task 3.5 requests fresh tester
reassessment of remaining current checks; archive task 4.1 is still open.

This record does not grant GO or archive by itself. Current governance edits to
CLAUDE, OpenSpec context and instruction mirrors belong to the separate
solo-developer-document-workflow change; prior preservation checks describe their
own earlier scope. Index historical text has not been consolidated or deleted.


### Current reassessment outcome

Independent current spec review: zero blocker, major or minor findings. The tester
issued **GO for documentation acceptance** on 2026-11-15 after strict validation,
current policy/link/scope checks, mirror consistency checks and passing targeted
secret-scan hooks. Task 3.5 is complete. The earlier human-confirmation NO-GO is
superseded for current work by the recorded sole-developer policy, not by a new
human acknowledgement. Archive task 4.1 remains open; no index cleanup, spec sync,
archive or Git delivery occurred.

- tests: N/A — no application code changed; document checks performed.
- coverage: N/A — no application code changed.
- UI/UX: N/A — no interface changed.
