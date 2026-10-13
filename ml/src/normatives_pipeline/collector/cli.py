"""Точка входа коллектора: сбор по источникам из конфига sources.toml."""

from __future__ import annotations

import argparse
import re

from ..core import Settings
from .repositories import FaufccRepository, PravoRepository
from .services import CollectService
from .storage import FileStorage

SP_TARGETS: dict[str, str] = {
    "22.13330": "Основания зданий и сооружений",
    "24.13330": "Свайные фундаменты",
    "45.13330": "Земляные сооружения, основания и фундаменты",
    "30.13330": "Внутренний водопровод и канализация зданий",
    "31.13330": "Водоснабжение. Наружные сети и сооружения",
    "32.13330": "Канализация. Наружные сети и сооружения",
}


def _resolve_sp(repository: FaufccRepository, base: str) -> list:
    pattern = re.compile(rf"^СП\s+{re.escape(base)}(\.\d+)?$")
    return [doc for doc in repository.search(base) if pattern.match(doc.designation)]


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Collect normative documents from registries")
    parser.add_argument("--source", choices=["faufcc", "pravo", "all"], default="all",
                        help="Registry source to collect from (default: all)")
    parser.add_argument("--document", metavar="DESIGNATION",
                        help="Collect only this document designation (e.g. '22.13330')")
    args = parser.parse_args(argv)

    settings = Settings.load()
    storage = FileStorage(settings.output_dir)
    service = CollectService(storage)

    targets = {args.document: SP_TARGETS.get(args.document, "")} if args.document else SP_TARGETS

    if args.source in ("faufcc", "all"):
        faufcc = FaufccRepository(settings.sources["faufcc"], settings.user_agent)
        for base, title in targets.items():
            documents = _resolve_sp(faufcc, base)
            if not documents:
                print(f"[faufcc] {base} — нет записей ({title})")
                continue
            service.collect(faufcc, documents, suffix=".pdf")

    if args.source in ("pravo", "all") and not args.document:
        pravo = PravoRepository(settings.sources["pravo"], settings.user_agent)
        pravo_docs = pravo.search(
            authority_id=settings.sources["pravo"].params["minstroy_id"],
            page_size=30,
        )[:5]
        service.collect(pravo, pravo_docs, suffix=".pdf")


if __name__ == "__main__":  # pragma: no cover
    main()
