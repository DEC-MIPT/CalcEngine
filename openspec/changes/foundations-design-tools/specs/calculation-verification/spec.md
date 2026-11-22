## ADDED Requirements

### Requirement: Foundation design-tool independent acceptance
The system SHALL preserve the admitted averaged-mode examples and pilot frozen corpus and SHALL verify the new load mode and search against independently derived engineer-approved references before feature GO. The applicable requirement for at least three complete references per new calculation type remains; For foundations_shallow_weights only, manual references MAY be admitted after Akim independently checks their full derivations and approves their expected results and tolerance provenance. Akim explicitly admitted weights-C, weights-X and weights-XY on 2026-11-22, with absolute tolerance 0.005 kPa for each R/pressure output, as recorded in reference-candidates.md. This exception does not admit other candidates or promote normative source status. Each added quantity requires approved expected value, unit, tolerance and provenance. Invariants SHALL cover one-time weight inclusion, equivalent units, zero/eccentric weights, cut/base transfer equivalence, mode equivalence for equal assembled resultants, candidate ordering/ties/exhaustion, determinism and unchanged stored-result identity.

#### Scenario: Competitor output is insufficient
- **WHEN** a numerical value is copied from a competitor, an inconsistent guide or the implementation under test without independent admission
- **THEN** it cannot satisfy the reference gate or justify changing a coefficient

#### Scenario: Candidate policy reproducibility
- **WHEN** the same admitted candidate request, methodology and source identity are run twice
- **THEN** candidate results, selection and deciding reason are identical except for permitted storage identifiers

#### Scenario: Regression differs
- **WHEN** the historical pilot or admitted averaged corpus changes outside the approved new-version scope
- **THEN** acceptance is NO-GO and the difference is reported without rewriting the baseline
