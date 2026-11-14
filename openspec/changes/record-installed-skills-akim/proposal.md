# Proposal

## Why

The `development-process` spec requires that any newly installed skill is recorded in
the specs with the installing developer, and `AGENTS.md` section 9 repeats it. On
2026-09-20 Akim installed the required project skills and eight further skills named
by the project's agents on a fresh machine, and nothing records it yet, so the team
cannot tell which skills each developer has. Skills are installed per machine and are
not stored in the repository, so the specs are the only shared record.

## What Changes

- Adds a requirement to the `development-process` capability: installed skills are
  recorded per developer with name, source, install scope, and date, each developer in
  a requirement of their own.
- Adds the requirement "Installed skills of Akim" with the fifteen skills Akim installed
  on 2026-09-20: seven required skills and eight of the 16 optional skills from
  `AGENTS.md` section 9. It is verified against the skills CLI lock file.
- Adds a non-functional requirement: the record holds only public identifiers, never
  local paths, tokens, or credentials.
- Records Akim's user-requested installation of `ub-mode` from `unclebob/ub-mode`
  on 2026-11-05 at global Codex scope. This entry is verified from the installed
  skill file rather than the skills CLI lock file.
- Records the user-requested companion tools `crapper`, `dryer`, and `mutator`
  installed for Akim on 2026-11-05 from their respective `unclebob` repositories.
  Installation uses a separate user environment; repository application dependencies
  and checks are unchanged.

## Non-goals

- Installing or removing any skill as part of the original September record.
  The November entries record explicitly requested user-environment installations.
- Recording Egor's skills; he records his own in a separate change.
- Recording skills that were not installed with `npx skills` (for example the
  `docx` and `skill-creator` skills provided by the claude.ai sync), except the
  explicitly requested Codex installation recorded above.
- Recording the eight optional skills that were not installed: `code-architecture-review`,
  `code-reviewer`, `devops-cicd`, `devops-engineer`, `docs-generator`, `flask-python`,
  `sqlite-database-expert`, `ui-ux-design`.
- Changing the existing "Skill availability check" requirement.
- Automating the record (no script or hook).
- Vetting the skills' content or security.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `development-process`: adds the requirement "Installed skills are recorded per
  developer".

## Impact

- Affects: `openspec/specs/development-process/spec.md` after archive. No code, no
  configuration, no other capability.
- Egor should acknowledge it because `openspec/` is a shared area.
