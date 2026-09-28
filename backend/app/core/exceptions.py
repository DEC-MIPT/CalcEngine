class DECError(Exception):
    """Base class for every backend-defined exception."""


class NotFoundError(DECError):
    """Raised when a requested resource does not exist."""


class ParameterValidationError(DECError):
    """Raised when parameter data fails schema validation."""
