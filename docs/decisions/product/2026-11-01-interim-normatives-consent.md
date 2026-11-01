# Interim normative base: PM consent record

Recorded 2026-11-01 by the agent at Akim's instruction for
`interim-normatives-source`, task 9.4. Decision date: 2026-10-18.
Russian version: [consent record](2026-11-01-interim-normatives-consent-rus.md).

## Decision and attribution

According to Akim, the PM orally agreed on 2026-10-18 that the pilot may use an interim
normative base maintained in Akim's backend zone while the catalog is being completed.
This permits normative data in Git under `backend/interim_normatives/`, within the scoped
exception in [design decision 9](../../../openspec/changes/interim-normatives-source/design.md).
This is Akim's account of oral consent, not a direct quotation or a written PM signature.
The supplied plan does not identify the meeting or communication channel more precisely.

The account is already recorded in [readiness, Akim's decisions, item 8](../backend/2026-10-20-interim-normatives-source-readiness.md)
and design decision 9. Egor's separate written acknowledgement is in
[his Answers](../backend/2026-10-20-interim-normatives-source-ack-to-egor.md#answers).

## Use and limits

As checked on 2026-11-01, `feature/interim-normatives/backend` at `f33df61` contains the
source, manifest and pilot data. It has not been merged into `develop` at `34eb49a`.
This records feature-branch use; it does not claim a release or successful acceptance
of the real data in `strict`.

The sunset remains 2026-12-01, with the transition event defined in the manifest and
design decision 8. Extension requires a separate decision by Akim. The consent does
not supply verifier verdicts, feature GO, merge permission or permission to archive.
