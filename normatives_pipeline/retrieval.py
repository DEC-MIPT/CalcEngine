"""RAG: поиск пунктов/формул по смыслу (эмбеддинги vs TF-IDF baseline)."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
import pymorphy3  # type: ignore[import-untyped]
from sklearn.feature_extraction.text import (  # type: ignore[import-untyped]
    TfidfVectorizer,
)
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore[import-untyped]

_TOKEN_RE = re.compile(r"[а-яёa-z0-9]+(?:\.[0-9]+)*")

_morph: pymorphy3.MorphAnalyzer | None = None


def _morph_analyzer() -> pymorphy3.MorphAnalyzer:
    global _morph
    if _morph is None:
        _morph = pymorphy3.MorphAnalyzer()
    return _morph


def normalize_text(text: str) -> str:
    text = text.lower().replace("ё", "е")
    text = "".join(
        ch for ch in text if ch != "\ufffd" and not (0xE000 <= ord(ch) <= 0xF8FF)
    )
    morph = _morph_analyzer()
    tokens = _TOKEN_RE.findall(text)
    out = []
    for tok in tokens:
        if re.fullmatch(r"[а-яa-z]+", tok):
            out.append(morph.parse(tok)[0].normal_form.replace("ё", "е"))
        else:
            out.append(tok)
    return " ".join(out)


@dataclass(frozen=True)
class Hit:
    number: str
    text: str
    score: float


class EmbeddingIndex:
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2") -> None:
        from sentence_transformers import (
            SentenceTransformer,  # type: ignore[import-untyped]
        )

        self._model = SentenceTransformer(model_name)
        self._texts: list[str] = []
        self._meta: list[dict] = []
        self._emb: np.ndarray | None = None

    def index(self, items: list[dict]) -> None:
        self._texts = [normalize_text(it["text"]) for it in items]
        self._meta = items
        self._emb = self._model.encode(self._texts, normalize_embeddings=True)

    def search(self, query: str, k: int = 5) -> list[Hit]:
        q = self._model.encode([normalize_text(query)], normalize_embeddings=True)
        scores = (self._emb @ q.T).ravel()  # type: ignore[union-attr]
        top = np.argsort(-scores)[:k]
        return [
            Hit(number=self._meta[i]["number"], text=self._texts[i], score=float(scores[i]))
            for i in top
        ]


class TfidfIndex:
    def __init__(self) -> None:
        self._vec = TfidfVectorizer(tokenizer=str.split, lowercase=False, token_pattern=None)
        self._texts: list[str] = []
        self._meta: list[dict] = []
        self._matrix = None

    def index(self, items: list[dict]) -> None:
        self._texts = [normalize_text(it["text"]) for it in items]
        self._meta = items
        self._matrix = self._vec.fit_transform(self._texts)

    def search(self, query: str, k: int = 5) -> list[Hit]:
        q = self._vec.transform([normalize_text(query)])
        scores = cosine_similarity(q, self._matrix).ravel()
        top = np.argsort(-scores)[:k]
        return [
            Hit(number=self._meta[i]["number"], text=self._texts[i], score=float(scores[i]))
            for i in top
        ]


def build_formula_items(
    formulas: list, notation: list, clauses: list | None = None
) -> list[dict]:
    heading = {}
    if clauses:
        heading = {c.number: c.text for c in clauses}

    meanings_by_page: dict[int, list[str]] = defaultdict(list)
    for entry in notation:
        meanings_by_page[entry.page].append(entry.meaning)

    items: list[dict] = []
    for formula in formulas:
        parts = [f"формула {formula.number}"]
        if formula.clause and formula.clause in heading:
            parts.append(heading[formula.clause])
        parts.extend(meanings_by_page.get(formula.page, []))
        if formula.latex:
            parts.append(formula.latex)
        items.append(
            {
                "number": formula.number,
                "clause": formula.clause,
                "text": " ".join(parts),
            }
        )
    return items


def recall_at_k(index, queries: list[dict], k: int) -> float:
    ok = 0
    for item in queries:
        hits = index.search(item["query"], k=k)
        if any(h.number == item["clause"] for h in hits):
            ok += 1
    return ok / len(queries)
