class DECError(Exception):
    """Base class for every backend-defined exception."""


class NotFoundError(DECError):
    """Raised when a requested resource does not exist."""


class AlreadyRegisteredError(DECError):
    """Raised when a name is registered twice."""


class ParameterValidationError(DECError):
    """Raised when parameter data fails schema validation."""


class ExpressionError(DECError):
    """Raised when a formula's expression tree cannot be checked or evaluated."""


class UnitError(DECError):
    """Raised when a value does not carry the unit the calculation expects."""


class CalculationError(DECError):
    """Raised when the parts a calculator produced do not form a valid result."""


class InputValidationError(DECError):
    """Raised when a calculation request does not fit its calculation type's contract."""
