from app.verification.invariants import InputRange, Invariant

PILOT_RANGES = (
    InputRange(quantity="b", lower=0.5, upper=20.0, unit="m"),
    InputRange(quantity="d_1", lower=0.5, upper=5.0, unit="m"),
    InputRange(quantity="d_b", lower=0.0, upper=2.0, unit="m"),
    InputRange(quantity="gamma_II", lower=14.0, upper=22.0, unit="kN/m3"),
    InputRange(quantity="gamma_II_prime", lower=14.0, upper=22.0, unit="kN/m3"),
    InputRange(quantity="c_II", lower=0.0, upper=50.0, unit="kPa"),
    InputRange(quantity="phi_II", lower=0.0, upper=45.0, unit="deg", whole=True),
    InputRange(quantity="p", lower=50.0, upper=600.0, unit="kPa"),
)
"""Допустимый диапазон входов пилота; принят инженером (Аким) 2026-10-06, это не значения нормы."""

R_AFFINE_IN_C_II = Invariant(
    identifier="R-affine-in-c_II",
    statement="With the other inputs fixed, equal steps of c_II give equal steps of R.",
    quantities=("c_II", "R"),
)
R_AFFINE_IN_D_1 = Invariant(
    identifier="R-affine-in-d_1",
    statement="With the other inputs fixed, equal steps of d_1 give equal steps of R.",
    quantities=("d_1", "R"),
)
R_GROWS_WITH_C_II = Invariant(
    identifier="R-grows-with-c_II",
    statement="A larger c_II gives an R not smaller.",
    quantities=("c_II", "R"),
)
R_GROWS_WITH_GAMMA_II = Invariant(
    identifier="R-grows-with-gamma_II",
    statement="A larger gamma_II gives an R not smaller.",
    quantities=("gamma_II", "R"),
)
R_GROWS_WITH_D_B = Invariant(
    identifier="R-grows-with-d_b",
    statement="A larger d_b gives an R not smaller.",
    quantities=("d_b", "R"),
)
R_GROWS_WITH_B = Invariant(
    identifier="R-grows-with-b",
    statement="A larger b gives an R not smaller, across the k_z threshold too.",
    quantities=("b", "R"),
)
FORMULA_INVARIANTS = (
    R_AFFINE_IN_C_II,
    R_AFFINE_IN_D_1,
    R_GROWS_WITH_C_II,
    R_GROWS_WITH_GAMMA_II,
    R_GROWS_WITH_D_B,
    R_GROWS_WITH_B,
)
"""Инварианты пилота, зависящие от формулы R; подтверждены инженером (Аким) 2026-10-06 (задача 2.11).

Проверяются на формуле и коэффициентах загруженного каталога: дерево формулы в тесты не
пишется (WP2, задача 7.1b; ``agent-docs/domain-constraints.md``).
"""
