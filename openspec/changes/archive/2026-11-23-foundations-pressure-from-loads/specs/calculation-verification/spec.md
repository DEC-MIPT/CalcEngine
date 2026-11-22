## MODIFIED Requirements

### Requirement: Reference examples
The system SHALL ship every calculation type of the first domain (`foundations-shallow`)
with at least 3 reference examples. Each reference example SHALL record: `example_id`;
the calculation type; the inputs, each with its unit; the expected outputs, each with its
unit; for every expected output a `tolerance`, a `tolerance_kind` (`absolute` or
`relative`), and a `tolerance_source`; an `origin`, one
of `manual calculation`, `textbook`, or `norm application`; a source citation (the
document, its year, and the page or example number); and `source_norm_edition`, the norm
edition the example was calculated with, which may be the literal `unverified`. The
`tolerance` of each quantity is set by the engineer who fills the example; this
requirement fixes the fields, not a value. An output is within its tolerance when the
absolute difference between the computed and the expected value is not more than the
`tolerance` (`absolute`), or not more than the `tolerance` times the absolute expected
value (`relative`). The calculation types are those listed in the requirement "In-scope
calculation types" of the canonical capability `foundations-shallow`. For foundations-shallow, textbook examples from methodical guides remain required,
except that foundations_shallow_loads MAY additionally admit manual calculation
examples after Akim explicitly checks and approves their inputs, full intermediate
derivation, expected outputs/checks and per-output tolerances with provenance.
Akim conditionally authorized this exception on 2026-11-09: approval after his check.
It admits no candidate automatically and does not alter the pilot policy. Outputs
of the tested implementation SHALL NOT serve as independent expected results.
Agent arithmetic remains candidate evidence until independently engineer-checked.

#### Scenario: Reference suite within tolerance
- **WHEN** the reference suite runs and every output of every example is within its
  `tolerance` of the expected value
- **THEN** the reference check passes

#### Scenario: A quantity outside its tolerance
- **WHEN** the reference suite runs and any output of any example is not within
  its `tolerance`
- **THEN** the verdict is NO-GO, and the report names the example, the quantity, the
  computed value, the expected value, and the `tolerance`

#### Scenario: Too few or incomplete examples
- **WHEN** a calculation type has fewer than 3 reference examples, or an example lacks
  a `tolerance` or `tolerance_kind` for any expected output, an `origin`, a source citation, or
  `source_norm_edition`
- **THEN** the reference suite is invalid and the verdict is NO-GO

#### Scenario: Unapproved manual candidate
- **WHEN** a loads candidate has not received recorded engineer approval of its results and tolerances
- **THEN** it cannot count toward the minimum of three admitted examples or support a feature GO
