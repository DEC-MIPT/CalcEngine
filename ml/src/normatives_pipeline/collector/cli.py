"""Точка входа коллектора: сбор по источникам из конфига sources.toml."""

from __future__ import annotations

import re

from ..core import Settings
from .repositories import FaufccRepository, PravoRepository
from .services import CollectService
from .storage import FileStorage

# TODO(будущее): пользователь чаще пишет «Свайные фундаменты», «Основания зданий и
# сооружений», «канализация», а не номер СП. Нужен поиск по названию/синонимам, а не
# по обозначению. Пока — подход «в лоб» по номерам.
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


def main() -> None:
    settings = Settings.load()
    storage = FileStorage(settings.output_dir)
    service = CollectService(storage)

    faufcc = FaufccRepository(settings.sources["faufcc"], settings.user_agent)
    for base, title in SP_TARGETS.items():
        documents = _resolve_sp(faufcc, base)
        if not documents:
            print(f"[faufcc] {base} — нет записей ({title})")
            continue
        service.collect(faufcc, documents, suffix=".pdf")

    # fgiscs — отложено до лучших времён (сметные нормативы, для расчётов не нужны).
    # fgiscs = FgiscsRepository(settings.sources["fgiscs"], settings.user_agent)
    # service.collect(fgiscs, fgiscs.list_datasets(), suffix=".csv")

    pravo = PravoRepository(settings.sources["pravo"], settings.user_agent)
    pravo_docs = pravo.search(
        authority_id=settings.sources["pravo"].params["minstroy_id"],
        page_size=30,
    )[:5]
    service.collect(pravo, pravo_docs, suffix=".pdf")


if __name__ == "__main__":
    main()
