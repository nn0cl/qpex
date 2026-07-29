"""Runtime value and terminal measurement helpers for finite mixed states."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..ast_nodes import Call, KetLit, ListExpr, LitFloat, LitInt, TupleExpr, Var
from .matrix import Matrix


@dataclass(frozen=True)
class DensityStateValue:
    matrix: Matrix
    domain: str
    operation: str


def density_from_call(expr: Call, *, domain: str) -> DensityStateValue:
    if len(expr.args) != 1 or not isinstance(expr.args[0], Call):
        raise ValueError("DensityState requires one Ensemble or RawMatrix input")
    source = expr.args[0]
    name = source.callee.name if isinstance(source.callee, Var) else ""
    if name == "RawMatrix":
        return DensityStateValue(
            matrix=matrix_from_list(source.args[0]),
            domain=domain,
            operation="RawMatrix",
        )
    if name == "Ensemble":
        return DensityStateValue(
            matrix=_matrix_from_ensemble(source.args[0]),
            domain=domain,
            operation="Ensemble",
        )
    raise ValueError("DensityState input must be Ensemble or RawMatrix")


def matrix_from_list(expr: Any) -> Matrix:
    if not isinstance(expr, ListExpr):
        raise ValueError("RawMatrix requires a matrix list")
    rows: Matrix = []
    for row in expr.items:
        if not isinstance(row, ListExpr):
            raise ValueError("RawMatrix requires nested row lists")
        rows.append([complex(_number(value)) for value in row.items])
    return rows


def _matrix_from_ensemble(expr: Any) -> Matrix:
    if not isinstance(expr, ListExpr):
        raise ValueError("Ensemble requires a list")
    dimension = 2
    matrix: Matrix = [[0j for _ in range(dimension)] for _ in range(dimension)]
    for item in expr.items:
        if not isinstance(item, TupleExpr) or len(item.items) != 2:
            raise ValueError("Ensemble entries must be weighted states")
        weight = _number(item.items[0])
        state = item.items[1]
        if not isinstance(state, KetLit) or state.label not in {"0", "1"}:
            raise ValueError("Ensemble MVP accepts |0> and |1>")
        index = int(state.label)
        matrix[index][index] += complex(weight)
    return matrix


def _number(expr: Any) -> float:
    if isinstance(expr, LitInt):
        return float(expr.value)
    if isinstance(expr, LitFloat):
        return float(expr.value)
    raise ValueError("mixed-state numeric input must be literal")
