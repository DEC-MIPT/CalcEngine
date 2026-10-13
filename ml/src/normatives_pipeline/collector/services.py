"""Слой services: бизнес-логика сбора документов."""

from __future__ import annotations

import time
from typing import Protocol

from .models import Document
from .storage import FileStorage

_RETRY_DELAYS = (2, 5, 10)


class Repository(Protocol):
    def download(self, document: Document) -> bytes: ...


class CollectService:
    def __init__(self, storage: FileStorage) -> None:
        self._storage = storage

    def collect(self, repository: Repository, documents: list[Document], suffix: str = ".pdf") -> None:
        for document in documents:
            content = self._download_with_retry(repository, document)
            if content is None:
                continue
            path, sha256, is_new = self._storage.save(f"{document.designation}{suffix}", content)
            status = "saved" if is_new else "duplicate"
            print(
                f"[{document.source}] {document.designation} -> {path.name} "
                f"({path.stat().st_size} bytes, sha256 {sha256[:16]}..., {status})"
            )

    def _download_with_retry(self, repository: Repository, document: Document) -> bytes | None:
        last_exc: Exception | None = None
        for attempt, delay in enumerate((*_RETRY_DELAYS, None), start=1):
            try:
                return repository.download(document)
            except ValueError as exc:
                print(f"[{document.source}] {document.designation} — {exc}")
                return None
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                if delay is not None:
                    print(f"[{document.source}] {document.designation} — retry {attempt}: {exc}")
                    time.sleep(delay)
        print(f"[{document.source}] {document.designation} — failed after retries: {last_exc}")
        return None
