# Proposal

## Why

The `development-process` spec requires that any newly installed skill is recorded in
the specs with the installing developer, and `AGENTS.md` section 9 repeats it. On
2026-09-20 Akim installed the required project skills on a fresh machine and nothing
records it yet, so the team cannot tell which skills each developer has. Skills are
installed per machine and are not stored in the repository, so the specs are the only
shared record.

## What Changes

- Adds one requirement to the `development-process` capability: installed skills are
  recorded per developer with name, source, install scope, and date.
- Records the seven skills Akim installed on 2026-09-20 as scenario data.
- Adds a non-functional requirement: the record holds only public identifiers, never
  local paths, tokens, or credentials.

## Non-goals

- Installing or removing any skill.
- Recording Egor's skills; he records his own in a separate change.
- Recording skills that were not installed with `npx skills` (for example the
  `docx` and `skill-creator` skills provided by the claude.ai sync).
- Recording the 16 optional skills from `AGENTS.md` section 9 that are not installed.
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
