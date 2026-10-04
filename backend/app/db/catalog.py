import threading

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import NormativesSettings
from app.core.exceptions import CatalogUnavailableError
from app.db.session import as_psycopg_url

READ_ONLY_OPTIONS = "-c default_transaction_read_only=on"
"""Опция подключения: каждая транзакция каталога только читает, даже при неверной роли."""


def get_catalog_engine(url: str) -> Engine:
    """Строит движок каталога норм (``normative-catalog-backend`` design.md, решение 4).

    Args:
        url: URL ``dec_normatives`` с ролью ``dec_normatives_reader``.

    Returns:
        Движок с только читающими подключениями, скрытыми параметрами запросов и
        проверкой подключения перед выдачей из пула.

    Raises:
        ArgumentError: если URL не разбирается.
        ValueError: если порт в URL не число.
    """
    return create_engine(
        as_psycopg_url(url),
        hide_parameters=True,
        pool_pre_ping=True,
        connect_args={"options": READ_ONLY_OPTIONS},
    )


class CatalogSessions:
    """Фабрика сессий каталога, построенная при первом обращении к ней.

    Каталог не нужен для старта приложения (спецификация "Catalog unavailability"),
    поэтому движок строится лениво, под блокировкой: два первых одновременных запроса
    строят один движок. Движок, построенный здесь, освобождается в ``dispose``;
    переданную готовую фабрику освобождает тот, кто её создал.

    Args:
        factory: готовая фабрика сессий (тесты); без неё фабрика строится из
            ``NormativesSettings``.
    """

    def __init__(self, factory: sessionmaker[Session] | None = None) -> None:
        self._factory = factory
        self._owned: Engine | None = None
        self._lock = threading.Lock()

    def factory(self) -> sessionmaker[Session]:
        """Возвращает фабрику сессий каталога, при первом вызове строя её.

        Returns:
            Фабрика сессий ``dec_normatives``.

        Raises:
            CatalogUnavailableError: если ``DEC_NORMATIVES_DATABASE_URL`` не задан или не
                разбирается; текст исходной ошибки не передаётся, потому что в нём может
                быть URL.
        """
        if self._factory is None:
            with self._lock:
                if self._factory is None:
                    url = NormativesSettings().dec_normatives_database_url
                    if url is None:
                        raise CatalogUnavailableError("the normative catalog is not configured")
                    try:
                        engine = get_catalog_engine(url.get_secret_value())
                    except (ArgumentError, ValueError):
                        raise CatalogUnavailableError("the normative catalog is not configured") from None
                    self._owned = engine
                    self._factory = sessionmaker(bind=engine, autoflush=False)
        return self._factory

    def dispose(self) -> None:
        """Освобождает движок, если его построила эта фабрика; переданную не трогает."""
        with self._lock:
            if self._owned is not None:
                self._owned.dispose()
                self._owned = None
                self._factory = None
