"""Immutable Equation / Unit DTO surface for LISS-0116 (Agent A).

Provides ``Unit``, ``Coefficient``, and ``EquationNode`` with a module-local
verifier. This module must not edit ``physics_ir.py``; it only imports
``SourceOrigin``.
"""

from __future__ import annotations

from dataclasses import dataclass

from .physics_ir import SourceOrigin

PHYSICS_EQUATION_UNIT_ERROR = "PHYSICS_EQUATION_UNIT_ERROR"
PHYSICS_EQUATION_PROVENANCE_ERROR = "PHYSICS_EQUATION_PROVENANCE_ERROR"
PhysicsEquationDiagnostic = dict[str, str]


@dataclass(frozen=True, slots=True)
class Unit:
    """A named unit with structured (L, M, T) dimension exponents."""

    symbol: str
    dimensions: tuple[int, int, int]
    origin: SourceOrigin


@dataclass(frozen=True, slots=True)
class Coefficient:
    """A symbolic coefficient retaining unit and source provenance."""

    expression: str
    unit: Unit | None
    origin: SourceOrigin | None


@dataclass(frozen=True, slots=True)
class EquationNode:
    """An equation or dynamics relation with inspectable sides and coefficients."""

    kind: str
    left: object
    right: object
    coefficients: tuple[Coefficient, ...]
    origin: SourceOrigin | None


def verify_physics_equation(
    value: Coefficient | Unit | EquationNode,
) -> list[PhysicsEquationDiagnostic]:
    """Return named diagnostics; never silently repair missing fields."""

    if isinstance(value, Unit):
        return _verify_unit(value)
    if isinstance(value, Coefficient):
        return _verify_coefficient(value)
    return _verify_equation(value)


def _verify_unit(unit: Unit) -> list[PhysicsEquationDiagnostic]:
    if unit.origin is None:
        return [_provenance_diagnostic("Unit")]
    return []


def _verify_coefficient(
    coefficient: Coefficient,
) -> list[PhysicsEquationDiagnostic]:
    diagnostics: list[PhysicsEquationDiagnostic] = []
    if coefficient.origin is None:
        diagnostics.append(_provenance_diagnostic("Coefficient"))
    if coefficient.unit is None:
        diagnostics.append(
            {
                "code": PHYSICS_EQUATION_UNIT_ERROR,
                "message": "Coefficient has no unit reference",
            }
        )
    else:
        diagnostics.extend(_verify_unit(coefficient.unit))
    return diagnostics


def _verify_equation(equation: EquationNode) -> list[PhysicsEquationDiagnostic]:
    diagnostics: list[PhysicsEquationDiagnostic] = []
    if equation.origin is None:
        diagnostics.append(_provenance_diagnostic("EquationNode"))
    for coefficient in equation.coefficients:
        diagnostics.extend(_verify_coefficient(coefficient))
    return diagnostics


def _provenance_diagnostic(kind: str) -> PhysicsEquationDiagnostic:
    return {
        "code": PHYSICS_EQUATION_PROVENANCE_ERROR,
        "message": f"{kind} has no source ancestry",
    }
