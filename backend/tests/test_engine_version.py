import ast
import tomllib
from pathlib import Path

import app.engine
from app.engine import ENGINE_VERSION
from app.engine.boundary import make_outputs
from app.engine.result import assemble_result
from app.engine.steps import check_step
from app.schemas.calculation import (
    CalculationTypeContract,
    NormRef,
    OutputDeclaration,
    QuantityDeclaration,
    QuantityValue,
    RoundingRule,
)
from app.schemas.parameters import EngineerRule
from app.schemas.text import LocalizedText

BACKEND = Path(__file__).resolve().parents[1]
ENGINE = Path(app.engine.__file__).parent


def test_engine_version_equals_the_backend_package_version() -> None:
    project = tomllib.loads((BACKEND / "pyproject.toml").read_text(encoding="utf-8"))

    assert ENGINE_VERSION == project["project"]["version"]


def test_a_result_carries_the_engine_version() -> None:
    reference = NormRef(
        document="<NORM-DOC-PLACEHOLDER>",
        edition="unverified",
        clause="<CLAUSE-PLACEHOLDER>",
        status="unverified",
        provenance="machine-extracted",
    )
    rule = EngineerRule(engineer="<ENGINEER>", rationale="<RATIONALE>")
    contract = CalculationTypeContract(
        name="synthetic",
        inputs=(QuantityDeclaration(name="x", label=LocalizedText(ru="x"), symbol="x", base_unit="m"),),
        outputs=(
            OutputDeclaration(
                name="y",
                label=LocalizedText(ru="y"),
                symbol="y",
                base_unit="m",
                rounding_rule=RoundingRule(decimals=1, mode="half_up"),
                rounding_source=rule,
            ),
        ),
        checks=("check",),
    )
    one = QuantityValue(value=1.0, unit="m")
    check = check_step("check", ("x", one), "le", ("x_{max}", one), (reference,))

    result = assemble_result(
        contract,
        input_hash="0" * 64,
        trace=(check,),
        outputs=make_outputs(contract, {"y": one}),
        warnings=(),
        validated_range=(),
    )

    assert result.engine_version == ENGINE_VERSION


def test_no_engine_module_reads_package_metadata() -> None:
    for module in ENGINE.glob("*.py"):
        syntax = ast.parse(module.read_text(encoding="utf-8"))
        imported = {
            node.module if isinstance(node, ast.ImportFrom) else alias.name
            for node in ast.walk(syntax)
            if isinstance(node, ast.Import | ast.ImportFrom)
            for alias in node.names
        }
        assert not any(name and name.startswith("importlib") for name in imported), module
