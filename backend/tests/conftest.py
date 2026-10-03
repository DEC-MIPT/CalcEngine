from collections.abc import Iterator
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.services.calculation as service_module
from app.models import Base
from app.schemas.calculation import CalculationTypeContract


@pytest.fixture
def sqlite_session() -> Iterator[Session]:
    """Сессия к пустой базе SQLite в памяти со всеми таблицами ``app.models``."""
    engine = create_engine("sqlite://", poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine)() as session:
        yield session
    engine.dispose()


@pytest.fixture
def engine_calls(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Имена типов расчёта, с которыми сервис вызвал движок, по порядку вызовов."""
    calls: list[str] = []
    original = service_module.calculate

    def spy(contract: CalculationTypeContract, *args: Any, **kwargs: Any) -> Any:
        calls.append(contract.name)
        return original(contract, *args, **kwargs)

    monkeypatch.setattr(service_module, "calculate", spy)
    return calls
