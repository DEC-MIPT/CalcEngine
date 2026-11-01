# DEC — Agent Operating Manual

Design Engineer's Calculator (DEC) — a cloud web service for automating engineering
calculations with a verified normative base, a transparent ("white box") calculation
engine, and GOST-compliant report generation.

This file is the single source of truth for how AI agents work in this repository.
Every agent (orchestrator, analyst, developers, testers, spec-keeper) MUST read and
follow it before acting.

## Start here

For a new task, use this file for shared rules and
[docs/akim/README.md](docs/akim/README.md) for selective context and current-work pointers.
That index is local and intentionally ignored by Git. If absent, use the map below,
`openspec list`, the selected change's artifacts and relevant `docs/decisions/` records.
Do not read the entire documentation archive before a local edit.

Codex does not need to read `CLAUDE.md` or `CLAUDE.local.md` each session. They remain
Claude Code entry points; their status snapshots are not the current task tracker.
Preserve generated OpenSpec instructions and managed blocks; do not run OpenSpec
initialization or update merely to refresh context.

## 1. Project summary

- DEC is a web SaaS developed as a master's IT-product thesis. Keep the MVP bounded;
  the product goals below do not imply that all capabilities are implemented or verified.
- **Product components (target)**:
  1. Normatives catalog / normative base — PostgreSQL + full-text search.
  2. Calculation engine — Python (NumPy/SciPy), architecture ready to hot-swap hot
     paths to C/C++ later.
  3. Single web platform — React + TypeScript frontend, FastAPI backend.
  4. Transparent output ("white box") — MathJax + React.
  5. Report generator — python-docx + reportlab (`.docx` for MVP).
- **Infrastructure**: Docker locally, with groundwork for deployment to a Russian
  cloud host (Yandex Cloud / VK Cloud / Cloud.ru) later.
- **Monetization**: B2B 30 000 ₽/mo (10 seats), B2C 3 000 ₽/mo, 14-day trial.
- **Normative data**: NLP/RAG auto-parsing of norms (collector, regex baseline parser,
  embeddings retrieval on CPU) is part of the MVP; a generative-LLM extraction step is
  deferred. No ML in the calculation path (explicitly rejected).

### Repository map and architecture

| Area | Code and checks | Requirements and detail |
|---|---|---|
| Calculation engine | `backend/app/engine/`, `backend/app/parameters/`, `backend/tests/test_engine_*.py` | `agent-docs/domain-constraints.md`; changes `calculation-core-contract`, `calculation-verification` |
| Backend/API | `backend/app/api/`, `services/`, `schemas/`, `repositories/`, `backend/alembic/`, `backend/tests/` | changes `backend-layered-architecture`, `calculation-api`, `normative-catalog-backend` |
| Frontend and trace | `frontend/src/`, colocated `*.test.ts(x)`, `frontend/e2e/` | `frontend/README.md`; change `frontend-app` |
| DOCX reports | `backend/app/reporting/`, `backend/tests/test_reporting_*.py` | `calculation-core-contract/specs/report-generator/`, change `report-title-block-limits` |
| Normative pipeline | `ml/src/normatives_pipeline/`, `ml/configs/`, `ml/tests/` (Egor) | `ml/research/PIPELINE.md`, catalog contract in `docs/decisions/` |
| Local infrastructure | `infra/docker-compose.yml` (Egor) | `README.md` local setup |
| Requirements and working context | `openspec/specs/`, `openspec/changes/`; `docs/decisions/`, `docs/verification/` | `docs/akim/` holds local plans, analysis and code journals |

Backend-relative names in the table are under `backend/app/`; change names are under
`openspec/changes/`. On `develop`, the pilot `foundations_shallow_r` calculates R and
checks supplied pressure p against it. Full settlement and pressure-from-loads calculations
are expansion work; check the selected branch before assuming a component exists.

The MVP target is a modular monolith with a separate worker process. The enforced backend
layers are in `backend/pyproject.toml`; `backend/app/worker/` is currently a package stub.
There is no worker launch command. The engine's pure `Calculator.calculate` function is
the future C/C++ boundary (`backend-layered-architecture/design.md`, decision 7).
Add services, queues or C++ only for a demonstrated need. NumPy/SciPy and PDF reports
are target-stack statements, not dependencies or delivered features of the current backend.

The cross-zone catalog contract is the database: read-only `catalog_read` views through
the backend's repository and `DEC_NORMATIVES_DATABASE_URL`, never imports from `ml/`.
See `docs/decisions/normative-catalog-backend-contract-akim.md`, including its Answers.
`backend/params/` holds engineer-set values; the scoped exception for interim norm data
is defined in the active `interim-normatives-source` change, not a general permission.

### Commands and verification

Commands below are defined in the named scripts/configuration and setup docs; listing
them does not claim they passed in this session. Use the existing environment; installing
dependencies or running migrations is a separate action. Activate `backend/.venv` before
`backend/check.sh`: the script changes directory but does not activate that environment.

| Working directory | Command | Purpose / prerequisite |
|---|---|---|
| Repository root | `openspec list`; `openspec status --change <name>` | Discover changes and artifact status; artifact completion is not DOR or GO |
| Repository root | `openspec validate <name> --strict`; `openspec validate --all --strict` | Validate selected change / all specs and changes |
| Repository root | `backend/check.sh` | Ruff, mypy, lint-imports, pytest with branch coverage of `app` and `scripts` >= 95% |
| Repository root | `frontend/check.sh` | API schema drift, ESLint, TypeScript, Vitest coverage; needs npm dependencies and backend Python |
| `backend/` | `.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --no-access-log` | Local API; database-backed requests need configured databases |
| `backend/` | `.venv/bin/alembic upgrade head` | Mutates configured application DB; use only for a task that needs migrations |
| `frontend/` | `npm run dev`; `npm run dev:mock` | Real backend / browser mocks; setup in `frontend/README.md` |
| `frontend/` | `npm run gen:api`; `npm run gen:api:check` | Regenerate / check `src/api/schema.d.ts` after API schema changes |
| `frontend/` | `npm run test:e2e` | Playwright; installed browsers required, own mock server on port 5179 |
| Repository root | `backend/.venv/bin/pre-commit run --all-files` | Existing secret and settings hooks; may rewrite `.secrets.baseline` |
| Repository root | `git diff --check` | Whitespace check for tracked edits |

Sources: `backend/check.sh`, `backend/pyproject.toml`, `frontend/check.sh`,
`frontend/package.json`, `frontend/playwright.config.ts`, `.pre-commit-config.yaml`,
`README.md`. Setup and database commands are in `README.md`; verify whether
`dec-postgres` already exists before choosing compose creation versus `docker start`.
Backend `postgres` tests skip without the corresponding `DEC_TEST_*DATABASE_URL` variables
(`backend/pyproject.toml`, marker description). Report skipped integration/catalog checks;
a green local suite alone does not verify the real catalog or calculation correctness.
Documentation-only edits need OpenSpec and document checks, not the full application suite.

## 2. Methodology: Spec-Driven Development (SDD) via OpenSpec

Every task in this project MUST be recorded in specs through OpenSpec. There is no
"just write code" path. The canonical OpenSpec root is `openspec/` in this repository.

### Lifecycle of any task

1. **Capture** — a task becomes an OpenSpec change proposal (`openspec new change`).
2. **Plan** — the `business-analyst` agent produces the plan and the DOR.
3. **Design** — the `architect` agent produces the design.
4. **Implement** — a developer agent works on the feature branch of the code (a change
   with no code has no branch: its documents go straight to `develop`).
5. **Test** — the `tester` agent writes and runs automated tests (coverage >= 95%)
   and issues the GO / NO-GO verdict for each feature.
6. **UI/UX check** — the `ui-ux-tester` agent verifies visuals and control behavior.
7. **Review & merge** — after GO, each feature is reviewed (by the other developer or
   the orchestrator) and its feature branch is merged to `develop`. For a change with no
   code, the second developer's acknowledgement is the review.
8. **Archive** — the `spec-keeper` agent syncs specs and archives the change.

### Branching rules

- **`develop` is the integration branch.** The bootstrap is done: `develop` was created
  from `main` and contains the former `Specs` / `Specs-onboarding` work. The `Specs*`
  branches are historical and no longer used.
- **`main` is frozen until MVP**: nothing is merged into `main` until there is a
  working prototype in `develop` (that prototype is the MVP).
- **Documents are committed directly to `develop`.** A document is a file on the
  "no code" list (section 4): `openspec/**` (specs and changes), `docs/**`,
  `agent-docs/**`, the agent and skill definitions under `.claude/`, `.kilo/`, and
  `.kilocode/`, `AGENTS.md`, `CLAUDE.md`, `README.md`, and `.editorconfig`. There is no
  sub-branch and no merge commit for them: the other developer reads `develop`, so a
  document is current as soon as it is committed. Before every commit and every push run
  `git fetch --all` and `git pull --ff-only`; if `develop` has diverged, stop and resolve
  it before going on. One exception for `.secrets.baseline`: when the pre-commit secret
  scan only rewrites line numbers in it or drops the entries of removed lines (exit 3,
  "The baseline file was updated", no "Potential secrets" report, and a diff of only
  `line_number` values, removed entries and `generated_at`), the rewritten baseline is
  committed together with the change that caused it, on that change's branch, `develop`
  included. A new finding is never added to the baseline in such a commit: it is removed
  from the file or marked there as a placeholder, or the baseline is regenerated with a
  hand review on a feature or fix branch.
- **Code goes only through a feature branch.** A feature is a component or a stage of
  the plan (for example the calculation engine, the report generator, the backend core,
  the frontend), named in the `tasks.md` of the one OpenSpec change it belongs to; a change
  may hold several features. Every file not on the document list (source code, tests, package
  manifests, `.gitignore`, agent settings, pre-commit config, `docker-compose.yml`) is
  code for this rule. Each feature gets its own branch from `develop` (or from the branch of
  an unmerged feature it depends on), named
  `feature/<feature>/<zone>`, and is merged into `develop` only when the whole feature
  is done: every task that `tasks.md` assigns to the feature is checked off, the `tester`
  has declared GO for the feature, and the review has passed (step 7 above). It is not
  merged per section or per subtask. One feature has exactly one branch; work in two zones
  is two features. A feature that needs code from an unmerged feature branches from it and
  merges after it. With the explicit consent required by section 7, push the branch to
  `origin` with the commit that finishes a subtask, so
  it stays visible, and bring new documents into it with `git merge develop`. The change
  is archived when all its features are merged.
  - Akim: `feature/<feature>/backend`, `feature/<feature>/frontend`
  - Egor: `feature/<feature>/data` (normative pipeline), `feature/<feature>/ml`
    (NLP/RAG/ML), `feature/<feature>/infra` (DevOps)
  - Fixes use `fix/<feature>/<zone>`.
- Do not implement code directly on `develop`/`main`; implement it on the feature branch
  and merge that branch into `develop`.
- The branch plan is part of the change proposal (in `tasks.md`): the change names each
  feature, its branch and its tasks (every task with code belongs to exactly one feature),
  or states that it has no code and no branch. The subtasks in `tasks.md` are checked off
  in `develop` as they are done on the feature branch, so `tasks.md` may run ahead of the
  code in `develop` until the feature is merged.

### Session start

Before starting a development session, an agent MUST check the state of commits on
`develop` and its remote:

- Run `git fetch --all` and inspect the commits that arrived on `origin/develop`
  and `origin/main` since the last session.
- If anything important arrived (new changes, merges, spec updates), warn the
  developer about it before doing anything else.
- Remind the developer to run `git pull` (and `git fetch --all`) so the local
  `develop` is up to date before starting work.
- Check `git status` for uncommitted or untracked work left by previous sessions.

Before starting a session, an agent MUST also inspect the current state of
`docs/decisions/` (tracked in git): start with filenames, headings and recent Git changes,
then read the decisions relevant to the selected task. These files are the team's written channel:
answers, confirmations, and review outcomes (for example
`backend/2026-10-07-<topic>-to-egor.md`, or the older `*-readiness*.md` at the root) may
have been added or updated since the last session. The layout of the folder is in
section 7, "Decision files". A decision or confirmation recorded there can change what
is blocked, agreed, or ready, so treat it as required context before acting.

Read Answers and later sections that resolve earlier questions in those decisions. Preserve
all existing user edits, including ignored files; never reset, stash or overwrite them
to obtain a clean tree. Check the current branch and whether required code has merged:
`tasks.md` completion alone is not evidence that it exists on `develop`.

Read base specs together with applicable active deltas and their readiness records.
Some base specs still name the beam placeholder pending `retarget-mvp-domain`; do not
silently copy it into foundation work. Distinguish requirements, observed code behavior,
analysis hypotheses and plans. Recheck a report's relevant claim against the selected
branch before relying on it; a filename containing "approved" is not an approval record.

Update the existing working-state record or journal when task status materially changes,
and maintain pointers in `docs/akim/README.md` when needed. Do not create a report for
each action or a second backlog. Shared decisions belong in `docs/decisions/`; local
`docs/akim/` material and source PDFs may be absent in another checkout. Never copy secrets,
machine paths or personal settings into shared instructions. For technical prose use
`technical-writing` when available; project conventions and explicit user scope prevail.

## 3. DOR — Definition of Ready

A task is ready for implementation only when ALL of the following hold:

- An OpenSpec change proposal exists with `proposal.md`, `specs/…`, `design.md`,
  and `tasks.md` created and validated (`openspec validate`).
- A `spec-reviewer` report on the current version of the change lists no blocker and
  no major finding. `openspec validate` checks structure only, so passing it alone
  does not make a change ready.
- Functional requirements are recorded as OpenSpec requirements/scenarios.
- Non-functional requirements (performance, security, accessibility, coverage) are
  recorded explicitly.
- The implementation plan (from the `business-analyst` agent) is complete and each
  task in `tasks.md` is small enough to complete in one session.
- Acceptance criteria and the Go/No-Go criteria are written.
- The feature branch name (`feature/<feature>/<zone>`) is defined, or the change states it has no code.
- Dependencies, if any, are listed and satisfied.

## 4. DOD — Definition of Done (with Go / No-Go)

A task is done only when ALL of the following hold:

- All tasks in `tasks.md` are checked off.
- Automated test coverage >= 95% (branch coverage) for the changed code.
- All tests pass (`tester` agent) — this is the primary GO signal.
- `ui-ux-tester` agent confirmed visuals and control behavior where UI changed.
- No known security issues introduced (refer to security best practices).
- `openspec validate` passes and the delta spec matches the implementation.
- The `spec-keeper` agent synced specs and archived the change.

The coverage, test, and UI/UX items apply to a change with code. A change with no code
takes the code-free path below instead.

### Go / No-Go rules

- **GO for a change with code** — declared per feature: tests pass with >= 95% coverage,
  UI/UX check passed, validation passed. The change is archived when all its features
  are merged.
- **GO for a change with no code** — `openspec validate --strict` passes, the
  `spec-reviewer` report lists no blocker and no major finding, and the developer who
  did not author the change has acknowledged it in a tracked commit or comment that
  names the change. The `tester` records `tests: N/A`, `coverage: N/A`, and
  `UI/UX: N/A`, each with the reason that the change has no code.
- **No code** means the change adds or edits no file outside `openspec/`, `docs/`,
  `agent-docs/`, the agent and skill definitions under `.claude/`, `.kilo/`, and
  `.kilocode/`, and `AGENTS.md`, `CLAUDE.md`, `README.md`, `.editorconfig`. Agent
  settings (for example `.claude/settings.json`) and `.gitignore` are not on the list. A
  refresh of `.secrets.baseline` that adds no finding, committed with a document under
  the exception of section 2, does not make a change a change with code.
- **NO-GO** — any of: test failure, coverage < 95%, unvalidated OpenSpec artifacts,
  UI/UX defects blocking the user flow, or security findings; for a change with no
  code, also a missing acknowledgement, an open blocker or major review finding, or a
  verdict without the N/A record.
- Only the `tester` agent (with `ui-ux-tester` confirmation where UI changed) declares
  GO.

## 5. Team & responsibility zones

The team is three people: two developers, **Akim** and **Egor**, and a product manager
(**PM**). The PM owns scope, pricing, and legal decisions, has no code zone and no
branch, and has no agent unless a later change adds one. A PM decision is recorded by a
developer as a dated entry in a tracked file under `docs/decisions/product/` (the
decision, the PM's words, and where they were given; section 7, "Decision files").

- Before starting any development, ask which developer is working: Akim or Egor,
  unless the developer's own untracked instructions already name the developer (for
  Claude Code, `CLAUDE.local.md` in that developer's checkout).
- Responsibility zones MUST NOT overlap (the only shared artifact is SPECS).
- Specs extended by developers MUST complement each other, never contradict.
- Code MUST NOT overlap across zones, so git branches merge without conflicts.

| Member | Responsibility zones |
|---|---|
| **Akim** | frontend/backend, calculation engine, report generator |
| **Egor** | normative-document pipeline, NLP/RAG parsing of normatives into the DB, DevOps, ML/DL/NLP |
| **PM** | scope, pricing, and legal decisions; no code zone |

Zone-to-agent mapping:

| Zone | Agent(s) |
|---|---|
| frontend/backend, engine, report generator | `frontend-developer`, `backend-developer` (Akim) |
| normative pipeline, NLP/RAG, ML | `data-engineer` (Egor) |
| DevOps | `devops-engineer` (Egor) |

## 6. Agent roster

| Agent | Role |
|---|---|
| `orchestrator` | Product agent: prioritizes tasks, dispatches subagents/skills, coordinates. |
| `business-analyst` | Planning: decomposes tasks, writes DOR + functional/non-functional requirements. |
| `architect` | System/component design, tech choices, C/C++ swap boundaries. |
| `backend-developer` | FastAPI, PostgreSQL, calculation engine (NumPy/SciPy), report generator. |
| `frontend-developer` | React + TypeScript, MathJax rendering, forms, UI logic. |
| `devops-engineer` | Docker, local env, CI groundwork, future cloud deployment. |
| `data-engineer` | Normative-document ingestion pipeline, NLP/RAG parsing into the DB, ML/DL/NLP work. |
| `tester` | Automated tests (pytest / Vitest+RTL / Playwright), >= 95% branch coverage, GO/NO-GO. |
| `ui-ux-tester` | Visual testing, control/button behavior, accessibility. |
| `ui-ux-designer` | Visual design, design system, layouts. |
| `spec-keeper` | Keeps OpenSpec specs actual, creates new agents/skills as the project grows. |
| `spec-reviewer` | Read-only review of a spec or change for completeness, testability, and OpenSpec format; reports gaps, never edits. |
| `norm-traceability-checker` | Read-only check that each calculation requirement names its norm source, edition, and clause; does not verify correctness. |

## 7. Conventions

- **Language**: all specs, agents, skills, and commit messages are in English.
- **Commits**: Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `docs:`).
- **Answers to questions**: when answering questions that a team member recorded in a
  `docs/decisions/` file, write the answers into the same file where the question was
  asked (append an `## Answers` section), not into a separate file.
- **Decision files** (`docs/decisions/`; agreed by Akim and Egor, section 2 of
  `docs/decisions/egor-open-points-akim.md` and Egor's reply of 2026-10-06):
  - A new file goes into the folder of its direction: `data/`, `ml/`, `infra/` (Egor),
    `backend/`, `frontend/` (Akim), `product/` (PM decisions, recorded by a developer).
  - Its name is `YYYY-MM-DD-<topic>.md`, the date the file is created; it is never
    renamed. Its Russian version is `YYYY-MM-DD-<topic>-rus.md` in the same folder.
  - A topic between zones goes into the folder of whoever writes first (asks the
    question or keeps the record), and the name ends with the addressee, for example
    `2026-10-05-formula-autoparse-limits-to-akim.md`. The readiness record of a change
    goes into the folder of the zone that leads the change.
  - A new question on an earlier topic is a new file that links to the earlier one; the
    earlier file stays a snapshot of its stage.
  - Files created before this rule stay at the root of `docs/decisions/`; topics still
    open in them go on in the same files until they close.
  - A file and its `-rus` version change in the same commit.
- **Never commit, merge, or push without the working developer's explicit consent.**
  Prepare and show the changes (diff) and the intended commit message, then wait for
  approval before running `git commit`, `git merge`, or `git push`.
- **Testing**:
  - Backend: `pytest` (unit + integration), coverage via `coverage.py`.
  - Frontend: `Vitest` + React Testing Library; E2E via Playwright.
  - Coverage target: >= 95% branch coverage.
- **Domain constraints**: calculation code and norm references follow
  `agent-docs/domain-constraints.md` (pure, deterministic, explicit units, primary-source
  citations only). A methodology change also names its formula, units and applicability.
  Never invent normative citations, coefficients, tolerances or expected results.
- **Reference results**: record the source and derivation of control values. The tested
  implementation's own output is not an independent oracle. Read the existing correctness
  gate in `calculation-verification` and `docs/decisions/reference-examples-foundations.md`
  before changing a calculation; coverage alone does not establish correctness.
- **Conflicts and contracts**: explicitly report a conflict between a spec, source norm
  and reference example. Do not choose a coefficient or rewrite the expected result to
  make a test pass. Coordinate API/data changes through the applicable OpenSpec change
  and the existing zone contract; regenerate frontend API types when required.
- **Autonomy and questions**: make local reversible choices within the task. Ask when
  ambiguity affects methodology, public contracts, requirement scope, compatibility or
  another developer's zone. Permission for ordinary documentation edits is not permission
  to commit, merge or push. Apply section 4 gates to closure; report completed work,
  actual checks, skips and remaining decisions without inventing GO or acknowledgement.
- **Code style**: no comments unless required; follow existing patterns; run lint and
  type checks before declaring done:
  - Backend: `ruff` (lint) + `mypy` (types).
  - Frontend: `eslint` (lint) + `tsc` (types).

## 8. Where agents live

- Claude Code: `.claude/agents/*.md` (canonical), `.claude/commands/`, `.claude/skills/`.
  Claude Code does not read `AGENTS.md`; `CLAUDE.md` imports it and adds nothing that
  contradicts it. Shared project settings live in `.claude/settings.json` (committed);
  machine-specific settings in `.claude/settings.local.json` (ignored).
- Kilo Code: `.kilo/agent/*.md`, `.kilo/skills/*/SKILL.md`,
  `.kilocode/skills/*/SKILL.md`, `.kilocode/workflows/*.md`. Kilo reads `AGENTS.md`
  natively. Kept as a secondary mirror for fallback use.
- Keep both in sync when adding or changing agents. Exception: agents with
  Claude-specific frontmatter (`model`, `tools`) live in `.claude/agents/` only,
  listed in `CLAUDE.md`.

## 9. Required skills

The primary skill every developer MUST have is `find-skills` — the entry point for
discovering other skills:

    npx skills add https://github.com/vercel-labs/skills --skill find-skills

The canonical source for discovering and installing skills is
`https://github.com/vercel-labs/skills`. Required skills are installed per machine and
are NOT stored in the repository.

### Project skills (install on each machine)

Frontend / design:

    npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices -g -y
    npx skills add vercel-labs/agent-skills --skill vercel-composition-patterns -g -y
    npx skills add vercel-labs/agent-skills --skill web-design-guidelines -g -y
    npx skills add anthropics/skills --skill frontend-design -g -y

Testing / reports / spec tooling:

    npx skills add anthropics/skills --skill webapp-testing -g -y
    npx skills add anthropics/skills --skill docx -g -y
    npx skills add anthropics/skills --skill skill-creator -g -y
    npx skills add anthropics/skills --skill doc-coauthoring -g -y

Additional skills already on the reference machine (discover exact commands via
`find-skills`): accessibility, code-architecture-review, code-reviewer, code-security,
devops-cicd, devops-engineer, docs-generator, flask-python, owasp-security,
postgresql-database-engineering, pytest-skill, python-code-quality,
software-architecture-design, sqlite-database-expert, technical-writing, ui-ux-design.

### At the start of every iteration

- Ask which developer is working: Akim or Egor (section 5 says when this is skipped).
- Verify that the required skills are present.
- If a required skill is missing, print a warning with the exact install command and
  instruct the developer to install it.
- When a developer installs a new skill, record it in the SPECS (an OpenSpec change)
  naming the developer and the skill, so the team knows it was added and by whom.
