"""Доступ к официальному API публикации правовых актов (pravo.gov.ru)."""

from __future__ import annotations

import requests

from ...core import SourceConfig
from ..models import Document


class PravoRepository:
    def __init__(self, source: SourceConfig, user_agent: str) -> None:
        self._base = source.base_url
        self._headers = {"User-Agent": user_agent}

    def search(
        self,
        name: str | None = None,
        authority_id: str | None = None,
        page_size: int = 30,
    ) -> list[Document]:
        params: dict[str, str | int] = {"PageSize": page_size}
        if name:
            params["Name"] = name
        if authority_id:
            params["SignatoryAuthorityId"] = authority_id
        resp = requests.get(
            f"{self._base}/api/Documents",
            params=params,
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        return [self._to_document(item) for item in resp.json().get("items", [])]

    def download(self, document: Document) -> bytes:
        if not document.download_url:
            raise ValueError(f"нет файла для скачивания: {document.designation}")
        resp = requests.get(document.download_url, headers=self._headers, timeout=120)
        resp.raise_for_status()
        return resp.content

    def _to_document(self, item: dict) -> Document:
        eo_number = item.get("eoNumber", "")
        number = (item.get("number") or "").strip()
        name = (item.get("name") or "").strip()
        return Document(
            source="pravo",
            designation=number or eo_number,
            title=name,
            download_url=f"{self._base}/file/pdf?eoNumber={eo_number}" if eo_number else None,
            extra={"eoNumber": eo_number},
        )
