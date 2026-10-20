import hashlib
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from app.engine.hashing import canonical_json
from app.parameters.interim_loader import InterimDocument
from app.parameters.interim_schemas import InterimRecord, VerificationStatus

logger = logging.getLogger("app.services.interim_data")

Profile = Literal["strict", "draft"]


def record_digest(record: InterimRecord) -> str:
    """SHA-256 канонической сериализации записи без её ``verification`` (design.md, решение 3).

    Args:
        record: запись временного источника.

    Returns:
        Шестнадцатеричная строка из 64 символов.
    """
    content = record.model_dump(mode="json", exclude={"verification"})
    return hashlib.sha256(canonical_json(content).encode("utf-8")).hexdigest()


def effective_status(record: InterimRecord) -> VerificationStatus:
    """Статус записи с учётом её ``value_digest``.

    Запись ``human-verified``, чей текущий digest не равен записанному, считается
    ``pending``: значение изменили после проверки. Код статус не повышает.

    Args:
        record: запись временного источника.

    Returns:
        Действующий статус записи.
    """
    verification = record.verification
    if verification.status == "human-verified" and verification.value_digest != record_digest(record):
        return "pending"
    return verification.status


@dataclass(frozen=True)
class CheckedRecord:
    """Запись с её местом в файле и действующим статусом.

    Attributes:
        path: путь записи в файле, например ``formulas[0]``.
        record: запись.
        status: действующий статус (``effective_status``).
    """

    path: str
    record: InterimRecord
    status: VerificationStatus


@dataclass(frozen=True)
class InterimTypeData:
    """Проверенные данные одного типа расчёта.

    Attributes:
        calculation_type: тип расчёта.
        file: путь файла от корня данных.
        records: записи файла в его порядке.
    """

    calculation_type: str
    file: str
    records: tuple[CheckedRecord, ...]


def check_documents(documents: Sequence[InterimDocument], profile: Profile) -> dict[str, InterimTypeData]:
    """Проверяет записи верификации документов при старте (design.md, решения 3 и 4).

    Строка лога называет каждую запись ``human-verified``, чьё значение изменили после
    проверки, а в профиле ``strict`` — каждую запись, которая не ``human-verified``.
    Значения в лог не попадают.

    Args:
        documents: документы загрузчика.
        profile: профиль временного источника.

    Returns:
        Данные каждого типа, у которого есть файл.
    """
    found: dict[str, InterimTypeData] = {}
    for document in documents:
        for data_file in document.files:
            records: list[CheckedRecord] = []
            for path, record in data_file.content.records():
                status = effective_status(record)
                if status != record.verification.status:
                    logger.warning("code=interim_value_changed file=%s record=%s", data_file.path, path)
                if profile == "strict" and status != "human-verified":
                    logger.warning(
                        "code=interim_record_unchecked file=%s record=%s status=%s", data_file.path, path, status
                    )
                records.append(CheckedRecord(path=path, record=record, status=status))
            found[data_file.calculation_type] = InterimTypeData(
                calculation_type=data_file.calculation_type, file=data_file.path, records=tuple(records)
            )
    return found
