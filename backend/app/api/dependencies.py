from collections.abc import Iterator

from fastapi import Request
from pydantic import ValidationError
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings
from app.core.exceptions import DatabaseUnavailableError
from app.db.session import get_engine, get_session_factory


def _session_factory(request: Request) -> sessionmaker[Session]:
    """The application's session factory, built at the first request that needs ``dec_app``.

    A missing or malformed ``DEC_APP_DATABASE_URL`` becomes ``DatabaseUnavailableError``;
    its text is not carried on, since it can hold the URL (design.md decision 7).
    """
    state = request.app.state
    if state.session_factory is None:
        try:
            state.session_factory = get_session_factory(get_engine(Settings()))  # type: ignore[call-arg]
        except (ValidationError, ArgumentError):
            raise DatabaseUnavailableError("the application database is not configured") from None
    factory: sessionmaker[Session] = state.session_factory
    return factory


def get_session(request: Request) -> Iterator[Session]:
    """One session per request, committed when the route returns without an error."""
    with _session_factory(request)() as session:
        yield session
        session.commit()
