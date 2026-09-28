from sqlalchemy.orm import DeclarativeBase

from app.models import Base


def test_base_is_a_declarative_base_with_metadata() -> None:
    assert issubclass(Base, DeclarativeBase)
    assert Base.metadata is not None
