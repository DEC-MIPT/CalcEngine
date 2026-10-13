"""Доступ к реестру сводов правил ФАУ ФЦС (api.faufcc.ru)."""

from __future__ import annotations

import json

import requests

from ...core import SourceConfig
from ..models import Document


class FaufccRepository:
    def __init__(self, source: SourceConfig, user_agent: str) -> None:
        self._base = source.base_url
        self._registry = source.params["sp_registry_id"]
        self._headers = {"User-Agent": user_agent}

    def search(self, term: str) -> list[Document]:
        filters = json.dumps(
            {"registry": self._registry, "search": term},
            ensure_ascii=False,
        )
        params: dict[str, str | int] = {
            "page": 1,
            "filters": filters,
            "include": "asset",
        }
        resp = requests.get(
            f"{self._base}/registries/entries",
            params=params,
            headers=self._headers,
            timeout=30,
        )
        resp.raise_for_status()
        return [self._to_document(entry) for entry in resp.json()["data"]]

    def download(self, document: Document) -> bytes:
        if not document.download_url:
            raise ValueError(f"нет файла для скачивания: {document.designation}")
        resp = requests.get(document.download_url, headers=self._headers, timeout=120)
        resp.raise_for_status()
        return resp.content

    @staticmethod
    def _to_document(entry: dict) -> Document:
        asset = entry.get("asset", {}).get("data") or {}
        state = entry.get("state") or {}
        return Document(
            source="faufcc",
            designation=(entry.get("number") or "").strip(),
            title=(entry.get("name") or "").strip(),
            edition=(entry.get("year") or "").strip() or None,
            download_url=(asset.get("links") or {}).get("download"),
            state=state.get("title"),
        )
