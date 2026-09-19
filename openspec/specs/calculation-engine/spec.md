# Calculation Engine

## Purpose
Component 2: a verified calculation engine implemented in Python (NumPy/SciPy) that
executes engineering calculations deterministically, logs every step, and validates
each intermediate result. The architecture must allow hot-swapping hot paths to C/C++
later.

## Requirements

### Requirement: Deterministic verified calculation
The system SHALL execute engineering calculations with verified algorithms in Python
(NumPy/SciPy) that strictly follow the bound normative method.

#### Scenario: Run a beam deflection check
- **WHEN** an engineer enters inputs for the beam deflection check per SP 16.13330
- **THEN** the engine computes the result using the verified algorithm with no arithmetic
  drift and no ML influence

### Requirement: Step-by-step logging
The system SHALL log every calculation step, including formulas, value substitution,
and intermediate results, for later transparent display.

#### Scenario: Trace the calculation
- **WHEN** a calculation completes
- **THEN** every step, substitution, and intermediate result is available in the trace

### Requirement: Automatic correctness validation
The system SHALL automatically validate each intermediate result and produce a final
conclusion (for example "strength condition satisfied / not satisfied").

#### Scenario: Conclusion verdict
- **WHEN** a calculation completes
- **THEN** the engine returns a deterministic conclusion with the reason

### Requirement: Hot-swap boundary for C/C++
The system SHALL isolate computational hot paths behind a well-defined boundary so
they can be replaced with C/C++ implementations later without changing callers.

#### Scenario: Swap a hot path
- **WHEN** a hot path is later reimplemented in C/C++
- **THEN** callers remain unchanged because the swap happens behind the engine boundary

### Requirement: Typed input and output contract
The system SHALL define a typed input and output contract per calculation type
(inputs such as loads, geometry, and material grade; outputs such as the result,
trace, and conclusion), validated by schemas at the engine boundary.

#### Scenario: Typed calculation contract
- **WHEN** a calculation type is implemented
- **THEN** its inputs and outputs are defined as typed schemas so callers validate
  inputs before the engine runs and read outputs without reaching into engine internals

### Requirement: Non-functional — performance and accuracy
The system SHALL complete a typical calculation in under 30 seconds and SHALL achieve
99.9% accuracy for correct inputs.

#### Scenario: Fast and accurate
- **WHEN** a typical calculation runs with correct inputs
- **THEN** it completes in under 30 seconds with 99.9% accuracy
