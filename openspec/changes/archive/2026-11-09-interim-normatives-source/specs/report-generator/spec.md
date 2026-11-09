## ADDED Requirements

### Requirement: Parameter source line in the report
The report of a result whose envelope carries `parameter_source` SHALL print one line naming
the source of the norm-given parameters: for kind `interim` the words for the interim
normative data, the profile and the full data digest; for kind `catalog` the words for the
normative catalog. While the result accountability section is not printed, the line SHALL be
printed in the conclusion, immediately before the engineer-responsibility sentence; when that
section is printed, the line SHALL be printed there instead, extending the content of the
"Result accountability block" of `calculation-core-contract`, so that it appears exactly
once.
A result without `parameter_source` SHALL produce a report without the line.

#### Scenario: Interim line in the conclusion
- **WHEN** a report is built for a result computed on interim data in the `strict` profile
  while the accountability section is off
- **THEN** the conclusion holds one line with the interim data, `strict` and the 64-character
  digest, directly before the responsibility sentence

#### Scenario: Line printed once
- **WHEN** the accountability section is on
- **THEN** the line appears in that section and not in the conclusion

#### Scenario: Older result
- **WHEN** a report is built for a stored result without `parameter_source`
- **THEN** the report has no source line and is otherwise unchanged
