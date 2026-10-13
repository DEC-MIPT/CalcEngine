# Design

## Context

The collector is the first stage of the domain-agnostic normative pipeline. It must
produce a reproducible corpus of documents with stable metadata, so the parser and the
embeddings retrieval have a fixed baseline to measure against.

## Goals

- Fetch every edition and release of the pilot documents from authoritative registries.
- Store documents and metadata additively (revisions never rewritten in place).
- Deduplicate by (designation, edition, content hash).
- Run as a batch/CLI on CPU; no public API.

## Non-Goals

See `proposal.md`.

## Decisions

1. **Access: Playwright first, JSON-API where found.** `faufcc.ru` and
   `fgiscs.minstroyrf.ru` are JS-heavy SPAs (a plain HTTP GET returns only the page
   title), so `requests`+`BeautifulSoup` is not enough. Use a headless browser
   (Playwright) for the SPA registries, and prefer a documented or reverse-engineered
   JSON API when one exists. `pravo.gov.ru` exposes an official API; `gost.ru` and
   `minstroyrf.gov.ru` are probed per-source.
2. **Metadata schema.** `document` (designation, normal form), `title`, `edition`
   (`<YYYY>[+<N>]`), `amendment_no`, `status` (in force / superseded / withdrawn),
   `validity_date`, `source` (registry + URL), `sha256`, `fetched_at`.
3. **Additive storage.** Revisions are stored as new rows/versions; an existing revision
   is never rewritten in place (matches the `NormRef` immutability in
   `norm-source-traceability`).
4. **Dedup.** Key by `(document, edition, sha256)`; re-fetch only when the source
   changed. Registry recall is measured against a manually verified 6-document pilot
   list.
5. **Boundary.** The collector writes `dec_normatives` and the local file store only; it
   has no public API and does not serve search (Akim's backend does).

## Assumptions

- The authoritative registry list may change as sources are probed; per-source findings
  are recorded in `docs/decisions/ml-model-journal.md`.

## Non-functional requirements

- **Performance**: metadata requests time out in 30 s; file downloads time out in 120 s;
  up to 3 retries on transient network errors (delays: 2 s, 5 s, 10 s).
- **Security**: no credentials stored in code; base URLs and registry parameters read
  from environment via `Settings`; all downloads are HTTPS.
- **Coverage**: branch coverage >= 95% (actual: 100%, 2026-10-13).
- **Accessibility**: N/A — batch CLI tool, no UI.

## C/C++ hot-swap boundary

This component has no C/C++ hot-swap boundary. It is a batch/offline tool; its only
CPU-bound operation is sha256 computation, handled by Python's built-in `hashlib`
(backed by OpenSSL). No latency-sensitive inner loop exists in the collection path.
