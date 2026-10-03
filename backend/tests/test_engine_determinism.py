import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_engine_purity import (
    CONTRACT,
    METHOD,
    PARAMETERS,
    VALIDATED,
    Parameters,
    SyntheticCalculator,
)

from app.engine.pipeline import calculate
from app.schemas.calculation import CalculationResult, QuantityValue

BACKEND = Path(__file__).resolve().parents[1]


def run_once(b: float, b_unit: str = "mm") -> CalculationResult:
    return calculate(
        CONTRACT,
        SyntheticCalculator(),
        {"b": QuantityValue(value=b, unit=b_unit), "phi": QuantityValue(value=20.0, unit="deg")},
        Parameters.model_validate(PARAMETERS.model_dump()),
        method_range=METHOD,
        validated_range=VALIDATED,
    )


@pytest.mark.parametrize("b", [6000.0, 200_000.0], ids=["completed", "refused"])
def test_two_runs_give_equal_results_that_serialize_to_identical_json(b: float) -> None:
    first, second = run_once(b), run_once(b)

    assert first is not second
    assert first == second
    assert first.model_dump_json() == second.model_dump_json()


def test_the_same_quantity_in_another_unit_gives_the_same_result() -> None:
    assert run_once(6000.0, "mm").model_dump_json() == run_once(6.0, "m").model_dump_json()


SCRIPT = """
import sys
sys.path.insert(0, "tests")
from test_engine_determinism import run_once
print(run_once(6000.0).model_dump_json())
"""


def test_the_result_does_not_depend_on_the_hash_seed() -> None:
    outputs = {
        subprocess.run(
            [sys.executable, "-c", SCRIPT],
            cwd=BACKEND,
            env=os.environ | {"PYTHONHASHSEED": seed},
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        for seed in ("1", "2", "3")
    }

    assert outputs == {run_once(6000.0).model_dump_json()}
