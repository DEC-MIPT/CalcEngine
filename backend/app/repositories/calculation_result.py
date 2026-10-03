import uuid
from collections.abc import Mapping, Sequence
from typing import Any

from sqlalchemy.orm import Session

from app.models.calculation_result import CalculationResultRow


class CalculationResultRepository:
    """Сохранённые результаты: добавляются один раз, читаются по ``result_id``, не изменяются и не удаляются.

    Требование ``calculation-api`` "Reproducible stored result".
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(
        self,
        *,
        result_id: uuid.UUID,
        calculation_type: str,
        engine_version: str,
        input_hash: str,
        inputs: Mapping[str, Any],
        envelope: Mapping[str, Any],
        norm_sources: Sequence[Mapping[str, str]],
    ) -> None:
        self._session.add(
            CalculationResultRow(
                result_id=result_id,
                calculation_type=calculation_type,
                engine_version=engine_version,
                input_hash=input_hash,
                inputs=dict(inputs),
                envelope=dict(envelope),
                norm_sources=[dict(source) for source in norm_sources],
            )
        )
        self._session.flush()

    def get(self, result_id: uuid.UUID) -> CalculationResultRow | None:
        return self._session.get(CalculationResultRow, result_id)
