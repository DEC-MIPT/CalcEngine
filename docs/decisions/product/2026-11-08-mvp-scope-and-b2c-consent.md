# MVP scope, non-goals and B2C limit: PM decision record

Recorded on 2026-11-08 from Akim's account in the current project conversation.
Decision date reported by Akim: 2026-10-19.
Russian version: [decision record](2026-11-08-mvp-scope-and-b2c-consent-rus.md).

## Decision and attribution

Akim reports that the PM gave approval during a meeting or call on 2026-10-19.
In this conversation, Akim confirmed the non-goals and B2C limit and clarified the
delivery boundary of the two domains. This record is Akim's account of the PM's
decision. No direct PM quotation, written signature or meeting transcript was supplied.

The approved product boundary is:

- The MVP must deliver the full calculation of a shallow foundation by the second
  group of limit states. The existing design-resistance calculation R is the delivered
  first stage; R alone does not satisfy the clarified MVP goal.
- Internal water supply follows as a separate post-MVP stage. It is the second domain
  in the product sequence, rather than a required delivery within the first MVP.
- Before the defense, billing/payment integration, generative-LLM structured extraction
  from norms, PDF report output and a multi-tenant audit trail remain non-goals.
  The normative NLP/RAG pipeline remains in the MVP; no ML enters the calculation path.
- The proposed B2C limit of 100 calculations per month is approved. After that limit,
  further calculations are blocked until the limit resets or the plan is upgraded.

The foundation scope and post-MVP water-supply boundary were explicitly clarified
by Akim in this conversation on 2026-11-08.

## Effect on requirements

This decision supplies the PM input for `retarget-mvp-domain` task 1.4.
Its current R-only scope and complementary out-of-scope wording require a coherent
revision before current-version review and acknowledgement. The existing natural-base
boundary is not broadened by this record. Engineering methods, applicability limits,
inputs, outputs and independent control values require their own reviewed calculation
contracts before implementation. This product decision supplies none of those choices.

The record does not assert that the full foundation workflow is implemented or accepted.
It does not supply Egor's acknowledgement, a tester GO, archive permission or consent
to commit, merge or push. The separate interim-source consent of 2026-10-18 remains
in [its original record](2026-11-01-interim-normatives-consent.md).
