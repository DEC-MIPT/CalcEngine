# Current developer roster and develop-only documentation work

- Recorded: 2026-11-15.
- Source: Akim's explicit instruction in the working conversation.
- Change: `solo-developer-document-workflow`.
- Russian version: `2026-11-15-solo-developer-document-workflow-rus.md`.

## Decision

All documentation authoring, commits and pushes take place only in a checkout of
`develop`. This includes `docs/`, `openspec/`, AGENTS.md, README.md, other files on
the document list, ignored local reports and code journals. The branch must be
checked before a documentation write. Committing documents to develop later does
not authorize preparing their content on a feature branch.

Egor has left the team. Akim is the sole active developer and no replacement has
joined. Confirmation from a second human developer is not required while this mode
applies, including for existing pending acknowledgement tasks. Akim will announce
a new second developer; record that announcement and the applicable ownership and
review rules before applying new team assumptions. The actual departure date was
not supplied; the recording date above is not a claim about that date.

## Operational scope

Akim is the current working contact and coordinator for all development domains.
Existing technical boundaries and feature branch zone suffixes remain in use.
The PM retains scope, pricing and legal decisions. This record does not transfer
those product rights or settle any engineering methodology question.

Instruction-only agent and skill definitions, including Codex Markdown and role
TOML instruction mirrors, are documentation like their Claude/Kilo counterparts.
Editing native permission settings, runtime configuration/rules, infrastructure,
application code, tests or package manifests remains code work under the existing
feature-branch policy. No model, tool or permission grant is changed by this decision.

Reading documents on a feature branch and importing versions already committed
on develop through an explicitly authorized merge are not new authoring. When
coding on a feature branch, use a separate checkout of develop for journals and
specification edits, or an authorized safe branch switch. Do not force checkout,
reset, stash, discard work or commit documents on the feature branch as a workaround.

## Gates and history preserved

Independent spec-reviewer, tester and orchestrator reviews, applicable UI/UX,
coverage, security, source verification and calculation correctness gates remain.
Only the unavailable second-human-developer confirmation is waived. Tester remains
the GO authority. Commit, merge, push, spec synchronization and archive do not
occur merely because a pending acknowledgement is no longer required.

Record obsolete pending confirmation tasks as not applicable under this policy;
do not fabricate Egor's acknowledgement or mark other work complete. Technical
questions formerly addressed to Egor still need evidence or Akim's applicable
decision. Preserve past authorship, signatures, approvals and archived records.

## Branch transition evidence

The initial requested switch from feature/calculation-module-contract/backend to
develop was refused because seventeen document paths would be overwritten.
Their contents were independently compared with develop and matched exactly.
Only those matching paths were staged to permit the switch. The repeated switch
succeeded; all twenty-four preserved document versions were unchanged and the
staging area was empty on develop. No stash, reset, forced switch, commit or merge
was used. Pull --ff-only on develop reported already up to date. The feature code
remains preserved in its existing commit and was not integrated by this operation.

This policy is authored on develop. New commits and pushes require separate consent.
