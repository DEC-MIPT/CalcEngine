"""Слой storage: запись файлов в norm-base с контролем целостности."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


class FileStorage:
    def __init__(self, root: Path) -> None:
        self._root = root

    def save(self, filename: str, content: bytes) -> tuple[Path, str, bool]:
        """Save content to file; return (path, sha256_hex, is_new).

        Deduplicates by sha256: if a file with the same hash already exists
        under any name in root, returns that file and is_new=False.
        """
        sha256 = hashlib.sha256(content).hexdigest()
        self._root.mkdir(parents=True, exist_ok=True)
        for existing in self._root.iterdir():
            if existing.is_file() and hashlib.sha256(existing.read_bytes()).hexdigest() == sha256:
                return existing, sha256, False
        dest = self._root / self._safe_name(filename)
        dest.write_bytes(content)
        return dest, sha256, True

    @staticmethod
    def _safe_name(name: str) -> str:
        return re.sub(r'[\\/:*?"<>|\r\n]+', "_", name).strip() or "unnamed"
