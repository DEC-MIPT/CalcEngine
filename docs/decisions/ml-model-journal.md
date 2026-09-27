# ML model & research journal

Development journal for Egor's data/ML zone. One entry per source probe, model
evaluation/selection, and hypothesis test (with its correction). English only.

Tag convention: `[ML]` — model-based tasks (OCR/ViT, embeddings, RAG models); untagged —
deterministic methods (regex/parsing/indexes/lemmatization). Regex is NOT ML.

## Entry 1 — Source probe: access mode per registry (2026-09-27)

Hypotheses under test: H1 (registry non-uniformity), H3 (registry discovery).

Method: plain HTTPS GET (`requests`/`curl`, no browser) against each registry root,
plus `robots.txt`/`sitemap.xml` and API-doc probing.

| Source | Result | Access mode |
|---|---|---|
| `faufcc.ru` | Angular SPA (`<app>`, `main.*.js`); API host `api.faufcc.ru`; `/docs` is a Laravel admin API (auth/users/roles/assets) | SPA + admin API, **no public normative-registry API** |
| `fgiscs.minstroyrf.ru` | React SPA; `GET /api/opendata` → `application/json`, 15 datasets (ФСНБ-2020/2022, КСР, ПССР, ценовые зоны, оплата труда…) | **clean JSON open-data API** |
| `minstroyrf.gov.ru` | HTML (Bitrix), `sitemap.xml` | static/HTML |
| `gost.ru` → `rst.gov.ru` | HTML, `sitemap.xml` | static/HTML |
| `pravo.gov.ru` | `ConnectTimeout` on root | retry needed |

Finding: the ФГИС ЦС open-data API is the only clean, legal JSON API found so far, but
it exposes structured cost norms (ФСНБ/КСР/ПССР), not the full text of СП/ГОСТ with
formulas and clauses. The СП document texts must come from faufcc SPA data endpoints,
minstroy, or pravo — to be probed next.

Decision: keep API-first. Playwright stays as a fallback for the SPA registries only.

## Entry 2 — Commercial СПС (Техэксперт/Кодекс, КонсультантПлюс): B2B, licensing, markup

Context: full texts of СП/ГОСТ circulate as PDF on official sites or inside commercial
reference systems (СПС). Both named systems are commercial B2B:

- **Техэксперт (Кодекс, `cntd.ru`)** — the specialized system for technical norms
  (СП/ГОСТ/СНиП) with clause/formula markup. Integration/API exists but requires a paid
  enterprise agreement; content and markup are proprietary.
- **КонсультантПлюс** — legal-focused (less relevant to technical norms). API exists,
  also paid, for licensed corporate clients.

Hypothesis (how they get the data): they are **official distributors** under licensing
agreements with the norm publishers/developers (ФАУ ФЦС, Росстандарт, Минстрой, and the
НИИ that authored the norms). They receive the authoritative electronic text directly
from the source of truth — they do not scrape PDFs — which is why their editions and
statuses are current.

Hypothesis (who does the markup): the markup is their **editorial work, done manually**
by methodologists/editors (human-in-the-loop), and it is the core of their IP:
structural breakdown into clauses/tables/formulas/appendixes, cross-references between
clauses and documents, actuality statuses, amendments, and structured formula/table
extraction.

Implication for DEC: they mark up norms **manually**; DEC automates the same step
(NLP/RAG parsing + human-in-the-loop verification). That automation is the differentiator
and the thesis. Commercial СПС are a legal/commercial dependency (C5); excluded from the
MVP baseline. Free official sources (PDF + pravo.gov.ru API + fgiscs open-data) remain
the MVP path.

## Entry 3 — pravo.gov.ru: full documented REST API (confirmed)

`pravo.gov.ru` (Официальный интернет-портал правовой информации) exposes a free,
documented OpenAPI/Swagger service at `http://publication.pravo.gov.ru/`
(`swagger/v1/swagger.json`, title `Architect.Public.OpenApi`). Key endpoints:

- `GET /api/Documents` — search by `Name`, `Number`, `EoNumber`, `DocumentText`,
  date ranges; returns `items[]` with `eoNumber`, `title`, `number`, `documentDate`,
  `pagesCount`, `pdfFileLength`, `documentTypeId`, `signatoryAuthorityId`, `id`.
- `GET /api/Document?eoNumber=` — metadata.
- `GET /api/DocumentText?eonumber=` — full text.
- `GET /{controller}/pdf/{eoNumber}` — PDF download.
- `GET /OpenData/*` — open-data CSVs (governmentauthority, legalacts).

Gotchas recorded: HTTPS to the host times out from this environment (HTTP works);
`PageSize` accepts only specific values (30/100/200 — 5/20/50 rejected with RFC 7807).

Finding: this API indexes **legal acts** (laws, orders, decrees) — not the technical
texts of СП. `Name=22.13330`, `Name=свод правил`, `DocumentText=22.13330` all return 0
items. So СП formulas/clauses are NOT here; they live as PDFs on faufcc/minstroy.

Conclusion: two working free JSON APIs confirmed (fgiscs open-data for structured cost
norms, pravo for legal acts with text+PDF). The СП technical texts remain PDF-only —
the collector needs a PDF-download path for СП from faufcc/minstroy in addition to the
two APIs.

## Entry 4 — faufcc.ru СП register: clean JSON API found (no scraping needed)

The faufcc.ru "Реестр сводов правил" (register of своды правил) is an Angular SPA, but
its data comes from a clean JSON API at `api.faufcc.ru`:

- `GET /api/registries/entries?page=1&filters={"registry":"<id>","search":"<term>"}&include=asset`
  → entries with `number`, `name`, `state` (active), and `asset.links.download` (PDF).
- `GET /api/registries/categories?registry=<id>` → categories.
- Registry id for своды правил: `c5020d9a-a239-4806-a793-ac66cb36c71a`.
- PDF download: `GET /api/assets/{assetId}/download`.

Correction to Entry 1: no Playwright/Chromium is needed for faufcc after all — the SPA
exposes a plain JSON API, so the collector uses `requests` only (API-first, no scraping).

First download (into `norm-base/`), current active editions only:

| СП | Domain | Status |
|---|---|---|
| СП 22.13330.2016 (СНиП 2.02.01-83*) Основания зданий и сооружений | foundations | downloaded |
| СП 24.13330.2021 (СНиП 2.02.03-85) Свайные фундаменты | foundations | downloaded |
| СП 45.13330.2017 (СНиП 3.02.01-87) Земляные сооружения, основания и фундаменты | foundations | downloaded |
| СП 30.13330.2020 (СНиП 2.04.01-85*) Внутренний водопровод и канализация зданий | water/sewage | downloaded |
| СП 31.13330.2021 (СНиП 2.04.02-84*) Водоснабжение. Наружные сети и сооружения | water | downloaded |
| СП 32.13330.2018 (СНиП 2.04.03-85) Канализация. Наружные сети и сооружения | sewage | **no file in register** |

Finding: this register lists only the current (active) edition of each СП, not
superseded historical editions. Historical editions need the "Реестр
нормативно-технической документации" (sibling register) or another source.

## Entry 5 — Historical normative traceability = killer feature (CustDev)

CustDev insight (from the developer): respondents struggle to find OLD versions of
normative documents. Example use case — "how was a building/структура calculated that
was built in 1985? By which norms, which coefficients were in force then?".

This makes **historical editions** a first-class requirement for the collector, not a
nice-to-have: the service must resolve the normative base as of any past date, and the
collector must ingest superseded revisions additively (matches WP3 "additive revision
storage" and the `NormRef` immutability decision).

Probe result: neither faufcc register exposes historical editions. The sibling register
`reestr-normativno-tekhnicheskoi-dokumentatsii` (registry id
`b154aaa9-236f-4c4d-8f2c-fab07558f322`) returns entries with `number=null` and no
`asset` download link — metadata only, current documents only. The old СНиП of the 1980s
(СНиП 2.02.01-83, СНиП 2.04.01-85, etc.) are not in the free official registers.

Open question: where do historical/снятые с действия editions live? Candidates:
commercial СПС (Техэксперт keeps historical versions), archival scans, or the approver's
archives. This needs its own source strategy before the "1985 lookup" feature can be fed.

## Entry 6 — pravo (приказы) and Техэксперт (docs.cntd.ru): probe results

pravo.gov.ru:
- `SignatoryAuthorityId=efa6da4b-…` (Минстрой России) works — 899 приказов, but they are
  administrative (формы, порядки, перечни). `Name=22.13330`, `Name=утверждении свода
  правил`, `DocumentText=свод правил` → 0. So the СП approval orders are not surfaced on
  pravo (the portal indexes legal acts, not the СП chronology). pravo is not a source for
  СП editions or their statuses.

Техэксперт (`docs.cntd.ru`):
- Nuxt SSR app. `robots.txt`: `Disallow: /api`, `Disallow: /search?`, `Disallow:
  /purchased`. Sitemaps: `/pages.xml`, `/sitemap/docs/documents_sitemap.xml`.
- Their `/api` exists but is explicitly disallowed for crawlers; programmatic access is a
  ToS/copyright violation. Content is commercial.

Answer to "откуда Техэксперт берёт документы": they are official distributors under
licensing agreements with ФАУ ФЦС / Росстандарт / Минстрой and receive authoritative
electronic texts directly from the publishers' systems — not via a public channel. That
channel is not available to us without our own agreements.

Bottom line for the collector: free official sources cover current СП (faufcc API),
structured cost norms (fgiscs open-data), and legal acts (pravo API). Historical СНиП/СП
editions have **no free official source** — commercial (Техэксперт) or archival scans.
This is the hard boundary for the "1985 lookup" killer feature; it needs a decision
(commercial contract vs archival-scan ingestion vs deferred).

## Entry 7 — Техэксперт: с кем договоры (кандидаты для переговоров)

Техэксперт (Консорциум «Кодекс») — официальный распространитель; договоры с
правообладателями нормативных документов:

- **Росстандарт** (Федеральное агентство по техническому регулированию и метрологии) —
  ГОСТ и национальные стандарты; оператор ФИФС / «Береста».
- **ФАУ «ФЦС»** (Федеральный центр нормирования, стандартизации и технической оценки
  соответствия в строительстве; подведомствен Минстрою России) — своды правил (СП),
  реестр нормативно-технической документации.
- **Минстрой России** — утверждающий орган СП.
- **Разработчики норм** (НИИ, авторские коллективы) — авторские права на тексты.

Стратегия: выходить напрямую на первичные источники (ФАУ ФЦС для СП, Росстандарт для
ГОСТ), а не на Техэксперт-посредника. ФАУ ФЦС уже отдаёт публичный реестр СП через свой
API (Entry 4) — это первичный канал, с него и начинать переговоры.

Дополнение: сформулирован черновик сообщения научному руководителю с просьбой выйти на
представителей официальных источников за доступом к историческим СП, плюс ориентиры по
ценам (точный прайс — Приказ Росстандарта №117 от 28.01.2019,
`standards.ru/i/pricelist_2019.pdf`; ГОСТ — десятки–сотни ₽/документ; подписка на фонд —
договорная; право на архив СП — договорное). Полный текст (на русском) — в
`ml-model-journal-rus.md`, Запись 7.

## Entry 8 — Архивный скан: пример получен (СНиП 2.02.01-83*)

Скачал примеры архивного СНиП (в `norm-base/`, gitignored):

- `СНиП 2.02.01-83.pdf` — files.stroyinf.ru, 52 стр., PDF 1.4. Есть OCR-текстовый слой,
  но неидеальный (артефакты: «М осква», «УД К 6 2 4 .1 5»).
- `СНиП 2.02.01-83 (1995).pdf` — ednc.gov.md, 63 стр., издание Республики Молдова.

Вывод: архивные СНиП циркулируют как **сканы страниц с (возможно) неполным/шумным
OCR-слоем**. Оба — неофициальные зеркала, не первоисточник. Для парсера это путь
«скан → OCR» (план §7.2), причём текстовый слой нельзя доверять без верификации
(сходится с provenance `human-verified`).

## Entry 9 — Error propagation in ML/OCR over normative sources (scientific note)

**Statement.** Machine-extracted text (OCR of archival scans, then NLP/RAG extraction of
formulas, coefficients and clauses) carries an irreducible, non-negligible error that
propagates into the calculation. The extracted layer must therefore be treated as
untrusted (`machine-extracted`, `unverified`) until a human verifies it; the engine is
deterministic and accepts only `human-verified` values ("no ML in the calculation path").

**Why the error occurs.**

1. *Source degradation.* Archival СНиП are scans of paper: low resolution, faded ink,
   skew, stains, uneven illumination. The 1980s typography (phototypesetting, multi-column
   tables, sub-/superscripts, footnotes) is far from clean OCR input.
2. *Domain-symbol complexity.* Engineering norms mix Cyrillic/Latin/Greek and mathematical
   notation (N₀, R₀, γ_c, φ_II, 10⁻³). General OCR models, trained on natural text, fail
   precisely on this mixed-symbol, formula-heavy surface.
3. *Systematic error modes.* Homoglyph confusion (0/O, 1/l, З/3, К/K), subscript/superscript
   flattening (N₀ → N0 / NO), formula mis-recognition (math is a layout problem, not a
   character problem), and table-cell segmentation errors. The critical tokens — digits,
   subscripts, units — are exactly where the error concentrates.
4. *Cascading.* OCR error → extraction error → wrong coefficient → wrong result. A single
   misread digit changes the design value; errors compound multiplicatively down the chain.

**How one can attempt to correct it (tools).**

- *OCR:* Tesseract (baseline, weak on Cyrillic formulas); Surya / PaddleOCR (multilingual,
  better on documents); ABBYY FineReader (commercial, best on Russian engineering text);
  formula-specific: Nougat (Meta), MathPix, pix2tex/LaTeX-OCR.
- *Layout/tables:* Table Transformer, PP-Structure, LayoutLM.
- *Post-correction:* LLM context re-scoring against a domain glossary (обозначения, units),
  rule-based normalization of designations and units.
- *Routing/ensembling:* OCR confidence to route low-confidence spans to review;
  multi-engine voting.

**Why full correction is practically unattainable.**

1. *Irreducible information loss.* Below a quality threshold the glyph is physically absent
   from the image; no model recovers information that is not there.
2. *Perceptual ≠ semantic accuracy.* OCR optimizes CER/WER, but correctness here is
   semantic (1.2 vs 12; subscript vs multiplier). High character accuracy can coexist with
   wrong values, and the model has no notion of engineering meaning.
3. *Formula recognition remains open.* Even state-of-the-art (Nougat/MathPix) errs on
   non-standard layouts; a single wrong subscript changes the formula's meaning.
4. *No ground truth at scale.* Verification requires the authoritative text — exactly what
   is missing for archival scans — so residual error cannot be measured or corrected
   reliably.
5. *Error concentration on the payload.* Metrics look acceptable in aggregate while the
   critical tokens (digits/subscripts/units) are systematically wrong — a long-tail,
   adversarial profile.
6. *Miscalibration.* Confidence scores are unreliable under domain shift.

**Consequences (added).** The human-in-the-loop gate is an architectural invariant, not a
workaround: ML output is a drafting aid (a suggestion plus a citation hint), never a source
of truth. Commercial СПС avoid OCR entirely by receiving authoritative electronic texts
from publishers; our historical-traceability feature forces us into OCR exactly where the
error ceiling is highest — a genuine thesis-level trade-off that must be stated and
measured, not hidden. Practical policy: prefer digital-born documents (native text layer,
e.g. faufcc current СП) for the baseline; reserve OCR for the historical track; report
residual error per entity type (CER / extraction F1 / exec_rate) and gate every
machine-derived value behind `human-verified`.

## Entry 10 — Session summary (2026-09-27)

Progress on hypotheses H1–H12 (definitions: `docs/01-гипотезы-ландшафт-пайплайна.md`):

- **Result (tested):** H1 — faufcc СП register has a clean JSON API; current СП resolve
  automatically, but no historical editions ("single source of truth" partly falsified);
  H2 — current СП downloadable legally (5 docs); archive/redistribution unresolved (advisor
  request drafted); H3 — current docs covered, historical ≈ 0; H4 — format heterogeneity
  confirmed (text-PDF vs scan-with-OCR); H7 — changes NOT machine-readable in free sources
  (pravo has no СП orders); H10 — universal collector layers implemented, extraction
  adapters not yet; H12 — desk-research reinforced (no interviews).
- **Theoretical only:** H9 — OCR/ML error-propagation note (Entry 9), no empirical F1.
- **No result:** H5, H6, H8, H11 (entity extraction, exec_rate, change→calc linking,
  methodologist chronometry).

Session artifacts: layered collector `normatives_pipeline/` (`sources.toml`, faufcc+pravo
active, fgiscs disabled), journal (EN+RU), `.gitignore` (`norm-base/`). Next:
`normatives-parser` — closes H4/H5/H6.

## Entry 11 — Model landscape for extraction (H5/H6)

Candidate ready models for the parser (formula → code, tables, RAG):

- **Formula → LaTeX:** `pix2tex`/LaTeX-OCR (ViT, open-source, `pip install pix2tex`);
  Nougat (Meta, academic PDF → Markdown+LaTeX); MathPix (commercial, best quality).
  Open-source 240M "image → LaTeX" base model (arXiv:2408.04015).
- **Formula → executable code:** SymPy `parse_latex` → `lambdify` → NumPy (the "substitute
  values → compute" path).
- **Tables:** Table Transformer TATR (Microsoft, DETR: detection + structure, HF
  `microsoft/table-transformer`); Camelot / pdfplumber (digital PDFs only); PP-StructureV2
  (PaddleOCR, images+PDF); PdfTable (unified, arXiv:2409.05125).
- **RAG / embeddings:** `cointegrated/rubert-tiny2` (Russian, per plan) → ONNX.

Risk (domain shift): pix2tex/Nougat are trained on English/Western academic math; Russian
СНиП use Cyrillic variable names and subscripts (N₀, γ_c, φ_II) — the domain gap must be
measured (H9/H10), not assumed away.

## Entry 12 — Decision: collector paused until historical-data access

The collector (`feature/normative-collector/data`) is paused until access to historical СП
editions is obtained (via the advisor → ФАУ ФЦС / Минстрой / Росстандарт). Historical
traceability is the killer feature; without it the product has no differentiator. Moving to
the parser (calculation extraction), which does not depend on the historical track.

## Entry 13 — Parser: baseline and formula → code (first runs)

Run on pilot СП 22.13330.2016 (222 pages, text-PDF):
- layer — text (not scan); clauses 647 (regex); formula numbers 124; notation entries 729;
  tables 1 (first 15 pages, for speed).

Formula (5.7) → executable code:
- **reliable** (explicit symbol table + deterministic expression) → `lambdify` → R = 143.75
  kPa. Works.
- **less-valid** — naive `parse_latex`: silent error — `\gamma_{c1}` → `c*1`, `\gamma_{II}`
  → `I*I` (imaginary unit squared). Confirms the domain shift (H9/H10): multi-char/roman
  subscripts of Russian notation break the naive LaTeX parser.
- Conclusion: the reliable path is NOT naive `parse_latex` but an explicit symbol table (or a
  structured AST), because subscripts must be mapped deliberately.

Performance / format:
- pdfplumber `extract_text` — 60 s for 222 pages; `pdftotext` (poppler) — ~1 s. Text via
  pdftotext (subprocess); pdfplumber only for tables (also slow, ~0.23 s/page → needs
  targeted page selection).
- The text layer garbles formulas: Greek letters/subscripts become box chars (, ) in
  pdftotext. So text-layer formula extraction is unreliable — need image OCR (pix2tex) or an
  explicit symbol table.

## Entry 14 — RAG: embeddings vs TF-IDF (recall@k on СП clauses)

Corpus: 635 clauses of СП 22.13330.2016 (text > 30 chars). 5 ground-truth queries (natural
phrase → clause number). Metric recall@1/3/5 (exact number match).

| Model | recall@1 | recall@3 | recall@5 |
|---|---|---|---|
| cointegrated/rubert-tiny2 (312-dim) | 20% | 20% | 20% |
| intfloat/multilingual-e5-small (384-dim) | 60% | 60% | 60% |
| TF-IDF (lexical baseline) | 60% | 60% | 60% |

Findings:
1. rubert-tiny2 is too weak for this task (20%) — a tiny model, 312 dims.
2. multilingual-e5-small matches TF-IDF but does NOT beat the lexical baseline.
3. For exact-term queries (the realistic normative-search case), lexical search (pg_trgm /
   TF-IDF) is competitive or better: domain vocabulary is repetitive, queries are exact terms.
Limitation: the eval uses exact-term queries (favoring lexical). A fair semantic comparison
needs paraphrase queries + a separate ground truth (next step).
Decision: MVP search is lexical (pg_trgm); embeddings go on top as a semantic layer (hybrid)
with a stronger model or fine-tuning.

## Entry 15 — NLP: pix2tex on formula (5.7) — domain gap (OCR)

Controlled test: formula (5.7) rendered to an image (matplotlib), run through pix2tex (ViT,
trained on English academic math).

Input: `R = \frac{\gamma_{c1}\gamma_{c2}}{k}[M_\gamma k_z b \gamma_{II} + M_q d_1 \gamma'_{II} + (M_q-1)d_b\gamma'_{II} + M_c c_{II}]`

pix2tex output:
`R = \frac{\underline{v_{c1} y_{c2}}}{k}[M_\gamma k_z b V_{II} + M_q q_1 V'_{II} + (M_q-1)d_b V'_{II} + M_c C_{II}]`

Errors:
- Greek γ read as v/y/V (three different Latin letters!) — `\gamma_{c1}→v_{c1}`,
  `\gamma_{c2}→y_{c2}`, `\gamma_{II}→V_{II}`;
- `d_1 → q_1`; `c_{II} → C_{II}` (case); spurious `\underline{}`.
- BUT the structure is preserved: fraction, brackets, subscripts, primes — correct.

Conclusion: pix2tex preserves formula structure but breaks Greek symbols (γ→v/y/V) and case.
Russian engineering formulas need a symbol post-corrector (map γ↔v/y/V, case normalization)
or domain fine-tuning. Confirms H9/H10.

## Entry 16 — RAG: ё-normalization is mandatory

Same query with and without «ё» on the 647-clause-heading corpus of СП 22.13330.2016:

- `расчётные значения характеристик грунтов формула` → 0.704 (5.3)
- `расчетные значения характеристик грунтов формула` → 0.835 (5.3)

~16% drop purely from ё/е: the TF-IDF tokenizer treats «расчётные» and «расчетные» as
different tokens, so only the shared words («значения», «характеристик», «грунтов») match,
lowering cosine. Users typically type «е» (without ё), while norms use «ё» rarely and
inconsistently.

Rule (mandatory for all search, lexical and embeddings):
- lowercase;
- ё → е (both query and document);
- strip replacement chars (□) from text before indexing.

## Entry 17 — RAG: formula indexing + lemmatization (morphology)

The raw formula text is useless (square glyphs). Formulas are indexed as separate items with
an enriched search_text = `формула <N>` + clause heading + notation meanings on the page
(+ latex). Formula→clause association is by `(page, line)`: a formula gets the nearest
preceding clause heading on the same page.

Without lemmatization the query `расчётные значения характеристик грунтов формула` did not
surface formula (5.1) at the top: «расчетные» (query) ≠ «расчетных» (in heading 5.3.16), so
cosine dropped. With pymorphy3 (lemmatization), formula (5.1) became the top hit:

- formula 5.1 (clause 5.3.16) — 0.435; then 6.41, 6.42, 6.43, 5.33.
- clauses: 5.3 / 5.3.15 / 5.3.2 — correct.

Conclusion: Russian search needs lemmatization (morphology), not just ё-normalization;
otherwise inflection («расчетные/расчетных/расчетными») breaks accuracy. Formulas must be
separate index items linked to their clause via NormRef.

## Entry 18 — RAG: reading the PDF per query is itself slow (speed/convenience)

The current demo search re-reads the PDF (`pdftotext`), re-extracts clauses/formulas/notation,
re-lemmatizes ~1400 texts (pymorphy3) and re-builds TF-IDF on every query. The bottleneck is
not the ranking search itself but the «read and process the document» step per query — this
contradicts the instant-response requirement.

Relates to the speed/convenience hypothesis: the passport working hypothesis (sheet 3, A92) —
«cut a typical calculation from 2–4 hours to 20 minutes», the pipeline acceptance criterion —
«load < 2 sec»; the engineer pain point from problem interviews — «finding the current edition
of a norm takes up to 30–40 min».

Conclusion: search must run over a **pre-built** store (structure + index built in offline
ingestion when the document is received), and the query path must only normalize+lemmatize the
query string and look it up in the ready index. Reading the PDF at query time is prohibited —
that is exactly why it «runs slowly».

## Entry 19 — H4/H10: СП 45.13330.2017 — formulas WITHOUT numbers

The query «условие успешного погружения опускных колодцев» found clause 13.8, but it did not
return a formula and did not print the «где…» block. Reason: in this document the formula is
not numbered:

```
13.8 Для успешного погружения опускных колодцев должны соблюдать следующее условие:
    G + Gп ≥ КпΣТ,
где G – собственный вес колодца (с учетом взвешивания в воде);
    Gп – дополнительная пригрузка колодца;
    Кп = 1,15–1,25 – коэффициент условий работы при погружении;
    ΣТ – силы трения стен колодца по грунту.
```

There is no `(13.x)` marker at the end of the line. The formula extractor is keyed on `(N.N)`
→ the whole document matched 1 line → «formulas 1». The «где…» block in
`extract_formula_notation` is also attached only to found (numbered) formulas, so it was lost.

Contrast: in СП 22.13330.2016 formulas are numbered `(5.1)`, `(5.7)`; in СП 45 they are often
unnumbered and inline. Confirms H4 (non-uniform formats) and H10 (per-document adapters needed;
one universal parser does not work).

Fix direction: detect a formula by structure (formula line + following «где…» block), not by
number; use the clause number or a synthetic id as the number.

## Entry 20 — H5/H6: the text layer is unusable for math

Checking formula (5.7) in СП 22.13330.2016 — `pdftotext -layout` produces a fragmented layout
where the numerator/subscripts/denominator are scattered across lines and Greek is PUA-encoded:

    26: '              \uf067 \uf067'                 # γ γ (numerator)
    27: 'R = c1 c2 \uf05bM k b\uf067 + M d \uf067\uf0a2 + (M − 1)d \uf067\uf0a2 + M c \uf05d,'   # body + c1,c2
    28: '(5.7)'
    29: '\uf067 z \uf049\uf049 q 1 \uf049\uf049 q b \uf049\uf049 c \uf049\uf049'  # subscripts γ,z,II,q,1,II,q,b,II,c,II
    30: 'k'                                      # denominator

(`\uf067`=γ, `\uf05b`=[, `\uf05d`=], `\uf049`=I, `\uf0a2`='). The symbol order is non-linear —
rebuilding the expression from text without coordinate-based layout analysis is impossible.

Conclusion: the text layer works for clauses/notation/search, but **not** for an executable
formula expression.

## Entry 21 — OCR (pix2tex) on a real formula: fails on this PDF

Rendering the formula (5.7) region → pix2tex (two attempts, different crops, 300 and 400 dpi)
produces garbage: the model reads the surrounding text («При расчете деформаций…») as a table,
not the formula. On a synthetic clean render (Entry 15) the structure survived; on the real
degraded PDF (PUA fonts, mixed with the heading) it fails.

MVP conclusion: auto-extracting `expression` from THIS PDF via pix2tex is unstable. The MVP path
is a deterministic **formula registry** (`formulas.toml`): expression+latex+symbols are written
once exactly (0 errors), and the pipeline delivers them automatically. OCR (Nougat/MathPix, better
rendering) is scaling to thousands of formulas LATER, not an MVP blocker.

## Entry 22 — OCR: two-stage pipeline (detect + recognize) — the structure is read

Built a decomposed two-stage pipeline (separate modules + a separate `ocr.toml` config):
(1) `ocr/detect.py` — formula-region detection from character coordinates (the `(N.N)` marker +
an x-indent filter), (2) `ocr/recognize.py` — pix2tex on the clean crop.

Result on (5.7) from the real PDF: **the formula structure is recovered** —
`R=\frac{...}{...}[M_\gamma b + M_q d \gamma' + (M_q-1)d c]` (fraction, brackets, subscripts,
primes). But: (a) detection still captures the inline heading «…вычисляемого по формуле» (the
formula sits right next to text), (b) symbols are misread (γ→`*`, k→`L`, II→`1`, b→`b1`,
d_b→`d_c`, c_II→`c_n`).

Conclusion: the CNN/ViT path works on **structure**. For an exact `expression` we need (1) precise
detection (separate the inline heading) and (2) symbol post-correction / fine-tuning. Confirms H9:
pure automation without a human does not reach 99.9%.

## Entry 23 — [ML: pix2tex/ViT OCR] formula (5.7) read ~98%

Precise detection (the formula is centered, the heading is above — separated by coordinates) plus
pix2tex produced a breakthrough: formula (5.7) is read almost fully.

- **[ML] pix2tex (ViT)** returned the correct structure and almost all symbols:
  `R=\frac{\gamma_{c1}\gamma_{c2}}{k}\bigl[M_\gamma k_z b \gamma_{II} + M_q d_1 \gamma'_{II} + (M_q-1)d_b \gamma'_{II} + M_c c_{II}\bigr]`
- **[not ML] deterministic correction** (a config replacement map in `ocr.toml`): the only
  systematic OCR error — Roman «II» is read as `\mathrm{in}`/`\mathrm{i}` → replace with `II`;
  plus `\bar{1}` → `1`.

Remaining differences from ground truth are cosmetic: `\bigl/\bigr` vs `[]`, the prime order
(`\gamma_{II}^{\prime}` vs `\gamma'_{II}`), a trailing «, (5.7)» (the number marker stayed in the crop).

Key takeaway: pix2tex previously produced garbage because the crop captured the heading; once
detection became precise (character coordinates), ViT read the formula almost without errors.
**ML here is only pix2tex; detection and correction are deterministic (regex/coordinates).**

## Entry 24 — [ML: pix2tex/ViT] overfit on (5.7); generalization fails

Cross-check on UNSEEN formulas: 5.1, 5.9, 5.10 — fail (garbage). (5.7) worked because detection and
correction were tuned to its layout (a centered formula with the heading above). Other formulas are
different: 5.1 — small inline; 5.9 — complex multi-line; 5.10 — the «где…» block right after it leaks
into the crop.

Conclusion: a single detection+correction config does not generalize (H10). We need either a stronger
layout model (Nougat, reads a whole page) or fine-tuning on a golden dataset (formula → LaTeX) via
HuggingFace Trainer.

## Entry 25 — [ML: Nougat] out-of-the-box failure on a Russian normative PDF

Nougat (`facebook/nougat-base`, ViT+BART, trained on English academic papers) on the СП 22.13330.2016
page with formula (5.7) collapsed into hallucination — it endlessly repeats «The β-function». Classic
domain shift: Cyrillic + engineering formulas are outside its training distribution.

Conclusion: Nougat is unusable on Russian normative PDFs without fine-tuning. Fine-tuning on a golden
dataset («formula → LaTeX») is the right path, but it needs a dataset (hundreds of examples), not the
2 formulas in the manifest. A GPU is available (CUDA, 1 device) and HF Trainer is ready — the blocker
is labelling the golden dataset.

## Entry 26 — [ML: small local LLMs] they do not replace OCR; useful for «text → structure» and labelling

Evaluation of small local LLMs (`Qwen2.5-3B`, `Llama-3.2-3B`, `Gemma-2-2B`) for formula reading:
- reading a formula **from an image** — NO (a text LLM cannot see an image; a small VLM is weak at math);
- turning extracted text+notation into structure (`id`/`latex`/`expression` via a JSON schema) — YES;
- semi-auto golden-dataset labelling (the LLM proposes «formula → LaTeX», a human confirms) — YES.

Decision: small LLMs are a «text → structure» post-processor and a labelling assistant, not an OCR
replacement. Matches the personal hypothesis (`02-личная-исследовательская-гипотеза.md`): an LLM with
a structurally-constrained JSON output.
