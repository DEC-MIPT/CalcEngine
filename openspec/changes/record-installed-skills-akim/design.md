# Design

## Context

`development-process` already says a new skill "SHALL be recorded in the specs with the
installing developer" but defines neither what the record contains nor where it lives.
This change defines the content and adds the first record. It is documentation only.

## Goals

- One clear, checkable record format: developer, skill, source, scope, date.
- A record that stays correct when the colleague adds their own.
- A record that can be verified against a source outside the spec.

## Non-Goals

See `proposal.md` (Non-goals).

## Decisions

1. **Add new requirements, do not modify the existing one.** The existing requirement
   "Skill availability check" is correct; it lacks only the record content. Adding
   avoids rewriting shared text and keeps the delta small. The new general requirement
   says it defines that content, so the two cannot be read as conflicting.
2. **One requirement per developer.** The general rule is one requirement; each
   developer's record is a separate requirement named "Installed skills of <developer>".
   In OpenSpec, extending an archived requirement needs a MODIFIED block that repeats
   its full text. With one requirement per developer, a separately recorded developer's
   change ADDS their own requirement and does not overwrite Akim's text. A later change
   by Akim to Akim's own record uses MODIFIED on Akim's requirement only. Historical
   contributor records stay intact; the current sole-developer roster does not create
   or update another person's installation record.
3. **One change per developer.** Each developer records their own installs in their own
   change (`record-installed-skills-<developer>`), so records do not overlap. Currently
   Akim is the sole active developer; a new developer is recorded only after his announcement.
4. **Scope is recorded.** `find-skills` was installed at project scope (`.agents/`,
   gitignored); the other fourteen globally in the user's home. Scope tells a reader
   whether a skill applies to every project on that machine or only to this one.
5. **Sources are recorded as repositories**, in the form of the `npx skills add`
   commands of `AGENTS.md` section 9. The `--skill` name equals the recorded skill
   name, so the command is `npx skills add <source> --skill <skill> -g -y` for global
   scope, without `-g` for project scope.
6. **Two groups for Akim: required and optional.** The seven required skills come from
   `AGENTS.md` section 9 with fixed sources. The eight optional skills had no source
   in `AGENTS.md`, so a source was chosen from the skills registry: exact name match,
   preferring 1K or more installs or a known vendor. These sources are provisional
   until `AGENTS.md` fixes them; a skill of the same name from another author is a
   different skill, which is why the source is recorded. Install counts are not
   recorded, to keep the record to the five fields.
7. **The record is verified against the skills CLI lock file.** The CLI keeps a lock
   file for global skills on each machine, with `source` and `installedAt` per skill.
   A reviewer compares the record with it: same skill, same source, same date, and no
   skill in the lock file missing from the record. The project-scope skill is checked
   by the presence of its directory under the project's `.agents/skills/`. The
   repository's `skills-lock.json` holds only the project-scope `find-skills`, without
   dates; the spec record supplements it and does not replace it. The lock file is on
   the developer's machine, so the check is done by that developer.
8. **`tester` declares GO, as `AGENTS.md` section 4 requires.** This change has no code,
   so `tester` issues an explicit verdict "no code, no tests, coverage not applicable"
   once the inputs are met (see `tasks.md`). This is not an exception to section 4.

## Component boundary

Not applicable. No code is written, so there is no calculation hot path and no C/C++
swap boundary.

## Non-functional requirements

- Security: the record holds only skill name, source repository, scope, and date.
- Accessibility, performance, coverage: not applicable (documentation only).

## Risks

- **Stale record.** A skill may later be removed or updated; nothing in this change
  detects that. Accepted for MVP; the record states the date it was made.
- **Recording is not endorsement.** The `npx skills` CLI output on 2026-09-20 reported
  Snyk "Med Risk" for `find-skills`, `webapp-testing`, and `doc-coauthoring`, one Socket
  alert for `webapp-testing`, and two Socket alerts for `code-security`, and states that
  skills run with full agent permissions. The record does not assess them.
- **A skill can disagree with the project conventions.** `python-code-quality`
  recommends `ruff` with `ty` (its `SKILL.md` description and pre-commit example),
  while `AGENTS.md` section 7 requires `ruff` with `mypy`. The `AGENTS.md` convention
  prevails; this change does not resolve the difference.
- **Verification depends on one machine.** The lock file is not in the repository, so
  only the developer who installed can repeat the check.
