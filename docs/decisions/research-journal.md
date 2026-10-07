# Research journal (formula extraction notebook)

Lab notebook for the `research.ipynb` work: rendering PDF pages to images and reading
formulas with pretrained models. English only (RU mirror: `research-journal-rus.md`).

Tag convention: `[ML]` — model-based tasks (detection/OCR models); untagged — deterministic
methods (rendering, cropping, IO).

## Entry 1 — Page rendering to images (2026-09-27)

Method: pdfplumber `page.to_image(resolution=300)` → one PNG per page, saved to
`normatives_pipeline/research/pages/page_NNN.png` (222 pages for СП 22.13330.2016).

Finding: pdfplumber rasterizes correctly at 300 dpi (2482×3507). Images are saved to disk,
not RAM (222 pages would be ~5 GB in memory).

## Entry 2 — [ML] Formula detection with DocLayout-YOLO (2026-09-27)

Method: DocLayout-YOLO (YOLOv10, pretrained on DocStructBench), class `isolate_formula`,
imgsz=1024, conf=0.25, on page 38.

Finding: detects the formula and crops it
(`normatives_pipeline/research/crops/page_038_formula_0.png`). The HF repo ID
`juliozhao/DocLayout-YOLO-DocStructBench` is NOT resolvable by `YOLOv10(...)` directly —
download `doclayout_yolo_docstructbench_imgsz1024.pt` via `hf_hub_download` and pass the
local path.

Conclusion: detection works out-of-the-box; use DocLayout-YOLO for the bbox, no fine-tuning.

## Entry 3 — [ML] LaTeX recognition with texify — FAILED (2026-09-27)

Method: `texify` (Donut-based vision-encoder-decoder), `load_model()` + `load_processor()`
+ `batch_inference` on the page-38 crop.

Finding: crashes with `AttributeError: 'dict' object has no attribute 'to_dict'` inside
`TexifyConfig.from_pretrained` (transformers `configuration_utils.to_diff_dict`). Root
cause: transformers 4.57.6 is incompatible with texify 0.2.1's custom config class.

Next: pin transformers to a compatible version, or switch to pix2text / pix2tex.

## Entry 4 — Dataset choice for formula recognition (2026-09-27)

Decision: im2latex-230k as the bulk fine-tune base (Zenodo record 7738969,
`PRINTED_TEX_230k.zip`, ~1 GB): `generated_png_images/` + `final_png_formulas.txt`
(+ `230k.json` vocab). Clean vector renders match our PDF crops better than noisy arXiv
scans (UNITE/IBEM).

Caveat: no public dataset covers Cyrillic normative formulas (`c₁`, `γ_II`, `где`-blocks),
so real domain adaptation still requires our own Russian golden set from СП.

## Entry 5 — ML pipeline strategy: MVP now, own model later (2026-09-27)

Decision (confirmed with the developer):

- MVP now: ready pretrained model for formula recognition (detection = DocLayout-YOLO;
  recognition = texify/pix2text, no training). Ready solution, no fine-tuning in the MVP path.
- Future ML pipeline: train our own recognition model on im2latex-230k, expand the dataset with
  our own formulas (Russian golden set from СП), and re-fine-tune the model iteratively as the
  dataset grows (collect → expand → re-fine-tune loop).

So the dataset download (`research.ipynb` cell 4) is groundwork for the future pipeline, not part
of the MVP delivery.

## Entry 6 — [ML] Formula recognition: pix2text LatexOCR works (2026-09-27)

Finding: texify (Entry 3) remains broken on transformers 4.57.6. pix2text's `LatexOCR`
(`mfr-1.5`, ONNX backend) works out-of-the-box on CPU (onnxruntime here has no CUDA provider).

Result on the page-38 crop: score=0.979, LaTeX
`\Delta h \leq a ~ ( \mathrm{t g} ~ \varphi_{\mathrm{I}} + c_{\mathrm{I}} / p ),`.
Known post-processing gaps: `\mathrm{t g}` should be `\mathrm{tg}`, spurious `~`.

Conclusion: use pix2text LatexOCR (device="cpu") as the MVP recognition model; texify deferred
until a transformers pin is safe.

## Entry 7 — sklearn pipeline + validation eval (2026-09-27)

Built the research pipeline as a scikit-learn `Pipeline` (detect → recognize → correct) and a
validation set (`research/validation.toml`, 3 verified etalons: 5.1, 5.5, 5.7). Eval metric:
normalized edit-distance similarity (difflib ratio after LaTeX canonicalization).

First run: mean similarity 0.764 — 5.5 (simple) 0.939; 5.1 0.682; 5.7 (complex R-formula) 0.671.
Weak spot: complex subscripts — `\gamma_{II}` → `\mathrm{\tiny I I}`, `k_z` → `k_{\varepsilon}`.
This is exactly what fine-tuning + the golden set must fix (Entry 5).

## Entry 8 — Semantic formula comparison via latex2sympy2 (2026-09-27)

The difflib string similarity (Entry 7) penalized cosmetic LaTeX differences (`\big` vs `\left`,
`_{_{\gamma}}` double subscripts, `\mathrm{I}` vs `I`, redundant `{}`). Replaced it with a
semantic round-trip: light preprocessing (`normalize_latex`) → `latex2sympy2` → SymPy expression
equality.

Result: formulas 5.5 and 5.7 are now `equal=True` (exact semantic match), not similarity
0.939/0.671. `sympy.parse_latex` is NOT usable here — it mangles `\mathrm{tg}` → `g*t`,
`\mathrm{I}` → `I*mathrm`, `\gamma_{II}` → `gamma_{I*I}`; `latex2sympy2` handles these correctly
(keeps `\mathrm{tg}` as a symbol, preserves multi-char subscripts).

## Entry 9 — Dependency resolution: one antlr4, drop the dead weight (2026-09-27)

`latex2sympy2` pins `antlr4==4.7.2`, conflicting with `omegaconf` (4.9, via pix2text's text-OCR)
and `sympy.parse_latex` (4.11). Resolution, without a separate venv and without losing quality:

- dropped `sympy.parse_latex` (`alternative_parse_latex` in `formula_code.py` — the "less valid"
  path; the MVP runs the deterministic registry, not `parse_latex`);
- dropped `texify` (already broken on transformers);
- bypassed `omegaconf` by importing `pix2text.latex_ocr.LatexOCR` directly (a small shim) instead
  of `from pix2text import LatexOCR` — `latex_ocr.py` only needs `cnocr.utils`, not the text-OCR
  chain that pulls `omegaconf`.

Result: a single antlr4 (4.7.2); `LatexOCR` (mfr-1.5) + `latex2sympy2` both work. Also raised the
page render DPI from 300 to 400 — recognition is excellent there.

## Entry 10 — Direction correction: OCR fills, registry verifies (2026-09-27)

ML journal Entry 21 declared the hand registry (`formulas.toml`) as the MVP formula path because
pix2tex was unstable. That direction is now reversed: the research OCR (pix2text mfr-1.5 +
DocLayout-YOLO + DPI 400) reads formulas well — the pilots 5.5 and 5.7 match semantically with no
errors — so auto-extraction scales, while filling the registry by hand for hundreds of formulas is
infeasible.

New model:
- OCR is the primary source: it fills `latex` (and a candidate `expression`) for every formula with
  `provenance=machine-extracted`, `status=unverified`;
- the registry is the human-verified subset — only formulas that must be 100% correct enter it.

Verification flow (open question for Akim, `formula-verification-akim.md`): on the user side, the
engineer sees the normative excerpt + the extracted LaTeX + notation and marks "верно"/"косяк"
(fixing on error). On the pilots there were no errors.

## Entry 11 — Decision: CNN detection + pix2text recognition (2026-09-27)

Why this final shape. The PDFs are text-based (not scans), so the symbols exist in the text
layer — but the formula STRUCTURE (fractions, subscripts, superscripts) is encoded only in
character positions and font size, not in the text content (ML journal Entry 20). Two options:

1. Coordinate-based layout reconstruction (deterministic): group chars by baseline, detect
   sub/superscript by size/offset, detect fractions by numerator/denominator. Attempted as
   `parser/formula_layout.py` — the first version misclassified subscripts (`^{c}` instead of
   `_{c1}`), missed fractions, and leaked the «где» block into the result. Fixing it means
   re-implementing a fragile layout engine.
2. CNN detection + OCR recognition: DocLayout-YOLO (pretrained on DocStructBench) finds the
   formula bbox on the rendered page (DPI 400); pix2text (LatexOCR mfr-1.5, ONNX) reconstructs
   the LaTeX structure from that crop. This is what the research notebook validated — pilots 5.5
   and 5.7 match semantically via `latex2sympy2`.

Decision: option 2. The CNN reliably finds the position (no coordinate heuristics), and pix2text
reliably reconstructs the structure (no fragile layout engine). Cost: ML (CPU ONNX, ~5 s/formula)
and the `machine-extracted`/`unverified` status — accepted, because verification is user-side
(`formula-verification-akim.md`). Parameters (DPI 400, conf 0.25, imgsz 1024) live in
`parser.toml` `[formula_ocr]`. The `ocr/` package and `ocr.toml` are removed; the pipeline is
`normatives_pipeline/formula_ocr.py` (detection + recognition + `correct_latex`).

## Entry 12 — Model lifecycle: lazy singletons + warm-up (2026-09-27)

What: `formula_ocr.py` loads DocLayout-YOLO (detector) and pix2text (recognizer) lazily as
module-level singletons (`_get_detector` / `_get_recognizer`), plus a `warm_up()` that forces
both loads.

Why: the models are heavy (weights + ONNX session); loading on every call/formula would be
unacceptable. A singleton loads once per process; `hf_hub_download` caches the weights on disk
(HF cache) so nothing re-downloads.

For what: a long-lived service calls `warm_up()` at startup, so the first request is already warm;
the batch CLI (`enrich.py`) amortizes the same one-time load across the whole document.

## Entry 13 — Full cycle run: download → ingest → sync → read (2026-10-06)

Branch `feature/normative-pipeline/data`. Goal: verify the end-to-end cycle works and catch
known bugs before the fix branch.

**Environment:** `dec-postgres` running (port 5433, DB `dec`), package installed as
`pip install -e "./ml[ml]"`, `DEC_DATABASE_URL=postgresql://dec:<password>@localhost:5433/dec`.

**Э1 — PDFs in `docs/normative-base/`:** 5 SP documents extract designation correctly
(СП 22/24/30/31/45); 7 files (приказы `_пр.pdf`, СНиП) give empty designation and are
correctly rejected by `ingest`.

**Э2 — ingest:**

+ `СП 22.13330.2016 --force`: 647 clauses, 130 formulas (127 numbered + 6 synthetic), 203
  notation entries, 56 cross-refs, 19 conditions, 121 tables, 2959 cells. Clean.
+ `СП 24.13330.2021 --force`: 292 clauses, 91 formulas, 134 notation entries. Clean.
+ **B1 confirmed:** after ingesting СП 24, `catalog_binding.document_id` for all 11 pilot
  parameters pointed at `СП 24.13330.2021` instead of `СП 22.13330.2016`. Root cause:
  `ingest.py:151` calls `pilot_catalog.sync_pilot_catalog(conn, designation)` with the
  ingested document's designation.

**Э3 — sync:** `pilot_catalog.sync_pilot_catalog(conn)` called without `designation`
argument (defaults to `СП 22.13330.2016`). Returns `True`. All 11 bindings correctly
reference `СП 22.13330.2016`.

**Э4 — read (as `dec_normatives_reader`):**

| View | Result |
| --- | --- |
| `catalog_read.documents` | 5 rows (СП 22/24/30/31/45); СП 30 and СП 45 show `edition=''`, `year=None` — old data from pre-edition-check code |
| `catalog_read.type_formulas` | 3 rows for `foundations_shallow_r`: `k_z_below`, `k_z_from` (`unverified`), `r` (`verified`) |
| `catalog_read.type_table_values` | 141 rows: 1 each for `gamma_c1/c2/k`, 46 each for `m_c/m_gamma/m_q` |
| `catalog_read.type_thresholds` | `k_z_threshold = 10.0 m` |
| `catalog_read.type_method_bounds` | `phi_II min=0.0 deg`, `phi_II max=45.0 deg` |
| `catalog_read.search(…)` | Correct ranked results for Russian query |

Access controls: INSERT refused (`FeatureNotSupported`), SELECT on `public.document` refused
(`InsufficientPrivilege`), CREATE TABLE refused by readonly session (m5 TEMP not yet tested
outside readonly session — m5 fix still open).

**M1 confirmed in read:** `type_formulas` shows formula `r` with `norm_refs[0].status =
"verified"` — must be `"unverified"` after the fix of M1.

**Summary:** the cycle runs end-to-end without errors. Bugs B1 and M1 are reproduced and
confirmed. The fix branch `fix/normative-catalog/data` must address both before Akim's
second review.
