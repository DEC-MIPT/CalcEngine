# Readiness review: `team-roles-update` (WP7)

- Date: 2026-09-26
- Change: `openspec/changes/team-roles-update/`
- Author: Akim. Egor is the second developer and must agree, because the change touches shared files.
- Criteria: `docs/audit/03-verified-roadmap.md`, section 3.7, "Ready when": Egor agrees, and validate passes.

## Final status

**READY FOR TEAM DISCUSSION**

Technically ready, waiting for Egor's agreement. After the third `spec-reviewer` pass there are 0 blockers, 0 major and 0 new minor findings, and `openspec validate --all --strict` passes 14/14. Egor has not agreed yet. That is a separate roadmap condition, so this is not "ready to archive": the change stays open until Egor acknowledges it (task A1.4) and Part B is applied or its deferral is recorded (task A2.3).

| Roadmap criterion (3.7) | State | Evidence |
|---|---|---|
| `openspec validate` passes | Met | 14/14, section 1 and section 8 |
| Egor agrees (shared files) | **Open** | no acknowledgement recorded; task B1 not started |
| (DOR, A13) `spec-reviewer` with no blocker and no major finding | Met | section 8 (third pass); earlier passes in sections 2 and 7 |

Sections 1-6 record the first pass and are kept as history; the status above supersedes their NOT READY.

## 1. `openspec validate --all --strict`

```
- Validating...
✓ change/backend-layered-architecture
✓ change/calculation-core-contract
✓ spec/calculation-engine
✓ spec/development-process
✓ spec/normatives-catalog
✓ spec/product-vision
✓ change/record-installed-skills-akim
✓ spec/report-generator
✓ change/retarget-mvp-domain
✓ spec/security
✓ change/team-roles-update
✓ spec/transparent-output
✓ spec/user-accounts
✓ spec/web-platform
Totals: 14 passed, 0 failed (14 items)
```

Validate checks structure only (finding A13), so this says nothing about content.

## 2. `spec-reviewer` report

Verdict: NOT READY. One pass, on the current version. `openspec validate` was not run by the reviewer. The reviewer did not read the `tester` and `spec-reviewer` agent definitions, so a conflict with the N/A record there is unchecked.

### Blocker

1. **The code-free rule does not literally close the `record-installed-skills-akim` blocker** (`design.md:65-70`; `record-installed-skills-akim/tasks.md:13,15,39-43`). The record change's DOD has the `tester` issue a verdict "no code, no tests, coverage not applicable". The new spec requires the fields `tests: N/A`, `coverage: N/A`, `UI/UX: N/A`, each with a reason, and a verdict without them is NO-GO. A tester who follows the record change's DOD text produces a verdict that is NO-GO under the new rule. Also, task 1.5 (Egor's acknowledgement) is defined but not removed, and the rule works only after this change is archived. `design.md` claims "its own tasks and DOD need no rewrite", which is false as written. Fix: align the wording in that DOD, or state in `design.md` that the verdict uses the exact N/A fields, drop the "no rewrite" claim, and state the order (archive this change, then 1.5, 1.6, 1.7).

### Major

2. **"No blockers" is defined differently in `design.md:43-44` and in the spec (`spec.md:27-29,37,66-67`).** The design means no blocker and no major; the spec never says. This decides a real case: the record change's last review was "NOT READY, 3 major", with no blockers. Fix: define it in the requirement.
3. **The tracked-sources rule conflicts with `agent-docs/domain-constraints.md`** (`spec.md:99-102`). Norm citations name primary-source documents (SP, GOST), which git does not track. The scope is also unclear: `proposal.md` is not clearly covered. Fix: limit the rule to decision rationale, exclude norm citations, state whether `proposal.md` is covered.
4. **The change breaks its own rule** (`proposal.md:9` and other `docs/audit/` references). `.gitignore` tracks only `docs/decisions/**` and `docs/reports/**`; `docs/audit/` is untracked (I confirmed this in `.gitignore`), so a reviewer cannot open D8, E5, A13, D2. Fix: restate the findings inline or move them to a tracked path.
5. **After archive, the specs contradict `AGENTS.md`** (sections 3-5). `AGENTS.md` calls itself the single source of truth. Part B fixes it but sits outside GO, so the contradiction can persist. Fix: state the order or a deadline for Part B, and record the risk in `design.md`.

### Minor

6. The PM's approval has no defined form or tracked artifact (`spec.md:15-18`).
7. "Author", the form of the acknowledgement (PR comments are not tracked by git), and its link to the current version of the change are not defined (`spec.md:65-68`; `design.md:34-37`). This change is itself co-developed with Egor.
8. The "no code" path list omits `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `README.md`, so Part B of this change would count as code, while `AGENTS.md:38-40` calls repo-meta files not product changes (`spec.md:63-65`).
9. The untracked-citation scenario names no checker or command (`spec.md:110-112`).
10. `tasks.md`: A1.1 is unchecked though the files exist; A3.2 and A3.3 ("Decide whether...") have no observable outcome; the NFR "not applicable" line does not list security and accessibility.

Reviewer's passes: all four MODIFIED blocks repeat the full requirement text and match the main headings; every SHALL has a scenario; the proposal and the delta list the same capabilities; Non-goals exist; the record change's delta only ADDs, so it does not conflict on archive.

## 3. Does this change unblock `record-installed-skills-akim`?

Current blocker text (`record-installed-skills-akim/tasks.md`):
- Task 1.5: "Get Egor's acknowledgement, because `openspec/` is shared; recorded as a commit or comment by Egor that names this change".
- Task 1.7: "`tester` issues the verdict for this change (see DOD)".
- DOD: "`tester` issues an explicit verdict 'no code, no tests, coverage not applicable'", and GO when validate passes, `spec-reviewer` reports no blockers, Egor has acknowledged, and the record check passes.

Result: **partly, with gaps.** What the new rule closes: the main spec `development-process` (Go/No-Go requirement) defines GO only through tests, coverage, and UI/UX, so today the `tester` has no code-free path and that DOD conflicts with the main spec. The new requirement supplies the path, and its three conditions (validate, `spec-reviewer`, acknowledgement by the non-author) match those in that DOD. Its acknowledgement form (a commit or comment by Egor that names the change) matches task 1.5.

Gaps, checked against the text:
1. **Wording of the verdict.** The DOD says "no code, no tests, coverage not applicable"; the new rule requires `tests: N/A`, `coverage: N/A`, `UI/UX: N/A` with reasons. Following the DOD literally gives NO-GO (reviewer finding 1).
2. **Task 1.5 is not removed.** The rule keeps Egor's acknowledgement as a GO condition. It gives that wait a definition; it does not end it.
3. **Timing.** The rule is normative only after this change is archived. Until then the `tester` verdict for the record change still contradicts the main spec. That change's "Dependencies: None" is then no longer accurate.
4. **"No blockers".** The record change's last review had 3 major and no blockers (task 1.4). Whether 1.6 passes depends on the definition in finding 2.
5. **Extra conditions stay.** The record check (lock file comparison) is stricter than the minimum rule; that is compatible.

Conclusion: the rule closes the missing-path part of the blocker, not the acknowledgement wait, and only after the fixes to findings 1 and 2 and the archive of this change.

## 4. Follow-up edits to shared files (to be discussed with Egor)

These are not part of the spec delta and are not applied by `apply`. Each needs Egor's agreement (task B1).

| # | File | Current text | Needed edit |
|---|---|---|---|
| 1 | `openspec/config.yaml:32` | "Team: two developers, Akim (...) and Egor (...). Ask who is working before development." | Three-person team: Akim, Egor, and a PM with no code zone; PM owns scope, pricing, legal. Keep "ask who is working" for the two developers. |
| 2 | `openspec/config.yaml` (Conventions) | no note on validate | One line: `openspec validate` is structural; readiness also needs a `spec-reviewer` report without blockers. |
| 3 | `AGENTS.md:104` (section 5) | "Two developers work on this project: **Akim** and **Egor**." | Three-person team; add a PM row to the zone table; say the PM has no agent unless a later change adds one. |
| 4 | `AGENTS.md` section 3 (DOR, line 68) | no `spec-reviewer` item | Add the item and one sentence that `openspec validate` is structural. |
| 5 | `AGENTS.md` section 4 (line 83) and section 2, step 7 (line 45) | GO only by tests, coverage, UI/UX; review after GO | Add the code-free GO path and the `tester` N/A record; state that for a code-free change the second developer's acknowledgement is the review. |
| 6 | `CLAUDE.md:69` | "`docs/` is untracked by design" | Stale: `docs/decisions/` and `docs/reports/` are tracked. Reword; Akim's file, shown as a diff. |

Questions for Egor: agree with a PM without an agent or zone (item 3)? Agree with the definition of "no code" by paths, and whether `AGENTS.md`-type repo-meta files fall inside it (finding 8)? Agree that "no blockers" means no blocker and no major (finding 2)?

## 5. Effect on WP1, WP2, WP3

The DOR is defined in no spec and no change today, only in `AGENTS.md` section 3, so this change creates its first spec definition.

- WP1 (`retarget-mvp-domain`) and WP2 (`calculation-core-contract`) already carry a DOR checklist and use `spec-reviewer`, so nothing conflicts. They may cite the new requirement after the fact (task A3.2). Neither needs to change to stay valid.
- WP3 does not exist yet. It should cite the DOR requirement when created (task A3.3).
- `record-installed-skills-akim` needs a re-run of tasks 1.5-1.7 after archive (section 3), and its "Dependencies" line should name this change.
- Untracked-source rule: WP1 and WP2 reports and readiness files cite `docs/audit/`, which is untracked. If finding 4 is fixed by moving the findings to a tracked path, they benefit from the same fix.
- `backend-layered-architecture` still cites "the passport" (`proposal.md:6`; `design.md:5,20,55,64`); tasks A2.1-A2.6 stay with that change's owner.

## 6. Next steps

1. Fix findings 1-5 (Akim, in the spec delta, `design.md`, and `tasks.md`), then re-run `spec-reviewer` and validate.
2. Only then put the shared-file edits to Egor (section 4) and get his acknowledgement.
3. Status becomes READY FOR TEAM DISCUSSION once no blocker remains and validate passes; it becomes ready for archive only with Egor's agreement.

## 7. Second pass (after fixing findings 1-5)

Status stays **NOT READY**. `openspec validate --all --strict`: 14/14. Egor has not agreed.

| First-pass finding | State |
|---|---|
| 1 (blocker) verdict wording and blocker closure | Resolved: `design.md` separates what is closed from what is not, and states the exact N/A fields |
| 2 "no blockers" definition | Resolved in spec, design, tasks |
| 3 tracked-sources rule vs norm citations | Resolved: norm citations excluded, scope limited to rationale |
| 4 untracked `docs/audit/` cited | Resolved: findings restated in `proposal.md` |
| 5 specs vs `AGENTS.md` | Mostly resolved: archive gated on Part B or a recorded deferral; a deferral leaves the contradiction as an accepted risk |

New findings: 0 blockers, **1 major**, 3 minor.

- **Major:** circular task order against the DOD (`tasks.md:36,62,85`). DOD requires all tasks checked before archive, but A3.1 needs A4.3 (the archive), and the A2 tasks belong to another change's owner and gate nothing. Fix: move A2 and A3 to a "follow-ups after archive" list, or state that they do not gate GO or archive, and make "Dependencies" consistent.
- Minor: "Dependencies: None" then lists dependencies, and the DOR item is checked while B1, A1.4, A4.1 are open.
- Minor: the Part B target text for the `AGENTS.md` DOR says "without blockers", so applying it literally would bring back the old inconsistency. Use the "no blocker and no major" definition there.
- Minor: `design.md:71-75` says the new rule has "the same three conditions" as the DOD of `record-installed-skills-akim`, but that DOD also has a fourth (the record check) and says "no blockers". Task A3.1 should also align "no blockers" and note that the record check stays as an extra condition.

The five minor findings from the first pass (PM approval form, "author", "no code" path list, untracked-citation check, task details) were left open on purpose and are unchanged.

## 8. Third pass (after fixing the circular task order)

Verdict: **READY for DOR**. Blocker 0, major 0, new minor 0. `openspec validate --all --strict`: 14/14. The reviewer did not run validate and did not re-verify the `[PM]` tag reference in `retarget-mvp-domain/tasks.md` (task 1.4).

- Circular order (major): resolved. Order is A2.1 verdict, A2.2 merge, A2.3 archive; A2.3 needs B8 or Egor's recorded deferral of Part B. The follow-ups for other owners are now section C without checkboxes and do not gate GO or archive.
- "Dependencies: None" and the DOR item (minor): resolved.
- Part B target text for the `AGENTS.md` DOR (minor): resolved; it now says "no blocker and no major finding".
- "Same three conditions" (minor): resolved; the record check stays as an extra condition of `record-installed-skills-akim`.

Five older minors remain open on purpose: PM approval form; definition of "author"; the "no code" path list (`AGENTS.md`, `CLAUDE.md`, `.gitignore`, `README.md`, `.editorconfig` are not on it); no mechanical check for untracked citations; terse tasks B2-B7 and C1.

What still needs Egor: the shared-file edits in section 4, and his acknowledgement of the change. Two of those minors touch his decisions: the "no code" path list and the PM approval form.

## 9. Update 2026-09-27: "no code" path list, fourth pass

Trigger: `AGENTS.md` (Branching rules, commit `e484a42`) now names `AGENTS.md` a no-code document, while the delta's "no code" path list left it out. Old minor 8 became a direct contradiction.

Edits:

- `specs/development-process/spec.md` ("Go/No-Go verdict and archive") and `design.md` decision 2: the list now covers everything under `.claude/`, `.kilo/`, `.kilocode/` (agent and skill definitions and agent settings) and the repository documents `AGENTS.md`, `CLAUDE.md`, `README.md`, `.editorconfig`. `.gitignore` stays off the list. The design states which of these `AGENTS.md` names and that `README.md` is added by this change.
- `proposal.md` and task B2: `openspec/config.yaml:31-33` became `:36-38` (the file changed since); the quoted current text is updated.
- Task A1.2 checked (validate re-run: 17/17). The DOR item for validate checked.
- Questions for Egor (A1.4, B1, the path list, the PM approval form, Part B timing): `docs/decisions/team-roles-update-egor.md` and `-rus.md`.

`openspec validate --all --strict`: 17 passed, 0 failed (17 items).

### Fourth pass: 0 blockers, 2 major, 3 minor

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Major | `design.md` decision 2 said all four repository documents are ones `AGENTS.md` already treats as repo-meta or no-code; `README.md` is not in `AGENTS.md`, and `CLAUDE.md` is covered only as an "agent entry file" | Fixed: the design names what `AGENTS.md` says for each file and states that `README.md` is added here |
| 2 | Major | A1.2 and A1.3 cited a fourth pass that this file did not record | Fixed: this section records it; A1.3 stays open until the fifth pass |
| 3 | Minor | DOR items for validate and review unchecked while A1.2 and A1.3 were checked | Fixed: the validate item is checked; the review item follows A1.3 |
| 4 | Minor | The list limited `.claude/`, `.kilo/`, `.kilocode/` to agent and skill definitions, narrower than "agent settings" in `AGENTS.md` | Fixed: agent settings are on the list; the questions file asks Egor to confirm, because settings can hold hooks that run commands |
| 5 | Minor | `docs/reports/WP7_report.md` stops at the third pass | Not changed: this file is the readiness record the tasks cite |

Checks that passed: the scenario "Change touches code" reads correctly with the longer list; every "Current text" cell of the shared-files table matches `openspec/config.yaml`, `AGENTS.md`, and `CLAUDE.md` today.

### Fifth pass: 0 blockers, 0 major, 0 minor

Verdict: **READY for DOR**. The pass first reported one blocker: that `AGENTS.md` does not name itself a no-code document. `AGENTS.md:73-74` reads "A change to `openspec/**` (specs and changes), `AGENTS.md`, or any other no-code document", so the finding was withdrawn on re-check. `design.md` decision 2 now quotes that sentence with its line numbers and cites `AGENTS.md:70` for repo-meta. The reviewer confirmed that fixes 1-4 of the fourth pass hold, that the path list is the same in the delta, the design, this section, and question 2 of `team-roles-update-egor.md`, that A1.2 is justified and A1.3 was correctly open, and that the questions file names the waiting tasks correctly. Task A1.3 and the DOR review item are checked.

What still needs Egor: the answers in `docs/decisions/team-roles-update-egor.md` (A1.4, B1, the path list including agent settings, the PM approval form, Part B timing).

## 10. Update 2026-09-27: Egor's answers, Part B, sixth pass

Egor answered `docs/decisions/team-roles-update-egor.md` (commit `243a6b9`): he acknowledged the change (A1.4), agreed to the "no code" path list except agent settings, which he put back under the normal gate because hooks run shell commands, agreed to the PM approval form, agreed to B2-B7, and asked for Part B right after, in one commit, before archive.

Edits:

- Delta: "Non-overlapping developer responsibility zones" gains how a PM decision is recorded and the scenario "PM approval recorded"; "Go/No-Go verdict and archive" drops agent settings from the no-code list. `design.md` decisions 1 and 2 match.
- Tasks A1.4 and B1-B8 checked. Part B applied to `openspec/config.yaml`, `AGENTS.md` (sections 2, 3, 4, 5, and one clause in "Branching rules"), and `CLAUDE.md`.
- `openspec validate --all --strict`: 17 passed, 0 failed.

### Sixth pass: 0 blockers, 0 major, 2 minor

Verdict: **READY for DOR**. The delta, `design.md`, and `tasks.md` agree; Part B restates the delta's path list, the three GO conditions, the N/A record, the DOR review rule, and the PM role without overstatement; every edit matches Egor's literal answers; the A1.4 acknowledgement stays valid, because the only later edits are the ones he asked for and the DOD requires acknowledgement, not a re-acknowledgement.

| # | Sev. | Finding | Outcome |
|---|---|---|---|
| 1 | Minor | `AGENTS.md` "Branching rules" still called agent settings repo-meta without a caveat, while section 4 now treats them as code for GO | Fixed: the bullet adds "A change that includes agent settings is still not code-free for GO (section 4)" |
| 2 | Minor | `CLAUDE.md` "Status" still said Egor's answers were awaited | Fixed: it now says Egor acknowledged the change and that spec-only changes can get their `tester` verdict |

Left: A2.1 (`tester` verdict), A2.2, A2.3 (archive).
