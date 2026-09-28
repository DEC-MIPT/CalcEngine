from app.core.exceptions import DECError, NotFoundError


def test_not_found_error_is_a_dec_error() -> None:
    assert issubclass(NotFoundError, DECError)
    assert isinstance(NotFoundError("missing"), DECError)
