import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.calculation import QuantityValue, ResultEnvelope


class NormSource(BaseModel):
    """Нормативный документ результата: документ и его редакция."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    document: str = Field(min_length=1)
    edition: str = Field(min_length=1)


class StoredResult(BaseModel):
    """Сохранённый результат расчёта в виде, который отдаёт сервис.

    Всё, что нужно для повторного запуска и сравнения (``calculation-api``
    «Reproducible stored result»). Сервис строит его из строки базы, поэтому ни один
    объект ``app.models`` не выходит за пределы ``services``.

    Attributes:
        result_id: идентификатор результата.
        calculation_type: имя типа расчёта.
        inputs: входы в том виде, в каком их дал запрос, с единицами.
        envelope: конверт результата, равный возвращённому при создании.
        engine_version: версия движка, посчитавшего результат.
        input_hash: хеш входных данных.
        created_at: время сохранения, заданное базой.
        norm_sources: различные документы и редакции из ``norm_refs`` конверта в
            порядке первого использования.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    result_id: UUID
    calculation_type: str = Field(min_length=1)
    inputs: dict[str, QuantityValue]
    envelope: ResultEnvelope
    engine_version: str = Field(min_length=1)
    input_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    created_at: datetime.datetime
    norm_sources: tuple[NormSource, ...]
