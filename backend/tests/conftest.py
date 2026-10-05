import secrets
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


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Выбирает seed Hypothesis на прогон, если он не задан опцией ``--hypothesis-seed``.

    Hypothesis сам печатает только провальный пример, а не seed, поэтому seed выбирается
    здесь и выводится в шапке отчёта (`calculation-verification` design.md, решение 16).

    Args:
        config: конфигурация pytest.
    """
    if config.getoption("hypothesis_seed") is None:
        config.option.hypothesis_seed = secrets.randbelow(2**32)


def pytest_report_header(config: pytest.Config) -> str:
    """Записывает seed Hypothesis в шапку отчёта, чтобы провальный прогон можно было повторить.

    Args:
        config: конфигурация pytest.

    Returns:
        Строка ``hypothesis seed: <n>``; прогон повторяется с ``--hypothesis-seed=<n>``.
    """
    return f"hypothesis seed: {config.getoption('hypothesis_seed')}"
