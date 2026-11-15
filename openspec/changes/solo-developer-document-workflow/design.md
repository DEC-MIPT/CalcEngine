# Design

## Context

The current development-process specification distinguishes document commits on
develop from code work on feature branches, but does not explicitly require the
documentation edits themselves to occur on develop. Several current instruction
surfaces also assume two active developers and require a second-human-developer
acknowledgement for code-free closure. See `proposal.md` for the requested outcome.

Akim has explicitly reported that Egor left the team, that no replacement exists,
and that second-developer confirmations are no longer required. This report is the
source of the current roster decision; no departure date or replacement identity
is inferred. The PM's scope, pricing and legal authority remains unchanged.

`AGENTS.md` owns shared operating rules. `CLAUDE.md`, OpenSpec planning context,
instruction-only role/skill mirrors and the local context index must agree with
those rules. Existing decisions, source signatures and archived changes also
contain historical references to Egor; those records retain their provenance.

## Goals and non-goals

Make the documentation branch check apply before authoring, not only before
delivery. Make the current human roster and acknowledgement exemption explicit
without changing the engineering or independent agent quality gates.

This is documentation-only work on develop, with no feature branch. It changes no
application, numerical algorithm, runtime setting, dependency, database, deployment
behavior, model assignment or tool permission. It does not merge the module-contract
feature, grant a new normative approval, settle an unresolved technical decision,
restructure local history or automatically archive another change.

## Decisions

### 1. Verify the actual worktree branch before documentation edits

Before creating or modifying a document, verify that its worktree is on develop.
The same check applies before document commits and pushes. Document files use the
existing allowed-path classification with instruction-only Codex agent/skill
mirrors included consistently with Claude and Kilo definitions. Permission settings
remain code; `openspec/config.yaml` is planning-context documentation under the
existing `openspec/**` category.

If the worktree is on another branch, stop authoring documents there. Obtain or use
the developer's existing authorization to switch safely or use a worktree whose
actual branch is develop. Inspect tracked, staged, untracked and relevant ignored
work before switching. A refused switch is a preservation condition to resolve,
not permission for stash, reset, forced checkout, deletion or overwriting user work.
Do not create a document commit on the feature branch to bypass the refusal.

Where existing working document copies already match develop, their equality may
be verified before using a reversible index operation to permit the authorized
switch. Check the intended file set and contents before the operation and compare
preservation evidence afterwards. The approach must not fabricate a commit or
silently absorb unrelated staged work.

The alternative of preparing documents on a feature branch and later moving their
commit to develop is rejected because it does not satisfy the requested edit-time
rule. Receiving previously committed documents through an explicitly authorized
merge of develop into a feature branch remains the existing integration mechanism;
it is not authorization to author new document changes on that feature branch.

### 2. Keep one current roster and propagate its consequences

Record the supplied fact in a dated decision under `docs/decisions/`, with its
Russian counterpart, and reflect the current roster in `AGENTS.md`. Akim is the
only active developer and coordinates current implementation ownership. Technical
area names and existing branch suffixes remain stable; former ownership labels
do not make Egor an available reviewer or implementation owner.

Agent routing continues by the task's technical area. The sole-developer state
does not assign product/legal authority to Akim or permit unrelated implementation
outside the authorized task. With one identified developer, agents do not ask the
obsolete Akim-or-Egor question as a startup prerequisite.

A second active developer is recorded only when Akim announces one. At that point,
update the roster, responsibility assignment and applicable review/confirmation
rules explicitly. Do not infer a new member from a historical Git author, an old
zone label or a retained source signature.

The alternative of globally replacing Egor's name is rejected. Historical work,
answers, signatures and authorship remain historical evidence. Current routing and
future obligations use the current roster instead.

### 3. Waive the unavailable human confirmation, preserve independent gates

While Akim is the only active developer, second-human-developer acknowledgements
and confirmations are not required. The exemption applies to current operational
gates, including the code-free path. It is recorded as an exemption, never as a
signature or approval by Egor or an invented replacement.

Independent `spec-reviewer` findings, tester verdicts, code branch review by the
orchestrator where required, UI/UX checks for changed interfaces, branch coverage,
security and calculation-correctness gates remain applicable. The code-free path
still requires strict validation, a current clean specification review, appropriate
document checks and a tester verdict with individually justified tests, coverage
and UI/UX N/A fields. The sole developer's statement is not a substitute for any
agent verdict or engineering evidence.

Existing pending items that ask only for the unavailable second developer's
acknowledgement can be recorded as N/A under this policy, with a link to the dated
decision. Preserve their prior pending/NO-GO evidence as history and obtain current
reassessment where a verdict depended on that gate. Questions needing a real
technical, methodological or PM answer remain unresolved until their actual
decision is recorded. Removing a signature requirement does not answer a question.

No unrelated change is automatically GO, synced or archived. Each keeps its other
open tasks and closure conditions. Git commits, merges and pushes still require
Akim's separate explicit consent.

### 4. Reconcile instruction surfaces without changing permissions

Use the existing canonical/mirror relationships for role and skill instructions.
Update current statements about documentation authoring, developer selection,
ownership and human confirmation together. Preserve frontmatter, model/tool
metadata, generated instruction blocks, permission settings and historical notes.
Check serialized mirror syntax where applicable and inspect diffs for changes
outside instruction text.

The local index contains only a compact current policy pointer and unfinished-work
routes. The dated decision owns the roster fact and its provenance; OpenSpec owns
the requirements. Do not add another operational history log to the index.

## Component boundary and non-functional constraints

No calculation hot path changes, so a new Python-to-C/C++ boundary is not applicable.
The existing pure `Calculator.calculate` boundary and the five product components
remain unchanged. There is no runtime latency, API performance or storage impact
to measure for this documentation-only change.

Verification covers branch correctness, rule consistency, history/user-work
preservation, links, whitespace, instruction-mirror syntax and existing document
hooks. Application tests, numerical coverage and UI/UX are N/A because this change
contains no application code or interface changes. Real DB/catalog behavior is
outside this scope and is not claimed as verified.

## Risks and trade-offs

- A safe switch can be confused with a clean-tree reset. Preserve content and index
  evidence, inspect failures, and use no destructive cleanup shortcut.
- A mirror can keep an obsolete owner or acknowledgement rule. Compare all current
  instruction surfaces against the roster decision and shared rules.
- An exemption can be mistaken for engineering approval. Separate administrative
  confirmation tasks from actual technical decisions and retain independent gates.
- Historical references can look like current membership. Keep their historical
  context and route current work through the active roster.
- A future developer can join without updated ownership rules. Require Akim's notice
  and explicit roster/policy reconciliation before relying on multiple-developer
  assumptions.

## Migration and verification

1. Confirm develop and preserve existing tracked/untracked/local documentation.
2. Record the dated decision and current shared rules, then reconcile affected
   entry points, planning context and instruction-only mirrors.
3. Update active confirmation tasks with explicit exemption provenance; preserve
   old decisions and verdicts, and retain unresolved substantive obligations.
4. Validate the selected change and all OpenSpec artifacts, compare original
   scenarios in MODIFIED requirements, and run focused document checks/hooks.
5. Obtain current specification review and tester reassessment. Record actual
   results and N/A reasons without claiming unrelated changes have closed.
6. Leave commit, push, merge and archive actions to their applicable consent and
   lifecycle gates. Any main-spec synchronization must follow the existing workflow.

A correction to the roster or workflow must be a new explicit recorded decision;
silently restoring obsolete two-developer assumptions is not a rollback strategy.
No application or database rollback is needed because their contents do not change.
