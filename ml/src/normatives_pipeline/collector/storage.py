"""Слой storage: запись файлов в norm-base с контролем целостности."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


class FileStorage:
    def __init__(self, root: Path) -> None:
        self._root = root

    def save(self, filename: str, content: bytes) -> tuple[Path, str]:
        self._root.mkdir(parents=True, exist_ok=True)
        dest = self._root / self._safe_name(filename)
        dest.write_bytes(content)
        return dest, hashlib.sha256(content).hexdigest()

    @staticmethod
    def _safe_name(name: str) -> str:
        return re.sub(r'[\\/:*?"<>|\r\n]+', "_", name).strip() or "unnamed"
