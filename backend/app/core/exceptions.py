class DECError(Exception):
    """Базовый класс всех исключений бэкенда."""


class NotFoundError(DECError):
    """Запрошенного ресурса не существует."""


class AlreadyRegisteredError(DECError):
    """Имя регистрируется второй раз."""


class ParameterValidationError(DECError):
    """Данные параметров не проходят проверку схемы."""


class ExpressionError(DECError):
    """Дерево выражения формулы не проходит проверку или не вычисляется."""


class UnitError(DECError):
    """Значение не в той единице, которую ожидает расчёт."""


class CalculationError(DECError):
    """Части, которые выдал калькулятор, не складываются в корректный результат."""


class InputValidationError(DECError):
    """Запрос на расчёт не подходит к контракту своего типа расчёта.

    Attributes:
        fields: по одной записи на каждый неподходящий вход (``FieldError`` из
            ``app.schemas.api``); обработчик ошибок API кладёт их в тело ``422``.
    """

    def __init__(self, message: str, fields: tuple[object, ...] = ()) -> None:
        super().__init__(message)
        self.fields = fields


class ParameterSourceUnavailableError(DECError):
    """У зарегистрированного типа расчёта не настроен источник параметров."""


class CalculationTypeNotRegisteredError(DECError):
    """Тип расчёта сохранённого результата больше не зарегистрирован."""


class DatabaseUnavailableError(DECError):
    """База приложения не настроена или не отвечает."""


class CatalogUnavailableError(DECError):
    """Каталог норм не настроен или не отвечает."""
