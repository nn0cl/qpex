"""Host-side validation for symbolic circuit parameters (LISS-0027 / ADR 0070)."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Mapping

from .ast_nodes import Call, CompilationUnit, LitString, StateBind, Var
from .qpu_ir import QpuProgram

PARAM_BINDING_MISSING = "PARAM_BINDING_MISSING"
PARAM_BINDING_UNKNOWN = "PARAM_BINDING_UNKNOWN"
PARAM_BINDING_VALUE_ERROR = "PARAM_BINDING_VALUE_ERROR"


@dataclass(frozen=True)
class CircuitParameter:
    """One declared symbolic parameter in a static/parametric QPU program."""

    name: str
    domain: str


def extract_circuit_parameters(unit: CompilationUnit) -> tuple[CircuitParameter, ...]:
    """Read declared `Param<T>` bindings from `main` in source order."""
    if unit.main is None:
        return ()
    params: list[CircuitParameter] = []
    for stmt in unit.main.body.stmts:
        if not isinstance(stmt, StateBind):
            continue
        declared = _parameter_decl_from_bind(stmt)
        if declared is not None:
            params.append(declared)
    return tuple(params)


def extract_circuit_parameters_from_program(program: QpuProgram) -> tuple[CircuitParameter, ...]:
    raw = program.get("parameters", ())
    return tuple(
        CircuitParameter(name=str(item["name"]), domain=str(item.get("domain", "Any")))
        for item in raw
    )


def validate_parameter_bindings(
    declared: tuple[CircuitParameter, ...],
    bindings: Mapping[str, Any],
) -> tuple[dict[str, Any], ...]:
    """Validate concrete Host bindings before QPU submission."""
    if not declared:
        if bindings:
            return (
                _diag(
                    PARAM_BINDING_UNKNOWN,
                    f"unexpected parameter bindings: {sorted(bindings)}",
                ),
            )
        return ()

    diagnostics: list[dict[str, Any]] = []
    declared_names = {param.name for param in declared}
    for name in sorted(declared_names - set(bindings)):
        diagnostics.append(
            _diag(
                PARAM_BINDING_MISSING,
                f"missing binding for parameter `{name}`",
            )
        )
    for name in sorted(set(bindings) - declared_names):
        diagnostics.append(
            _diag(
                PARAM_BINDING_UNKNOWN,
                f"unknown parameter binding `{name}`",
            )
        )
    for param in declared:
        if param.name not in bindings:
            continue
        value = bindings[param.name]
        if param.domain == "Angle":
            if not isinstance(value, (int, float)):
                diagnostics.append(
                    _diag(
                        PARAM_BINDING_VALUE_ERROR,
                        f"parameter `{param.name}` requires a real scalar angle",
                    )
                )
                continue
            numeric = float(value)
            if not math.isfinite(numeric):
                diagnostics.append(
                    _diag(
                        PARAM_BINDING_VALUE_ERROR,
                        f"parameter `{param.name}` must be finite",
                    )
                )
        else:
            if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
                diagnostics.append(
                    _diag(
                        PARAM_BINDING_VALUE_ERROR,
                        f"parameter `{param.name}` requires a finite scalar",
                    )
                )
    return tuple(diagnostics)


def bindings_are_valid(
    declared: tuple[CircuitParameter, ...],
    bindings: Mapping[str, Any],
) -> bool:
    return not validate_parameter_bindings(declared, bindings)


def _parameter_decl_from_bind(stmt: StateBind) -> CircuitParameter | None:
    if stmt.ty is None or stmt.ty.name != "Param" or len(stmt.names) != 1:
        return None
    domain = stmt.ty.args[0].name if stmt.ty.args else "Any"
    binding_name = stmt.names[0]
    if (
        isinstance(stmt.expr, Call)
        and isinstance(stmt.expr.callee, Var)
        and stmt.expr.callee.name == "parameter"
        and len(stmt.expr.args) == 1
        and isinstance(stmt.expr.args[0], LitString)
    ):
        binding_name = stmt.expr.args[0].value
    return CircuitParameter(name=binding_name, domain=domain)


def _diag(code: str, message: str) -> dict[str, Any]:
    return {"code": code, "message": message}


__all__ = [
    "CircuitParameter",
    "PARAM_BINDING_MISSING",
    "PARAM_BINDING_UNKNOWN",
    "PARAM_BINDING_VALUE_ERROR",
    "bindings_are_valid",
    "extract_circuit_parameters",
    "extract_circuit_parameters_from_program",
    "validate_parameter_bindings",
]
