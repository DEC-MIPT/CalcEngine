# Codex mirror of Claude project tooling

## Why

DEC project roles and workflows exist under `.claude/`, while `.codex/` is empty.
Akim requested a Codex mirror before CH1 frontend acceptance.

## What changes

Preserve all Claude agents, commands, skills and shared/local settings under
`.codex/`; add native Codex role TOML, project config, command permission rules,
and skill discovery links. Explain format differences and local-settings limits.

## Non-goals

No application changes, CH1 9.2 execution, credential migration, global Codex
configuration changes, automatic commits, merges or pushes. Claude stays canonical.

## Impact

One feature, `codex-claude-mirror`, on `feature/codex-claude-mirror/backend`
(Akim's project-agent tooling). Existing CH1 documentation edits are preserved.
