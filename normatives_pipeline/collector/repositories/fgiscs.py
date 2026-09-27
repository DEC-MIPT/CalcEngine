"""Доступ к открытым данным ФГИС ЦС (fgiscs.minstroyrf.ru)."""

from __future__ import annotations

import requests

from ...core import SourceConfig
from ..models import Document


class FgiscsRepository:
    def __init__(self, source: SourceConfig, user_agent: str) -> None:
        self._base = source.base_url
        self._headers = {
            "User-Agent": user_agent,
            "Referer": source.params.get("referer", ""),
        }

    def list_datasets(self) -> list[Document]:
        resp = requests.get(f"{self._base}/api/opendata", headers=self._headers, timeout=30)
        resp.raise_for_status()
        return [self._to_document(item) for item in resp.json()["items"]]

    def download(self, document: Document) -> bytes:
        dataset_id = document.extra.get("id")
        if not dataset_id:
            raise ValueError(f"нет идентификатора датасета: {document.designation}")
        detail = requests.get(
            f"{self._base}/api/opendata/{dataset_id}",
            headers=self._headers,
            timeout=30,
        )
        detail.raise_for_status()
        path = (detail.json().get("datasetFile") or {}).get("path")
        if not path:
            raise ValueError(f"нет файла датасета: {document.designation}")
        resp = requests.get(
            f"{self._base}/api/values/GetFileContent/{path}",
            headers=self._headers,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.content

    @staticmethod
    def _to_document(item: dict) -> Document:
        return Document(
            source="fgiscs",
            designation=item.get("datasetName", ""),
            title=item.get("identificationNumber", ""),
            extra={"id": str(item.get("id", ""))},
        )
