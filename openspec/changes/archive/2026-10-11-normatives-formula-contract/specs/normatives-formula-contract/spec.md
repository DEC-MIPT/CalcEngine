# Spec Delta

## Purpose
Defines the structured formula payload the normatives pipeline hands to the backend and
frontend: traceability, LaTeX, normalized symbols, and cross-references.

## ADDED Requirements

### Requirement: Formula payload
The system SHALL return a formula as a structured payload with a normative reference, LaTeX,
normalized symbols, an expression field, and cross-references, in a shape defined by config.

#### Scenario: Config-driven shape
- **WHEN** `output_config` is monkeypatched to return a config where `formula_keys = ['norm_ref', 'formula_id', 'latex', 'symbols', 'expression', 'cross_refs']` and `build_formula_payload` is called with a valid formula row dict and a mock connection whose cursor returns empty lists
- **THEN** the returned dict contains exactly the keys `norm_ref`, `formula_id`, `latex`, `symbols`, `expression`, `cross_refs`

#### Scenario: Missing config key raises error
- **WHEN** `output_config` is monkeypatched to return a config where `formula_keys = ['norm_ref', 'foo']` and `build_formula_payload` is called with a valid formula row dict and a mock connection whose cursor returns empty lists
- **THEN** the builder raises `KeyError` with key `'foo'` and never returns normally

### Requirement: Symbol normalization
The system SHALL normalize each notation symbol to an ASCII machine id and a canonical LaTeX
representation.

#### Scenario: Greek symbol
- **WHEN** a notation symbol is `γc1`
- **THEN** its id is `gamma_c1` and its latex is `\gamma_{c1}`

#### Scenario: PUA symbol mapped
- **WHEN** a notation symbol contains the PUA character `U+F061` (Symbol-font alpha, mapped to `\alpha` in `pua_map`)
- **THEN** its id is `alpha` and its latex is `\alpha`

#### Scenario: PUA symbol not in map
- **WHEN** a notation symbol contains a PUA character that has no entry in `pua_map`
- **THEN** `normalize_symbol` returns `None` and the symbol is not stored

#### Scenario: Garbage filter
- **WHEN** a notation symbol contains no alphabetic character and no PUA entry
- **THEN** `normalize_symbol` returns `None` and the symbol is not stored

#### Scenario: Subscript index
- **WHEN** `normalize_symbol('Рраб')` is called (first character `Р` is the base; remaining characters `раб` form the subscript)
- **THEN** its id is `R_rab_cyr` (`cyr_map` from `parser.toml` drives the ASCII transliteration for the id only) and its latex is `\text{Р}_{\text{р}\text{а}\text{б}}` (Cyrillic characters are preserved verbatim inside `\text{…}`)

#### Scenario: Cyrillic suffix
- **WHEN** `normalize_symbol('А')` is called (a bare Cyrillic letter)
- **THEN** its id is `A_cyr` (carries the `_cyr` suffix) and its latex is `\text{А}`

#### Scenario: Multi-symbol split
- **WHEN** a raw notation entry contains `γc1, γc2` (comma-separated)
- **THEN** `split_symbols` returns `['γc1', 'γc2']` (two strings, leading and trailing whitespace stripped)

### Requirement: Traceability reference
The system SHALL attach the agreed `NormRef` to each formula payload.

#### Scenario: NormRef fields
- **WHEN** `build_formula_payload` is called with a formula row dict where `designation`, `edition`, `status`, `provenance`, `clause_number`, `document_id`, and `number` are all set to valid non-empty values, and `conn` is a mock connection whose cursor returns empty lists for all SQL queries
- **THEN** the returned payload's `norm_ref` carries `document` (sourced from `designation`), `edition`, `clause`, `status`, and `provenance` as non-empty strings

#### Scenario: Internal id outside NormRef
- **WHEN** `build_formula_payload` is called with a formula row dict where `number = '13.8#1'`, `designation` and `document_id` are valid, and `conn` is a mock connection whose cursor returns empty lists
- **THEN** `payload['formula_id']` is `'13.8#1'` and `payload['norm_ref']` does not contain key `formula_id`

#### Scenario: Coefficient NormRef
- **WHEN** `build_coefficient_norm_ref` is called with a coefficient row dict where `designation`, `edition`, `clause`, `status`, and `provenance` are non-empty strings
- **THEN** the returned `norm_ref` carries `document` (from `designation`), `edition`, `clause`, `status`, and `provenance`

#### Scenario: Per-formula provenance
- **WHEN** `build_formula_payload` is called with a formula row dict where `provenance = 'machine-extracted'`, `designation` is non-empty, `document_id` and `number` are valid, and `conn` is a mock connection whose cursor returns empty lists
- **THEN** the returned payload's `norm_ref['provenance']` is `'machine-extracted'`

### Requirement: Ingestion validation
The system SHALL refuse to build a payload for a formula or coefficient that carries no
source document reference.

#### Scenario: Missing designation field refused
- **WHEN** `build_formula_payload` is called with a formula row dict that has no `designation` key
- **THEN** the builder raises `RuntimeError` and no payload is returned

#### Scenario: Empty designation string refused
- **WHEN** `build_formula_payload` is called with a formula row dict where `designation = ''`
- **THEN** the builder raises `RuntimeError` and no payload is returned

#### Scenario: Coefficient missing designation refused
- **WHEN** `build_coefficient_norm_ref` is called with a coefficient dict that has no `designation` key
- **THEN** the builder raises `RuntimeError` and no `norm_ref` is returned

#### Scenario: Coefficient empty designation refused
- **WHEN** `build_coefficient_norm_ref` is called with a coefficient dict where `designation = ''`
- **THEN** the builder raises `RuntimeError` and no `norm_ref` is returned

### Requirement: Inspectable return
The system SHALL expose the payload through a query function whose return value is the
serialized object, not console text.

#### Scenario: Query return type
- **WHEN** `search.query` is called with a non-empty query string, `db.connect` monkeypatched to return a mock connection, and `db.search_formulas` and `db.search_clauses` monkeypatched to return empty lists
- **THEN** it returns a `dict` containing the keys `query`, `lemmas`, `formulas`, `clauses`

#### Scenario: JSON CLI mode
- **WHEN** `search.main(['--json', 'нагрузка'])` is called with `search.query` monkeypatched to return `{'query': 'нагрузка', 'lemmas': [], 'formulas': [], 'clauses': []}` and stdout is captured
- **THEN** the captured stdout is a valid JSON string whose top-level keys include `query`, `lemmas`, `formulas`, `clauses`

### Requirement: Non-functional — no PDF read at query time
The system SHALL execute a formula search without reading PDFs at query time; `pdfplumber`
is used only during ingestion and is not reachable from the query path.

#### Scenario: Query path does not import pdfplumber
- **WHEN** the source files of `normatives_pipeline.search` and its transitive imports are examined
- **THEN** none of them imports `pdfplumber` or any PDF-reading library (verifiable by source inspection: `grep -r 'import pdfplumber\|from pdfplumber' ml/src/normatives_pipeline/search.py` returns no matches, and the same check on files transitively imported by `search.py`)

### Requirement: Non-functional — expression safety
The system SHALL never evaluate the formula `expression` field; all symbol identifiers
in the payload match the pattern `[A-Za-z_][A-Za-z0-9_]*`.

#### Scenario: Expression passed through unchanged
- **WHEN** `build_formula_payload` is called with a formula row containing `expression = 'E = m * c^2'`, required fields `designation`, `document_id`, `number` present, and `conn` is a mock connection whose cursor returns empty lists
- **THEN** the returned `payload['expression']` equals `'E = m * c^2'`

#### Scenario: Identifier safety
- **WHEN** `normalize_symbol` is called with representative inputs `'γc1'`, `'Рраб'`, `'k'`, and the PUA character `U+F061`
- **THEN** each non-`None` returned id matches `[A-Za-z_][A-Za-z0-9_]*` (starts with a letter or underscore, followed by ASCII alphanumeric characters or underscores)
