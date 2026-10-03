import pytest

from app.core.exceptions import (
    AlreadyRegisteredError,
    CalculationTypeNotRegisteredError,
    DatabaseUnavailableError,
    DECError,
    NotFoundError,
    ParameterSourceUnavailableError,
    ParameterValidationError,
)


def test_not_found_error_is_a_dec_error() -> None:
    assert issubclass(NotFoundError, DECError)
    assert isinstance(NotFoundError("missing"), DECError)


def test_already_registered_error_is_a_dec_error() -> None:
    assert issubclass(AlreadyRegisteredError, DECError)
    assert isinstance(AlreadyRegisteredError("twice"), DECError)


def test_parameter_validation_error_is_a_dec_error() -> None:
    assert issubclass(ParameterValidationError, DECError)
    assert isinstance(ParameterValidationError("invalid"), DECError)


@pytest.mark.parametrize(
    "error",
    [ParameterSourceUnavailableError, CalculationTypeNotRegisteredError, DatabaseUnavailableError],
)
def test_the_api_errors_are_dec_errors(error: type[DECError]) -> None:
    assert issubclass(error, DECError)
    assert isinstance(error("message"), DECError)
