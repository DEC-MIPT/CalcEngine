# Proposal

## Why

The product needs a verified normative base, but today there is no automated way to get
normative documents (SP/GOST/SNiP) into `dec_normatives`: the specs still assume manual
data entry. To build a parsing/retrieval baseline (ML-in-MVP), the pipeline must first
download real documents — all editions and all releases — from the authoritative
registries. This change adds the ingestion layer (collector): registry discovery,
download, metadata, dedup, and versioned storage. It is domain-agnostic (one pipeline
for any design domain); shallow foundations and internal water supply are only the pilot
corpus, not a domain-specific model.

## What Changes

- New capability `normatives-collector`: automated ingestion of normative documents.
- New component `normatives-pipeline/collector/` (batch/CLI, no public API): registry
  clients, downloader, metadata store.
- Documents and metadata are stored in `dec_normatives` (provisional schema, to be
  reconciled with `norm-source-traceability`).
- CPU-only; no ML in the calculation path.

## Non-goals

- No parsing/extraction of formulas, tables, or clauses (that is `normatives-parser`).
- No embeddings or vector search (later).
- No public API; the collector is a batch/CLI tool.
- No change to Akim's backend, engine, or report generator.

## Capabilities

### New Capabilities

- `normatives-collector`: registry discovery, download, metadata, dedup, versioned
  storage.

## Impact

- New code under `normatives-pipeline/` and new `dec_normatives` migrations. No change
  to Akim's zones.
