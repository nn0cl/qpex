"""Compile Operator AST → dense Hamiltonian matrix (ℏ = 1)."""

from __future__ import annotations

from typing import Sequence

from ..ast_nodes import (
    OpBin,
    OpExpr,
    OpGridQuad,
    OpLit,
    OpNumber,
    OpPauli,
    OpPow,
    OpQuadrature,
    OpVar,
)
from .matrix import (
    Matrix,
    embed_pauli,
    eye,
    identity,
    mat_add,
    mat_mul,
    mat_scale,
    momentum_grid_op,
    momentum_op,
    number_op,
    pauli1,
    position_grid_op,
    position_op,
)


def op_n_qubits(
    op: OpExpr,
    env: dict[str, OpExpr],
    scalars: dict[str, float] | None = None,
) -> int:
    """Infer space size: >0 qubits, 0 Fock, -1 position grid."""
    mode = op_space(op, env, scalars)
    if mode == "fock":
        return 0
    if mode == "grid":
        return -1
    # qubit
    scalars = scalars or {}
    sites: list[int] = []

    def walk(e: OpExpr) -> None:
        if isinstance(e, OpPauli):
            if e.site is not None:
                sites.append(e.site)
        elif isinstance(e, OpBin):
            walk(e.lhs)
            walk(e.rhs)
        elif isinstance(e, OpPow):
            walk(e.base)
        elif isinstance(e, OpVar):
            if e.name in scalars:
                return
            if e.name not in env:
                raise ValueError(f"unbound Operator / scalar `{e.name}`")
            walk(env[e.name])

    walk(op)
    if sites:
        return max(sites) + 1
    return 1  # bare X/Y/Z


def op_space(
    op: OpExpr,
    env: dict[str, OpExpr],
    scalars: dict[str, float] | None = None,
) -> str:
    """Return `fock` | `grid` | `qubit` for an Operator polynomial."""
    scalars = scalars or {}
    uses_fock = False
    uses_grid = False
    sites: list[int] = []

    def walk(e: OpExpr) -> None:
        nonlocal uses_fock, uses_grid
        if isinstance(e, OpPauli):
            if e.site is not None:
                sites.append(e.site)
        elif isinstance(e, (OpNumber, OpQuadrature)):
            uses_fock = True
        elif isinstance(e, OpGridQuad):
            uses_grid = True
        elif isinstance(e, OpBin):
            walk(e.lhs)
            walk(e.rhs)
        elif isinstance(e, OpPow):
            walk(e.base)
        elif isinstance(e, OpVar):
            if e.name in scalars:
                return
            if e.name not in env:
                raise ValueError(f"unbound Operator / scalar `{e.name}`")
            walk(env[e.name])

    walk(op)
    if uses_fock and (uses_grid or sites):
        raise ValueError("cannot mix Fock N/Q/P with grid Xx/Px or site Pauli (MVP)")
    if uses_grid and (uses_fock or sites):
        raise ValueError("cannot mix grid Xx/Px with Fock or site-indexed Pauli (MVP)")
    if uses_fock:
        return "fock"
    if uses_grid:
        return "grid"
    return "qubit"


def compile_hamiltonian(
    op: OpExpr,
    *,
    env: dict[str, OpExpr],
    scalars: dict[str, float] | None = None,
    n_qubits: int | None = None,
    fock_dim: int | None = None,
    grid_xs: Sequence[float] | None = None,
) -> Matrix:
    scalars = scalars or {}
    if n_qubits is None:
        nq = op_n_qubits(op, env, scalars)
    else:
        nq = n_qubits
    if nq == 0:
        dim = fock_dim if fock_dim is not None else 4
        return _eval_fock(op, env, scalars, dim)
    if nq < 0:
        if grid_xs is None:
            raise ValueError("grid Hamiltonian requires grid_xs abscissae")
        return _eval_grid(op, env, scalars, list(grid_xs))
    return _eval_qubits(op, env, scalars, nq)


def _resolve_var(
    op: OpVar, env: dict[str, OpExpr], scalars: dict[str, float]
) -> OpExpr | float:
    if op.name in scalars:
        return scalars[op.name]
    if op.name not in env:
        raise ValueError(f"unbound Operator / scalar `{op.name}`")
    return env[op.name]


def _eval_qubits(
    op: OpExpr, env: dict[str, OpExpr], scalars: dict[str, float], n: int
) -> Matrix:
    if isinstance(op, OpLit):
        return mat_scale(eye(2**n), complex(op.value))
    if isinstance(op, OpPauli):
        site = 0 if op.site is None else op.site
        if n == 1 and op.site is None:
            return pauli1(op.kind)
        return embed_pauli(n, op.kind, site)
    if isinstance(op, OpNumber):
        raise ValueError("N is only valid in Fock Hamiltonians")
    if isinstance(op, OpQuadrature):
        raise ValueError("Q/P are only valid in Fock Hamiltonians")
    if isinstance(op, OpGridQuad):
        raise ValueError("Xx/Px are only valid in grid Hamiltonians")
    if isinstance(op, OpVar):
        resolved = _resolve_var(op, env, scalars)
        if isinstance(resolved, float):
            return mat_scale(eye(2**n), complex(resolved))
        return _eval_qubits(resolved, env, scalars, n)
    if isinstance(op, OpPow):
        base = _eval_qubits(op.base, env, scalars, n)
        acc = eye(2**n)
        for _ in range(op.exp):
            acc = mat_mul(acc, base)
        return acc
    if isinstance(op, OpBin):
        if op.op == "+":
            return mat_add(
                _eval_qubits(op.lhs, env, scalars, n),
                _eval_qubits(op.rhs, env, scalars, n),
            )
        if op.op == "-":
            return mat_add(
                _eval_qubits(op.lhs, env, scalars, n),
                mat_scale(_eval_qubits(op.rhs, env, scalars, n), -1),
            )
        if op.op == "*":
            if isinstance(op.lhs, OpLit):
                return mat_scale(
                    _eval_qubits(op.rhs, env, scalars, n), complex(op.lhs.value)
                )
            if isinstance(op.rhs, OpLit):
                return mat_scale(
                    _eval_qubits(op.lhs, env, scalars, n), complex(op.rhs.value)
                )
            if isinstance(op.lhs, OpVar) and op.lhs.name in scalars:
                return mat_scale(
                    _eval_qubits(op.rhs, env, scalars, n),
                    complex(scalars[op.lhs.name]),
                )
            if isinstance(op.rhs, OpVar) and op.rhs.name in scalars:
                return mat_scale(
                    _eval_qubits(op.lhs, env, scalars, n),
                    complex(scalars[op.rhs.name]),
                )
            return mat_mul(
                _eval_qubits(op.lhs, env, scalars, n),
                _eval_qubits(op.rhs, env, scalars, n),
            )
    raise ValueError(f"cannot compile operator node {type(op).__name__}")


def _eval_fock(
    op: OpExpr, env: dict[str, OpExpr], scalars: dict[str, float], dim: int
) -> Matrix:
    if isinstance(op, OpLit):
        return mat_scale(identity(dim), complex(op.value))
    if isinstance(op, OpNumber):
        return number_op(dim)
    if isinstance(op, OpQuadrature):
        if op.kind == "Q":
            return position_op(dim)
        if op.kind == "P":
            return momentum_op(dim)
        raise ValueError(f"unknown quadrature `{op.kind}`")
    if isinstance(op, OpPauli):
        raise ValueError("Pauli not valid in Fock H (use N / Q / P)")
    if isinstance(op, OpGridQuad):
        raise ValueError("Xx/Px not valid in Fock H (use grid evolve)")
    if isinstance(op, OpVar):
        resolved = _resolve_var(op, env, scalars)
        if isinstance(resolved, float):
            return mat_scale(identity(dim), complex(resolved))
        return _eval_fock(resolved, env, scalars, dim)
    if isinstance(op, OpPow):
        base = _eval_fock(op.base, env, scalars, dim)
        acc = identity(dim)
        for _ in range(op.exp):
            acc = mat_mul(acc, base)
        return acc
    if isinstance(op, OpBin):
        if op.op == "+":
            return mat_add(
                _eval_fock(op.lhs, env, scalars, dim),
                _eval_fock(op.rhs, env, scalars, dim),
            )
        if op.op == "-":
            return mat_add(
                _eval_fock(op.lhs, env, scalars, dim),
                mat_scale(_eval_fock(op.rhs, env, scalars, dim), -1),
            )
        if op.op == "*":
            if isinstance(op.lhs, OpLit):
                return mat_scale(
                    _eval_fock(op.rhs, env, scalars, dim), complex(op.lhs.value)
                )
            if isinstance(op.rhs, OpLit):
                return mat_scale(
                    _eval_fock(op.lhs, env, scalars, dim), complex(op.rhs.value)
                )
            if isinstance(op.lhs, OpVar) and op.lhs.name in scalars:
                return mat_scale(
                    _eval_fock(op.rhs, env, scalars, dim),
                    complex(scalars[op.lhs.name]),
                )
            if isinstance(op.rhs, OpVar) and op.rhs.name in scalars:
                return mat_scale(
                    _eval_fock(op.lhs, env, scalars, dim),
                    complex(scalars[op.rhs.name]),
                )
            return mat_mul(
                _eval_fock(op.lhs, env, scalars, dim),
                _eval_fock(op.rhs, env, scalars, dim),
            )
    raise ValueError(f"cannot compile Fock operator {type(op).__name__}")


def _eval_grid(
    op: OpExpr,
    env: dict[str, OpExpr],
    scalars: dict[str, float],
    xs: list[float],
) -> Matrix:
    dim = len(xs)
    if isinstance(op, OpLit):
        return mat_scale(identity(dim), complex(op.value))
    if isinstance(op, OpGridQuad):
        if op.kind == "Xx":
            return position_grid_op(xs)
        if op.kind == "Px":
            return momentum_grid_op(xs)
        raise ValueError(f"unknown grid quadrature `{op.kind}`")
    if isinstance(op, (OpNumber, OpQuadrature)):
        raise ValueError("Fock N/Q/P not valid in grid H (use Xx / Px)")
    if isinstance(op, OpPauli):
        raise ValueError("Pauli not valid in grid H")
    if isinstance(op, OpVar):
        resolved = _resolve_var(op, env, scalars)
        if isinstance(resolved, float):
            return mat_scale(identity(dim), complex(resolved))
        return _eval_grid(resolved, env, scalars, xs)
    if isinstance(op, OpPow):
        base = _eval_grid(op.base, env, scalars, xs)
        acc = identity(dim)
        for _ in range(op.exp):
            acc = mat_mul(acc, base)
        return acc
    if isinstance(op, OpBin):
        if op.op == "+":
            return mat_add(
                _eval_grid(op.lhs, env, scalars, xs),
                _eval_grid(op.rhs, env, scalars, xs),
            )
        if op.op == "-":
            return mat_add(
                _eval_grid(op.lhs, env, scalars, xs),
                mat_scale(_eval_grid(op.rhs, env, scalars, xs), -1),
            )
        if op.op == "*":
            if isinstance(op.lhs, OpLit):
                return mat_scale(
                    _eval_grid(op.rhs, env, scalars, xs), complex(op.lhs.value)
                )
            if isinstance(op.rhs, OpLit):
                return mat_scale(
                    _eval_grid(op.lhs, env, scalars, xs), complex(op.rhs.value)
                )
            if isinstance(op.lhs, OpVar) and op.lhs.name in scalars:
                return mat_scale(
                    _eval_grid(op.rhs, env, scalars, xs),
                    complex(scalars[op.lhs.name]),
                )
            if isinstance(op.rhs, OpVar) and op.rhs.name in scalars:
                return mat_scale(
                    _eval_grid(op.lhs, env, scalars, xs),
                    complex(scalars[op.rhs.name]),
                )
            return mat_mul(
                _eval_grid(op.lhs, env, scalars, xs),
                _eval_grid(op.rhs, env, scalars, xs),
            )
    raise ValueError(f"cannot compile grid operator {type(op).__name__}")
