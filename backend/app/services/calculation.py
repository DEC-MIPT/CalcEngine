from collections.abc import Callable, Mapping, Sequence
from types import MappingProxyType
from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.core.exceptions import (
    CalculationTypeNotRegisteredError,
    NotFoundError,
    ParameterSourceUnavailableError,
)
from app.engine.pipeline import calculate
from app.engine.registry import CalculatorRegistry
from app.reporting.docx_writer import render_docx
from app.reporting.model import build_report
from app.repositories.calculation_result import CalculationResultRepository
from app.schemas.calculation import (
    CalculationRequest,
    CalculationResult,
    MethodBound,
    ParameterSourceInfo,
    QuantityValue,
    ResultEnvelope,
    ValidatedBound,
)
from app.schemas.report import ReportRequest
from app.schemas.stored import StoredResult
from app.services.parameter_source import ParameterSource

NO_SOURCES: Mapping[str, ParameterSource] = MappingProxyType({})
NO_RANGES: Mapping[str, Sequence[ValidatedBound]] = MappingProxyType({})


def norm_sources(envelope: CalculationResult) -> list[dict[str, str]]:
    """Перечисляет нормативные документы результата.

    Args:
        envelope: результат расчёта.

    Returns:
        Различные пары документа и редакции из ``norm_refs`` в порядке первого
        использования (``calculation-api`` design.md, решение 4).
    """
    pairs = dict.fromkeys((ref.document, ref.edition) for ref in envelope.norm_refs)
    return [{"document": document, "edition": edition} for document, edition in pairs]


class CalculationService:
    """Запускает зарегистрированный тип расчёта и сохраняет результат.

    ``run`` и ``envelope`` — путь движка без хранения (``calculation-core-contract``
    design.md, решение 12); ``submit`` — путь API: проверки, источник параметров,
    запуск и запись (``calculation-api`` design.md, решение 3).

    Args:
        registry: реестр типов расчёта.
        new_id: генератор ``result_id``.
        sources: источник нормативных параметров для каждого типа расчёта.
        validated_ranges: проверенный диапазон каждого типа из его ``.yaml``.
        results: репозиторий сохранённых результатов; нужен только ``submit``.
    """

    def __init__(
        self,
        registry: CalculatorRegistry,
        new_id: Callable[[], UUID] = uuid4,
        *,
        sources: Mapping[str, ParameterSource] = NO_SOURCES,
        validated_ranges: Mapping[str, Sequence[ValidatedBound]] = NO_RANGES,
        results: CalculationResultRepository | None = None,
    ) -> None:
        self._registry = registry
        self._new_id = new_id
        self._sources = sources
        self._validated_ranges = validated_ranges
        self._results = results

    def envelope(self, result: CalculationResult, source: ParameterSourceInfo | None = None) -> ResultEnvelope:
        """Превращает результат в конверт с новым ``result_id``.

        Args:
            result: результат расчёта.
            source: описание источника параметров; ``None`` — конверт без
                ``parameter_source`` (``interim-normatives-source`` design.md, решение 13).

        Returns:
            Конверт; все поля, кроме ``result_id`` и ``parameter_source``, — из результата.
        """
        return ResultEnvelope.model_validate(
            dict(result) | {"result_id": self._new_id(), "parameter_source": source}
        )

    def submit(self, request: CalculationRequest) -> ResultEnvelope:
        """Проверяет запрос, запускает расчёт и сохраняет результат.

        Порядок решения 3 дизайна: тип зарегистрирован, входы подходят к контракту,
        источник параметров настроен, затем запуск и запись. При любом отказе до
        запуска движок не вызывается и ничего не сохраняется. Отказ по диапазону
        метода — это результат, он сохраняется с вердиктом ``refused``.

        Args:
            request: запрос на расчёт, уже прошедший проверку схемы.

        Returns:
            Сохранённый конверт результата с новым ``result_id``.

        Raises:
            NotFoundError: если тип расчёта не зарегистрирован.
            InputValidationError: если входы не подходят к контракту.
            ParameterSourceUnavailableError: если у типа нет источника параметров.
            RuntimeError: если сервис создан без репозитория результатов.
        """
        results = self._repository()
        name = request.calculation_type
        request.check_against(self._registry.contract(name))
        source = self._sources.get(name)
        if source is None:
            raise ParameterSourceUnavailableError(
                f"No parameter source is configured for the calculation type {name!r}."
            )
        resolved = source.resolve(name, request.inputs)
        envelope = self.run(
            name,
            request.inputs,
            resolved.parameters,
            method_range=resolved.method_range,
            validated_range=self._validated_ranges.get(name, ()),
            source=resolved.source,
        )
        results.add(
            result_id=envelope.result_id,
            calculation_type=name,
            engine_version=envelope.engine_version,
            input_hash=envelope.input_hash,
            inputs={key: value.model_dump(mode="json") for key, value in request.inputs.items()},
            envelope=envelope.model_dump(mode="json"),
            norm_sources=norm_sources(envelope),
        )
        return envelope

    def get(self, result_id: UUID) -> StoredResult:
        """Читает сохранённый результат.

        Args:
            result_id: идентификатор результата.

        Returns:
            Сохранённая запись; её конверт равен конверту, который вернул ``submit``.

        Raises:
            NotFoundError: если результата с таким идентификатором нет.
            RuntimeError: если сервис создан без репозитория результатов.
        """
        row = self._repository().get(result_id)
        if row is None:
            raise NotFoundError(f"no stored result {result_id}")
        return StoredResult.model_validate(
            {
                "result_id": row.result_id,
                "calculation_type": row.calculation_type,
                "inputs": row.inputs,
                "envelope": row.envelope,
                "engine_version": row.engine_version,
                "input_hash": row.input_hash,
                "created_at": row.created_at,
                "norm_sources": row.norm_sources,
            }
        )

    def report(self, result_id: UUID, report_request: ReportRequest) -> bytes:
        """Строит отчёт ``.docx`` по сохранённому результату.

        Отчёт собирается из сохранённых входов и конверта и контракта типа из реестра
        (``calculation-api`` design.md, решение 9); расчёт заново не запускается.

        Args:
            result_id: идентификатор сохранённого результата.
            report_request: данные основной надписи и подписей.

        Returns:
            Содержимое файла ``.docx``.

        Raises:
            NotFoundError: если результата с таким идентификатором нет.
            CalculationTypeNotRegisteredError: если тип расчёта результата больше не
                зарегистрирован: результат есть, поэтому это не ``NotFoundError``.
            RuntimeError: если сервис создан без репозитория результатов.
        """
        stored = self.get(result_id)
        try:
            contract = self._registry.contract(stored.calculation_type)
        except NotFoundError:
            raise CalculationTypeNotRegisteredError(
                f"The calculation type {stored.calculation_type!r} of this result is no longer registered."
            ) from None
        return render_docx(build_report(contract, stored.inputs, stored.envelope, report_request))

    def _repository(self) -> CalculationResultRepository:
        if self._results is None:
            raise RuntimeError("CalculationService needs a result repository to store or read results")
        return self._results

    def run(
        self,
        calculation_type: str,
        inputs: Mapping[str, QuantityValue],
        parameters: object,
        *,
        method_range: Sequence[MethodBound] = (),
        validated_range: Sequence[ValidatedBound] = (),
        source: ParameterSourceInfo | None = None,
    ) -> ResultEnvelope:
        result = calculate(
            self._registry.contract(calculation_type),
            self._registry.get(calculation_type),
            inputs,
            parameters,
            method_range=method_range,
            validated_range=validated_range,
            module=self._registry.module(calculation_type),
        )
        return self.envelope(result, source)


def calculation_service(
    session: Session,
    registry: CalculatorRegistry,
    *,
    sources: Mapping[str, ParameterSource],
    validated_ranges: Mapping[str, Sequence[ValidatedBound]],
) -> CalculationService:
    """Собирает сервис для одного запроса с репозиторием на его сессии.

    Слой ``api`` не импортирует ``repositories`` (``backend-architecture``, порядок
    слоёв), поэтому репозиторий создаётся здесь.

    Args:
        session: сессия ``dec_app`` этого запроса.
        registry: реестр типов расчёта.
        sources: источник нормативных параметров для каждого типа.
        validated_ranges: проверенный диапазон каждого типа.

    Returns:
        Сервис, который пишет и читает результаты через эту сессию.
    """
    return CalculationService(
        registry,
        sources=sources,
        validated_ranges=validated_ranges,
        results=CalculationResultRepository(session),
    )
