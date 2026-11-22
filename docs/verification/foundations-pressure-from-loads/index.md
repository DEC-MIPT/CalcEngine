# Loads source verification portions

[LOADS-DB-1](LOADS-DB-1.md) isolates the basement-depth source item needed by
`foundations_shallow_loads`. Its [worksheet](LOADS-DB-1.yaml) contains only
`d_b_cap_2m`; the other nine items of D-1 are outside this portion.

The existing digitization tool generated the portion from the same A/B extraction
files as D-1. Its shown_digest matches the approved `D-1/d_b_cap_2m` item exactly.
The dictated verdict, verifier and review date were copied unchanged: `верно`,
`Akim`, `2026-11-08`. Generation on 2026-11-09 does not change that review date.
The extraction's only-B flag remains visible; this is not a claim that both
extractions independently supplied this record.

The generated eight-minute estimate is a planning heuristic: five minutes for a
formula record and three for an extraction difference. It is not measured review time.

The source is СП 22.13330.2016 with amendments 1-5, clause 5.6.7, explanation
of d_b for formula (5.7), PDF page 36. The source rule prepares a calculation
value for a physical basement deeper than 2 m. The new type accepts a prepared
input in 0-2 m and requests correction outside it, without automatic clamping.

Runtime promotion requires the signature and committed provenance described in
[the verifier rules](../README.md). It does not promote an unverified NormRef.
The source evidence and remaining readiness gates are recorded in the
[paired readiness record](../../decisions/backend/2026-11-08-foundations-pressure-from-loads-readiness.md).

## Browser acceptance

The [desktop browser matrix](browser-matrix.md) records the separate manual UI
compatibility evidence for frontend task 3.6. It does not change normative
source verification or the LOADS-DB-1 verdict.
