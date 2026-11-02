import hashlib
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from typing import Literal

from app.engine.hashing import canonical_json
from app.parameters.interim_loader import MANIFEST, InterimDocument
from app.parameters.interim_schemas import (
    InterimManifest,
    InterimRecord,
    VerificationStatus,
)

logger = logging.getLogger("app.services.interim_data")

Profile = Literal["strict", "draft"]


def _sha256(data: object) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def record_digest(record: InterimRecord) -> str:
    """SHA-256 канонической сериализации записи без её ``verification`` (design.md, решение 3).

    Args:
        record: запись временного источника.

    Returns:
        Шестнадцатеричная строка из 64 символов.
    """
    return _sha256(record.model_dump(mode="json", exclude={"verification"}))


def document_digest(document: InterimDocument) -> str:
    """SHA-256 проверенного содержимого каталога документа (design.md, решение 6).

    Манифест и файлы типов берутся как проверенные данные, в порядке их путей от каталога
    документа, и сериализуются ``canonical_json``: ключи отсортированы, разделители
    фиксированы, UTF-8, числа — как в хеше движка. Digest покрывает каждое значение,
    ссылку, страницу и запись проверки и не зависит от комментариев YAML, порядка ключей
    и отступов.

    Args:
        document: документ загрузчика.

    Returns:
        Шестнадцатеричная строка из 64 символов.
    """
    contents = {MANIFEST: document.manifest.model_dump(mode="json")} | {
        data_file.path.rsplit("/", 1)[-1]: data_file.content.model_dump(mode="json") for data_file in document.files
    }
    return _sha256([{"path": path, "content": contents[path]} for path in sorted(contents)])


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
        data_sha256: digest документа, которому принадлежит файл.
        records: записи файла в его порядке.
    """

    calculation_type: str
    file: str
    data_sha256: str
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
        digest = document_digest(document)
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
                calculation_type=data_file.calculation_type,
                file=data_file.path,
                data_sha256=digest,
                records=tuple(records),
            )
    return found


def sunset_passed(manifest: InterimManifest, today: date) -> bool:
    """Прошла ли дата отключения временного источника (design.md, решение 8).

    Args:
        manifest: манифест документа.
        today: сегодняшняя дата; в день отключения срок ещё не прошёл.

    Returns:
        ``True``, если сегодня позже даты отключения.
    """
    return today > manifest.sunset.date


def warn_passed_sunsets(documents: Sequence[InterimDocument], today: date) -> tuple[str, ...]:
    """Пишет предупреждение о каждом документе, чей срок прошёл; приложение стартует.

    Строка называет документ, дату и событие, которое закрывает источник.

    Args:
        documents: документы загрузчика.
        today: сегодняшняя дата.

    Returns:
        Имена каталогов документов с прошедшим сроком.
    """
    passed = tuple(document for document in documents if sunset_passed(document.manifest, today))
    for document in passed:
        logger.warning(
            "code=interim_sunset_passed document=%s date=%s event=%s",
            document.name,
            document.manifest.sunset.date.isoformat(),
            document.manifest.sunset.event,
        )
    return tuple(document.name for document in passed)
