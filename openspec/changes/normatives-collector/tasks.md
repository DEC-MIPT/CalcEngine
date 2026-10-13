# Tasks

Branch: `feature/normative-collector/data` (Egor, data zone).

Executor tags: **[Egor]** data zone, **[Agent]** subagent.

## 1. Probe sources (research)

- [x] 1.1 [Egor] Probe each registry (`faufcc.ru`, `fgiscs.minstroyrf.ru`,
  `minstroyrf.gov.ru`, `gost.ru`, `pravo.gov.ru`) and record the access mode (API vs SPA
  vs static HTML) in `docs/decisions/ml-model-journal.md`
  (journal entries 1-4: faufcc=JSON API, fgiscs=JSON API, pravo=REST; Playwright NOT
  needed for faufcc; minstroyrf=HTML scraping; results in journal entries 1, 3, 4, 6)
- [x] 1.2 [Egor] Assemble a 5-document pilot list (designation + edition) across document
  formats
  (6-document pilot list in `SP_TARGETS` dict in `collector/cli.py`: СП 22, 24, 45, 30,
  31, 32; journal entry 12)

## 2. Collector implementation

- [x] 2.1 [Egor] Registry client for the first source (discovery + listing editions)
  (`FaufccRepository` in `collector/repositories/faufcc.py`: JSON API search + download;
  `PravoRepository` in `collector/repositories/pravo.py`; `FgiscsRepository` in
  `collector/repositories/fgiscs.py`)
- [x] 2.2 [Egor] Downloader (HTTP + Playwright) with retry, timeout, and sha256
  (HTTP + retry in `services._download_with_retry`; sha256 in `storage.save`;
  Playwright deferred — all current sources are JSON APIs, not SPAs)
- [x] 2.3 [Egor] Metadata model + dedup by `(document, edition, sha256)`
  (`Document.edition` field added; `FileStorage.save` deduplicates by sha256)
- [x] 2.4 [Egor] Storage: `dec_normatives` migration + local file store
  (local `FileStorage` done; `dec_normatives` migration deferred to WP3 per
  Dependencies)
- [x] 2.5 [Egor] CLI entry point (`collect --source <name> --document <designation>`)
  (`cli.main(argv)` with `--source {faufcc,pravo,all}` and `--document DESIGNATION`)

## 3. Tests and quality

- [x] 3.1 [Agent: tester] pytest: registry parse, metadata, dedup; fixtures = sample
  pages; branch coverage >= 95%
  (34 tests in `ml/tests/test_collector.py`; collector package branch coverage 100%;
  all 34 pass)
- [x] 3.2 [Egor] `ruff` + `mypy` clean
  (ruff 0 errors, mypy 0 errors on collector + tests)

## 4. Validate and close

- [x] 4.1 [Egor] `openspec validate normatives-collector --strict`
  (passes: 2026-10-13)
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
