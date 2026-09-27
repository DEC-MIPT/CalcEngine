"""Нормализация символов обозначений: raw → (id, latex) — паттерны из конфига."""

from __future__ import annotations

import re
import unicodedata

from ..config import parser_config

_CFG = parser_config()
GREEK: dict[str, str] = _CFG.get("greek_map", {})
PUA: dict[str, str] = _CFG.get("pua_map", {})
CYR: dict[str, str] = _CFG.get("cyr_map", {})

_MAX_SYMBOL_LEN = 8
_PRIME_CHARS = ("´", "'", "\u02b9", "\u2032", "\u2033", "\u2034")


def split_symbols(raw: str) -> list[str]:
    parts = re.split(r"\s*,\s*|\s+и\s+|\s*;\s*", raw)
    return [p.strip() for p in parts if p.strip()]


def _strip_value(s: str) -> str:
    return s.split("=", 1)[0].strip()


def _char_latex(ch: str) -> str:
    if ch in GREEK:
        return GREEK[ch]
    if ch in PUA:
        return PUA[ch]
    if ch.isascii():
        return ch
    return "\\text{" + ch + "}"


def _char_id(ch: str) -> str:
    if ch in GREEK:
        lt = GREEK[ch]
        return lt.removeprefix("\\")
    if ch in PUA:
        lt = PUA[ch]
        return lt.removeprefix("\\")
    low = ch.lower()
    if low in CYR:
        return CYR[low]
    if ch.isascii() and ch.isalnum():
        return ch
    return "_"


def normalize_symbol(raw: str) -> tuple[str, str] | None:
    prime = "'" if any(p in raw for p in _PRIME_CHARS) else ""
    for p in _PRIME_CHARS:
        raw = raw.replace(p, "")
    s = _strip_value(unicodedata.normalize("NFKC", raw))
    if not s or len(s) > _MAX_SYMBOL_LEN or any(ch.isspace() for ch in s):
        return None
    if not any(ch.isalpha() or ch in PUA for ch in s):
        return None

    chars = [ch for ch in s if ch != "´"]
    if not chars:
        return None

    base = _char_latex(chars[0])
    sub = "".join(_char_latex(ch) for ch in chars[1:])
    latex = base + (("_{" + sub + "}") if sub else "") + prime

    id_base = _char_id(chars[0])
    id_sub = "".join(_char_id(ch) for ch in chars[1:])
    ident = id_base + (("_" + id_sub) if id_sub else "") + ("_pr" if prime else "")

    return ident, latex
