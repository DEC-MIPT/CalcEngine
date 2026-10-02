"""Слой services: бизнес-логика сбора документов."""

from __future__ import annotations

from typing import Protocol

from .models import Document
from .storage import FileStorage


class Repository(Protocol):
    def download(self, document: Document) -> bytes: ...


class CollectService:
    def __init__(self, storage: FileStorage) -> None:
        self._storage = storage

    def collect(self, repository: Repository, documents: list[Document], suffix: str = ".pdf") -> None:
        for document in documents:
            try:
                content = repository.download(document)
            except ValueError as exc:
                print(f"[{document.source}] {document.designation} — {exc}")
                continue
            path, sha256 = self._storage.save(f"{document.designation}{suffix}", content)
            print(
                f"[{document.source}] {document.designation} -> {path.name} "
                f"({path.stat().st_size} bytes, sha256 {sha256[:16]}...)"
            )
