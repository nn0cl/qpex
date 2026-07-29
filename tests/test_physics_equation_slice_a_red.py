"""AT-TDD Phase 1 Red: LISS-0116 Slice A — Coefficient / Unit DTOs."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    """Slice A Green must provide Coefficient, Unit, and module verifier."""
    from compiler.staqex.physics_equation import (
        Coefficient,
        Unit,
        verify_physics_equation,
    )
    from compiler.staqex.physics_ir import SourceOrigin

    return Coefficient, Unit, SourceOrigin, verify_physics_equation


def test_unit_and_coefficient_are_importable() -> None:
    Coefficient, Unit, SourceOrigin, verify_physics_equation = _load_api()

    assert Coefficient is not None
    assert Unit is not None
    assert SourceOrigin is not None
    assert callable(verify_physics_equation)


def test_unit_is_immutable_with_dimension_tags_and_provenance() -> None:
    _, Unit, SourceOrigin, _ = _load_api()

    origin = SourceOrigin(source_id="oscillator.sqx", line=3, col=1)
    unit = Unit(symbol="J", dimensions=(1, 1, -2), origin=origin)

    assert unit.symbol == "J"
    assert unit.dimensions == (1, 1, -2)
    assert unit.origin == origin
    try:
        unit.symbol = "eV"  # type: ignore[misc]
        mutated = True
    except (AttributeError, TypeError):
        mutated = False
    assert mutated is False, "Unit must be immutable"


def test_coefficient_retains_unit_and_provenance() -> None:
    Coefficient, Unit, SourceOrigin, verify_physics_equation = _load_api()

    origin = SourceOrigin(source_id="ising.sqx", line=8, col=5)
    unit = Unit(symbol="1", dimensions=(0, 0, 0), origin=origin)
    coefficient = Coefficient(
        expression="J",
        unit=unit,
        origin=origin,
    )

    assert coefficient.expression == "J"
    assert coefficient.unit is unit
    assert coefficient.origin == origin
    diagnostics = verify_physics_equation(coefficient)
    assert diagnostics == []


def test_coefficient_without_unit_is_rejected() -> None:
    Coefficient, _, SourceOrigin, verify_physics_equation = _load_api()

    origin = SourceOrigin(source_id="ising.sqx", line=9, col=5)
    coefficient = Coefficient(
        expression="J",
        unit=None,
        origin=origin,
    )

    diagnostics = verify_physics_equation(coefficient)
    assert any(
        diagnostic.get("code") == "PHYSICS_EQUATION_UNIT_ERROR"
        for diagnostic in diagnostics
    ), diagnostics


def test_coefficient_without_provenance_is_rejected() -> None:
    Coefficient, Unit, SourceOrigin, verify_physics_equation = _load_api()

    unit_origin = SourceOrigin(source_id="ising.sqx", line=1, col=1)
    unit = Unit(symbol="1", dimensions=(0, 0, 0), origin=unit_origin)
    coefficient = Coefficient(
        expression="h",
        unit=unit,
        origin=None,
    )

    diagnostics = verify_physics_equation(coefficient)
    assert any(
        diagnostic.get("code") == "PHYSICS_EQUATION_PROVENANCE_ERROR"
        for diagnostic in diagnostics
    ), diagnostics


if __name__ == "__main__":
    try:
        test_unit_and_coefficient_are_importable()
        test_unit_is_immutable_with_dimension_tags_and_provenance()
        test_coefficient_retains_unit_and_provenance()
        test_coefficient_without_unit_is_rejected()
        test_coefficient_without_provenance_is_rejected()
    except Exception as exc:
        print(f"RED (expected until Green): {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc
    print("OK — LISS-0116 Slice A")
    raise SystemExit(0)
