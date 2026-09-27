# DEC — Agent Operating Manual

Design Engineer's Calculator (DEC) — a cloud web service for automating engineering
calculations with a verified normative base, a transparent ("white box") calculation
engine, and GOST-compliant report generation.

This file is the single source of truth for how AI agents work in this repository.
Every agent (orchestrator, analyst, developers, testers, spec-keeper) MUST read and
follow it before acting.

## 1. Project summary

- **Problem**: design engineers spend up to 30% of their time searching for current
  norms, doing manual calculations, and re-checking them; arithmetic/methodology
  errors and outdated norms cause expert-review rejections.
- **Solution (USP)**: a "single window" combining a normative base (SP/GOST/SNiP),
  a verified calculation engine, and a GOST report generator.
- **Five product components**:
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

## 2. Methodology: Spec-Driven Development (SDD) via OpenSpec

Every task in this project MUST be recorded in specs through OpenSpec. There is no
"just write code" path. The canonical OpenSpec root is `openspec/` in this repository.

### Lifecycle of any task

1. **Capture** — a task becomes an OpenSpec change proposal (`openspec new change`).
2. **Plan** — the `business-analyst` agent produces the plan and the DOR.
3. **Design** — the `architect` agent produces the design.
4. **Implement** — a developer agent works on a dedicated branch.
5. **Test** — the `tester` agent writes and runs automated tests (coverage >= 95%)
   and issues the GO / NO-GO verdict.
6. **UI/UX check** — the `ui-ux-tester` agent verifies visuals and control behavior.
7. **Review & merge** — after GO, the change is reviewed (by the other developer or
   the orchestrator) and its branches are merged to `develop`. For a change with no
   code, the second developer's acknowledgement is the review.
8. **Archive** — the `spec-keeper` agent syncs specs and archives the change.

### Branching rules

- **All work happens in the `develop` branch only.** The bootstrap is done:
  `develop` was created from `main` and contains the former `Specs` /
  `Specs-onboarding` work. The `Specs*` branches are historical and no longer used.
- **A sub-branch of `develop` is a task branch** — exactly the branch a developer
  (Akim or Egor) is currently working on. Create it from `develop` and merge it back
  into `develop` when the task is done.
- **`main` is frozen until MVP**: nothing is merged into `main` until there is a
  working prototype in `develop` (that prototype is the MVP).
- Every task gets its own branch AND a zone sub-branch from `develop`. Zone
  sub-branches map to developer responsibility zones (see Team section):
  - Akim: `feature/<task>/backend`, `feature/<task>/frontend`
  - Egor: `feature/<task>/data` (normative pipeline), `feature/<task>/ml`
    (NLP/RAG/ML), `feature/<task>/infra` (DevOps)
  - Fixes use `fix/<task>/<zone>`.
- The branch plan is part of the change proposal (in `tasks.md`), so it is also
  reflected in the specs via OpenSpec.
- Do not implement directly on `develop`/`main`; implement on the task sub-branch
  and merge it into `develop`.
- Repo-meta files (agent entry files, agent settings, `.editorconfig`, `agent-docs/`) are
  not product changes and need no OpenSpec change; they are still committed on a branch.
  A change that includes agent settings is still not code-free for GO (section 4).
- **No-code documents merge into `develop` as soon as they are ready, not held for the
  rest of the task.** A change to `openspec/**` (specs and changes), `AGENTS.md`, or any
  other no-code document (`docs/**`, `agent-docs/**`) is the team's shared state: the
  other developer reads `develop`, not a task sub-branch. As soon as that document change
  is in the form it should have on `develop` (a validated OpenSpec change, an agreed
  `AGENTS.md` edit, a decision record), merge the sub-branch into `develop`, even if the
  code part of the task is still in progress. Do not let doc-only work sit unmerged on a
  sub-branch waiting for the rest of the task.

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

Before starting a session, an agent MUST also read the current state of
`docs/decisions/` (tracked in git). These files are the team's written channel:
answers, confirmations, and review outcomes (for example
`normref-questions-egor*.md`, `*-readiness*.md`) may have been added or updated
since the last session. A decision or confirmation recorded there can change what
is blocked, agreed, or ready, so treat it as required context before acting.

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
- Branch naming (frontend/backend sub-branches) is defined.
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

- **GO for a change with code** — tests pass with >= 95% coverage, UI/UX check passed,
  validation passed.
- **GO for a change with no code** — `openspec validate --strict` passes, the
  `spec-reviewer` report lists no blocker and no major finding, and the developer who
  did not author the change has acknowledged it in a tracked commit or comment that
  names the change. The `tester` records `tests: N/A`, `coverage: N/A`, and
  `UI/UX: N/A`, each with the reason that the change has no code.
- **No code** means the change adds or edits no file outside `openspec/`, `docs/`,
  `agent-docs/`, the agent and skill definitions under `.claude/`, `.kilo/`, and
  `.kilocode/`, and `AGENTS.md`, `CLAUDE.md`, `README.md`, `.editorconfig`. Agent
  settings (for example `.claude/settings.json`) and `.gitignore` are not on the list.
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
developer as a dated entry in a tracked file under `docs/decisions/` (the decision, the
PM's words, and where they were given).

- Before starting any development, ask which developer is working: Akim or Egor,
  unless the agent's entry file already names the developer (`CLAUDE.md`: Akim).
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
- **Never commit, merge, or push without the working developer's explicit consent.**
  Prepare and show the changes (diff) and the intended commit message, then wait for
  approval before running `git commit`, `git merge`, or `git push`.
- **Testing**:
  - Backend: `pytest` (unit + integration), coverage via `coverage.py`.
  - Frontend: `Vitest` + React Testing Library; E2E via Playwright.
  - Coverage target: >= 95% branch coverage.
- **Domain constraints**: calculation code and norm references follow
  `agent-docs/domain-constraints.md` (pure, deterministic, explicit units, primary-source
  citations only).
- **Code style**: no comments unless required; follow existing patterns; run lint and
  type checks before declaring done:
  - Backend: `ruff` (lint) + `mypy` (types).
  - Frontend: `eslint` (lint) + `tsc` (types).

## 8. Where agents live

- Kilo Code: `.kilo/agent/*.md` (canonical), `.kilo/skills/*/SKILL.md`,
  `.kilocode/skills/*/SKILL.md`, `.kilocode/workflows/*.md`. Kilo reads `AGENTS.md` natively.
- Claude Code: mirror under `.claude/agents/*.md`, `.claude/commands/`, `.claude/skills/`.
  Claude Code does not read `AGENTS.md`; `CLAUDE.md` imports it and adds nothing that
  contradicts it. Claude-only settings live in `.claude/settings.json`.
- Keep both mirrors in sync when adding or changing agents. Exception: agents that need
  Claude-specific frontmatter (`model`, `tools`) may exist in `.claude/agents/` only,
  and are listed in `CLAUDE.md`.

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

- Ask which developer is working: Akim or Egor.
- Verify that the required skills are present.
- If a required skill is missing, print a warning with the exact install command and
  instruct the developer to install it.
- When a developer installs a new skill, record it in the SPECS (an OpenSpec change)
  naming the developer and the skill, so the team knows it was added and by whom.
