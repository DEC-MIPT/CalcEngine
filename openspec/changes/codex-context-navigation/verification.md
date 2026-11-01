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
