# ML model & research journal

Development journal for Egor's data/ML zone. One entry per source probe, model
evaluation/selection, and hypothesis test (with its correction). English only.

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
