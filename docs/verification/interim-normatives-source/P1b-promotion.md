# Phase-1b promotion evidence

The mapping covers all eight records of the future calculation type. It transfers
the signed source verdicts from P1b-1; P1b-2 supplies separate control-point evidence.
The type remains unregistered and its stored conditions remain non-executable.

## Inputs and mapping review

The pending runtime input is
`backend/interim_normatives/sp-22-13330-2016/foundations_pressure_from_loads.yaml`
at `014467f`. The source sheet is [P1b-1.yaml](P1b-1.yaml), last committed by
signer Akim at `582ea84`. The separate [P1b-2.yaml](P1b-2.yaml) was last committed
by signer Akim at `1c580fd`. Both signatures and clean Git provenance were checked.

[P1b-1-items.yaml](P1b-1-items.yaml) preserves the exact displayed payloads.
Its source paths identify extraction provenance; reproduction uses this portable
file and requires no ignored local extraction archive or source PDF.
[P1b-runtime-mapping.yaml](P1b-runtime-mapping.yaml) identifies each target list,
index, record digest and signed item digest.

Each `shown_digest` is the SHA-256 of UTF-8
`json.dumps([shown_payload], sort_keys=True, ensure_ascii=False, separators=(',', ':'))`.
This display hash differs from the record digest algorithm. The latter uses the
backend canonical JSON of the record without `verification`.

| Signed item | Runtime target | Projection checked |
|---|---|---|
| P1B-A01 | table_values[0] | Common provenance fields, parameter, symbol, value and unit |
| P1B-A02 | formulas[0] | Common fields, result symbol, LaTeX, expression tree and units |
| P1B-A03 | formulas[1] | Common fields, result symbol, LaTeX, expression tree and units |
| P1B-A04 | formulas[2] | Common fields, result symbol, LaTeX, expression tree and units |
| P1B-A05 | table_values[1] | Common fields, parameter, symbol, value and unit |
| P1B-A06 | table_values[2] | Common fields, parameter, symbol, value and unit |
| P1B-A07 | applicability_conditions[0] | Common fields, quantity, relation, exact fraction, unit and LaTeX |
| P1B-A08 | diagram_cases[0] | Common fields, units, three cases and separate caption expressions |

Common fields are `norm_refs`, `page` and `parameter`. Table `latex` equals the
source symbol and optional headings are null. The applicability `applies_to`
identifier comes from the source clause. Diagram `condition_latex_as_printed`
maps to `condition_latex`; absent edge ordinates become null. These schema
projections preserve the signed content. Reference status and provenance remain unchanged.

Independent review on 2026-11-08 (`phase1b_review`): **APPROVE**, zero blockers,
zero major and zero minor findings. The reviewer independently reproduced all
eight display hashes, checked every projection, confirmed unique complete mapping
coverage and compared backend/tool record digests. The pending YAML equals the
reviewed input. Promotion was authorized to proceed after this mapping review.

## Reproduction

Use a clean `develop` checkout containing the signed sheets and these evidence files.
Set `CH1_DOCS` to that checkout, `CH1_BACKEND` to the backend feature checkout,
`CH1_TOOLS` to the digitization checkout at `973f416`, and `CH1_PYTHON` to the
existing backend virtual environment's Python executable. Choose new output paths
for `CH1_DRAFT` and `CH1_OUTPUT`; the command never overwrites the runtime input.

```bash
git -C "$CH1_BACKEND" show 014467f:backend/interim_normatives/sp-22-13330-2016/foundations_pressure_from_loads.yaml > "$CH1_DRAFT"
PYTHONPATH="$CH1_TOOLS/tools/digitization" "$CH1_PYTHON" -m extractcmp promote \
  --draft "$CH1_DRAFT" \
  --mapping "$CH1_DOCS/docs/verification/interim-normatives-source/P1b-runtime-mapping.yaml" \
  --manifest "$CH1_BACKEND/backend/interim_normatives/sp-22-13330-2016/manifest.yaml" \
  --out "$CH1_OUTPUT" \
  "$CH1_DOCS/docs/verification/interim-normatives-source/P1b-1.yaml"
```

Require eight successful report lines and eight effective `human-verified` statuses.
Compare the parsed output with the runtime file, then compare both with the pending
input after removing only `verification`. Record digests must remain unchanged;
the document digest must change. A zero process exit code alone does not establish
complete promotion: the report must contain no skipped or pending target.

P2b-1 remains an unsigned empty correction template. A content correction requires
another verifier decision and re-check before promotion. The source sheets and their
signatures must remain unchanged.

## Promotion result and continuation review

The existing CLI produced eight successful promotion lines on 2026-11-08, with no
skipped or pending target. Independent final review (`phase1b_review`): **APPROVE**,
zero blockers, zero major and zero minor findings. Reproduction from the pending
input, checked mapping and signed P1b-1 yields the exact parsed runtime file.

All eight records have effective status `human-verified`, signer Akim, portion P1b-1
and their current record digest. Only verification fields changed. The pilot YAML
is byte-identical to `479172e`, and all 146 pilot records retain their digests.
The extension and promotion introduce no API, engine or UI changes. The updated
real-data test checks effective status, signer, portion, digest and reference status.

The tester's GO is recorded in the paired CH1 readiness record. Commit `dd0fd15`
contains the promoted file and its acceptance test. Task 9.3a still requires
approved integration and checks on the actual integrated `develop`.
