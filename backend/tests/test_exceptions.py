from app.core.exceptions import DECError, NotFoundError, ParameterValidationError


def test_not_found_error_is_a_dec_error() -> None:
    assert issubclass(NotFoundError, DECError)
    assert isinstance(NotFoundError("missing"), DECError)


def test_parameter_validation_error_is_a_dec_error() -> None:
    assert issubclass(ParameterValidationError, DECError)
    assert isinstance(ParameterValidationError("invalid"), DECError)
