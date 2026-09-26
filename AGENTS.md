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
- **Normative data**: manual monitoring for now (one pilot file); NLP/RAG auto-parsing
  is a future, non-MVP goal. No ML in the calculation path (explicitly rejected).

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
   the orchestrator) and its branches are merged to `develop`.
8. **Archive** — the `spec-keeper` agent syncs specs and archives the change.

### Branching rules

- **Planning phase**: work happens on the `Specs` branch.
- **After planning is complete**: commit and push `Specs`, then create `develop` from
  `main` and merge `Specs` into `develop`.
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
- Do not implement on `develop`/`main` directly.
- Repo-meta files (agent entry files, agent settings, `.editorconfig`, `agent-docs/`) are
  not product changes and need no OpenSpec change; they are still committed on a branch.

## 3. DOR — Definition of Ready

A task is ready for implementation only when ALL of the following hold:

- An OpenSpec change proposal exists with `proposal.md`, `specs/…`, `design.md`,
  and `tasks.md` created and validated (`openspec validate`).
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

### Go / No-Go rules

- **GO** — tests pass with >= 95% coverage, UI/UX check passed, validation passed.
- **NO-GO** — any of: test failure, coverage < 95%, unvalidated OpenSpec artifacts,
  UI/UX defects blocking the user flow, or security findings.
- Only the `tester` agent (with `ui-ux-tester` confirmation) declares GO.

## 5. Team & responsibility zones

Two developers work on this project: **Akim** and **Egor**.

- Before starting any development, ask which developer is working: Akim or Egor,
  unless the agent's entry file already names the developer (`CLAUDE.md`: Akim).
- Responsibility zones MUST NOT overlap (the only shared artifact is SPECS).
- Specs extended by developers MUST complement each other, never contradict.
- Code MUST NOT overlap across zones, so git branches merge without conflicts.

| Developer | Responsibility zones |
|---|---|
| **Akim** | frontend/backend, calculation engine, report generator |
| **Egor** | normative-document pipeline, NLP/RAG parsing of normatives into the DB, DevOps, ML/DL/NLP |

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
