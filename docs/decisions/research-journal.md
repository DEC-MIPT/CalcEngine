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
