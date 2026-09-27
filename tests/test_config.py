"""Конфиг пайплайна: секции parser и output загружаются."""

from __future__ import annotations

from normatives_pipeline.config import output_config, parser_config


def test_parser_config_patterns() -> None:
    cfg = parser_config()
    assert "clause_re" in cfg
    assert len(cfg["formula_num_res"]) >= 2
    assert "gde_re" in cfg


def test_parser_config_maps() -> None:
    cfg = parser_config()
    assert cfg["greek_map"]["γ"] == "\\gamma"
    assert cfg["cyr_map"]["с"] == "s"


def test_output_config_keys() -> None:
    cfg = output_config()
    assert cfg["formula_keys"] == ["norm_ref", "formula_id", "latex", "symbols", "expression", "cross_refs"]
    assert cfg["norm_ref_keys"] == ["document", "edition", "clause", "status", "provenance"]
    assert "id" in cfg["symbol_keys"]
    assert cfg["default_symbol_kind"]
