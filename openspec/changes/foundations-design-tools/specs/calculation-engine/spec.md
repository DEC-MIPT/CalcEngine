## ADDED Requirements

### Requirement: Foundation design load assembly
The system SHALL calculate design-tool requests through the existing pure module boundary, using an explicit versioned load-assembly contract. The proposed first explicit-weight type SHALL identify second-limit-state structural loads at the upper cut, with separately named added moments already at the base. It SHALL NOT silently interpret base-level structural loads as upper-cut loads. Supporting both load levels requires an independently typed variant and approved methodology identity before implementation. The averaged variant SHALL preserve N/A+gamma_mt*d under its original methodology. The explicit-weight variant SHALL assemble N_base=N+sum(G_i), p=N_base/A and the agreed signed base moments, with no averaged allowance. Each supplied weight and moment SHALL have explicit units and engineer attribution. Changing methodology SHALL create a distinct versioned identity and SHALL NOT rewrite prior stored runs.

Source: Akim's confirmation on 2026-11-22; vertical resultant and signed-moment assembly are EngineerRules approved through the three checked reference derivations and final admission. Akim additionally confirmed strictly positive N_base before calculation on 2026-11-22. The averaged component remains prepared SP 22.13330.2016, edition 2016 with amendments 1-5, clause 5.6.28 formula (5.11). Geometry, signed transfer, full contact and four ordered checks retain their existing approved sources and rules.

#### Scenario: Equivalent assembled vertical force
- **WHEN** independently approved explicit weights sum to the averaged allowance for identical geometry and signed base moments
- **THEN** both modes produce the same unrounded pressure distribution and ordered check outcomes under the same R

#### Scenario: Asymmetric added weights
- **WHEN** an explicit weight has a nonzero signed moment contribution
- **THEN** the contribution is included exactly once under the approved axis convention and is visible in the trace

#### Scenario: Historical identity remains stable
- **WHEN** a pre-change averaged result is retrieved or replayed under its original methodology
- **THEN** no new mode field is required in that historical envelope and its original identity is preserved

### Requirement: Positive explicit-weight vertical resultant
The system SHALL require N_base=N+G_fund+G_soil+G_other to be strictly positive after unit normalization for foundations_shallow_weights. All four components remain nonnegative. A nonpositive resultant SHALL produce invalid_input with named contributing inputs before any calculation or eccentricity division, independently of the supplied moments. This rule SHALL NOT change the averaged-weight type.

Source: Akim's explicit engineering decision in the working conversation, 2026-11-22, confirming N_base>0 and invalid_input before calculation for N_base<=0. This is an engineer-defined domain restriction, not a new normative coefficient.

#### Scenario: Zero force and zero moments
- **WHEN** the explicit-weight request has zero N and zero added weights, with zero moments and shears
- **THEN** it is rejected as invalid_input before calculation and no zero-pressure success is stored

#### Scenario: Zero force with a moment
- **WHEN** the explicit-weight vertical resultant is zero and a cut or added moment is nonzero
- **THEN** it is rejected as invalid_input before eccentricity division, not as a completed pressure result

#### Scenario: Positive added weight with zero structural force
- **WHEN** N is zero and at least one valid downward added weight is positive
- **THEN** the positive-resultant guard passes and ordinary method/contact checks still apply
