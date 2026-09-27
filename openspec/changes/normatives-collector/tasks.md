# Tasks

Branch: `feature/normative-collector/data` (Egor, data zone).

Executor tags: **[Egor]** data zone, **[Agent]** subagent.

## 1. Probe sources (research)

- [ ] 1.1 [Egor] Probe each registry (`faufcc.ru`, `fgiscs.minstroyrf.ru`,
  `minstroyrf.gov.ru`, `gost.ru`, `pravo.gov.ru`) and record the access mode (API vs SPA
  vs static HTML) in `docs/decisions/ml-model-journal.md`
- [ ] 1.2 [Egor] Assemble a 5-document pilot list (designation + edition) across document
  formats

## 2. Collector implementation

- [ ] 2.1 [Egor] Registry client for the first source (discovery + listing editions)
- [ ] 2.2 [Egor] Downloader (HTTP + Playwright) with retry, timeout, and sha256
- [ ] 2.3 [Egor] Metadata model + dedup by `(document, edition, sha256)`
- [ ] 2.4 [Egor] Storage: `dec_normatives` migration + local file store
- [ ] 2.5 [Egor] CLI entry point (`collect --source <name> --document <designation>`)

## 3. Tests and quality

- [ ] 3.1 [Agent: tester] pytest: registry parse, metadata, dedup; fixtures = sample
  pages; branch coverage >= 95%
- [ ] 3.2 [Egor] `ruff` + `mypy` clean

## 4. Validate and close

- [ ] 4.1 [Egor] `openspec validate normatives-collector --strict`
- [ ] 4.2 [Agent: spec-reviewer] Review; resolve blockers
- [ ] 4.3 [Agent: tester] Issue the GO/NO-GO verdict
- [ ] 4.4 [Egor] Merge to `develop`
- [ ] 4.5 [Agent: spec-keeper] Sync and archive

## Dependencies

- `norm-source-traceability` (WP3) finalizes the `dec_normatives` schema; the collector
  uses a provisional schema and reconciles when WP3 lands.
- `bootstrap-dev-environment` (WP6) provides Docker + PostgreSQL for local storage.

## DOR checklist

- [ ] `proposal.md`, `specs/…`, `design.md`, `tasks.md` exist
- [ ] `openspec validate --strict` passes
- [ ] Functional and non-functional requirements recorded
- [ ] Branch defined (above)
- [ ] Acceptance and Go/No-Go criteria written (below)

## DOD and Go / No-Go

- GO: the 5-document pilot is downloadable, metadata is stored, dedup is correct, registry
  recall >= 95% (H1), tests pass with >= 95% branch coverage.
- NO-GO: test failure, coverage < 95%, or a source that cannot be probed without a
  recorded fallback.
