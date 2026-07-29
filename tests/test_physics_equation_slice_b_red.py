"""AT-TDD: LISS-0116 Slice B — EquationNode sides/dynamics + verifier."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.physics_equation import (
        Coefficient,
        EquationNode,
        Unit,
        verify_physics_equation,
    )
    from compiler.staqex.physics_ir import SourceOrigin

    return Coefficient, EquationNode, Unit, SourceOrigin, verify_physics_equation


def test_equation_node_is_importable() -> None:
    _, EquationNode, _, _, verify_physics_equation = _load_api()
    assert EquationNode is not None
    assert callable(verify_physics_equation)


def test_equation_retains_sides_coefficients_and_provenance() -> None:
    Coefficient, EquationNode, Unit, SourceOrigin, verify = _load_api()

    origin = SourceOrigin(source_id="oscillator.sqx", line=12, col=1)
    unit = Unit(symbol="J", dimensions=(1, 1, -2), origin=origin)
    coeff = Coefficient(expression="omega", unit=unit, origin=origin)
    equation = EquationNode(
        kind="dynamics",
        left="H",
        right="omega * N",
        coefficients=(coeff,),
        origin=origin,
    )

    assert equation.kind == "dynamics"
    assert equation.left == "H"
    assert equation.right == "omega * N"
    assert equation.coefficients == (coeff,)
    assert equation.origin == origin
    try:
        equation.kind = "equality"  # type: ignore[misc]
        mutated = True
    except (AttributeError, TypeError):
        mutated = False
    assert mutated is False, "EquationNode must be immutable"
    assert verify(equation) == []


def test_equation_without_provenance_is_rejected() -> None:
    Coefficient, EquationNode, Unit, SourceOrigin, verify = _load_api()

    origin = SourceOrigin(source_id="oscillator.sqx", line=1, col=1)
    unit = Unit(symbol="1", dimensions=(0, 0, 0), origin=origin)
    coeff = Coefficient(expression="1", unit=unit, origin=origin)
    equation = EquationNode(
        kind="equality",
        left="E",
        right="hbar * omega",
        coefficients=(coeff,),
        origin=None,
    )

    diagnostics = verify(equation)
    assert any(
        diagnostic.get("code") == "PHYSICS_EQUATION_PROVENANCE_ERROR"
        for diagnostic in diagnostics
    ), diagnostics


def test_equation_rejects_nested_coefficient_without_unit() -> None:
    Coefficient, EquationNode, _, SourceOrigin, verify = _load_api()

    origin = SourceOrigin(source_id="ising.sqx", line=4, col=2)
    bad = Coefficient(expression="J", unit=None, origin=origin)
    equation = EquationNode(
        kind="equality",
        left="H",
        right="J * Z",
        coefficients=(bad,),
        origin=origin,
    )

    diagnostics = verify(equation)
    assert any(
        diagnostic.get("code") == "PHYSICS_EQUATION_UNIT_ERROR"
        for diagnostic in diagnostics
    ), diagnostics


if __name__ == "__main__":
    try:
        test_equation_node_is_importable()
        test_equation_retains_sides_coefficients_and_provenance()
        test_equation_without_provenance_is_rejected()
        test_equation_rejects_nested_coefficient_without_unit()
    except Exception as exc:
        print(f"RED: {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc
    print("OK — LISS-0116 Slice B")
