import logging
from collections.abc import Callable

from pydantic import ValidationError

from app.core.exceptions import CatalogUnavailableError, NotFoundError
from app.db.catalog import UNREACHABLE, CatalogSessions
from app.repositories.normatives import NormativesRepository
from app.schemas.normatives import DocumentView, SearchResults

logger = logging.getLogger("app.services.normatives")


class NormativesService:
    """Поиск и чтение документов каталога норм для эндпоинтов ``/normatives``.

    Каждый вызов читает каталог в одной короткой сессии. Ненастроенный или недоступный
    каталог даёт ``CatalogUnavailableError`` без текста драйвера, потому что в нём может
    быть URL (``normative-catalog-backend`` design.md, решения 4 и 5). Строка каталога,
    которая не проходит модель ответа, даёт тот же ``CatalogUnavailableError`` и одну
    строку лога без значений (решение 7).

    Args:
        sessions: фабрика сессий каталога приложения.
    """

    def __init__(self, sessions: CatalogSessions) -> None:
        self._sessions = sessions

    def _read[T](self, endpoint: str, query: Callable[[NormativesRepository], T]) -> T:
        try:
            with self._sessions.factory()() as session:
                return query(NormativesRepository(session))
        except UNREACHABLE:
            raise CatalogUnavailableError("the normative catalog is not available") from None
        except ValidationError:
            logger.warning("code=catalog_data_invalid endpoint=%s", endpoint)
            raise CatalogUnavailableError("the normative catalog is not available") from None

    def search(self, query: str, limit: int) -> SearchResults:
        """Ищет документы, пункты и формулы (спецификация "Normative search endpoint").

        Args:
            query: текст поиска после обрезки пробелов по краям.
            limit: наибольшее число совпадений.

        Returns:
            Совпадения в порядке ранга каталога.

        Raises:
            CatalogUnavailableError: если каталог не настроен, не отвечает или отдал строку,
                которая не проходит модель ответа.
        """
        return SearchResults(hits=self._read("search", lambda repository: repository.search(query, limit)))

    def document(self, document_id: int) -> DocumentView:
        """Документ каталога с пунктами (спецификация "Normative document endpoint").

        Args:
            document_id: идентификатор документа в каталоге.

        Returns:
            Документ с пунктами в порядке документа.

        Raises:
            CatalogUnavailableError: если каталог не настроен, не отвечает или отдал строку,
                которая не проходит модель ответа.
            NotFoundError: если каталог не содержит документа.
        """
        found = self._read("document", lambda repository: repository.document(document_id))
        if found is None:
            raise NotFoundError("the normative document does not exist")
        return found
