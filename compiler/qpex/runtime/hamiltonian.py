"""Compile Operator AST → dense Hamiltonian matrix (ℏ = 1)."""

from __future__ import annotations

from typing import Any

from ..ast_nodes import (
    OpBin,
    OpExpr,
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
    momentum_op,
    number_op,
    pauli1,
    position_op,
)


def op_n_qubits(
    op: OpExpr,
    env: dict[str, OpExpr],
    scalars: dict[str, float] | None = None,
) -> int:
    """Infer qubit count from max site index + 1 (0 if only bare Paulis / N)."""
    scalars = scalars or {}
    sites: list[int] = []
    uses_fock = False

    def walk(e: OpExpr) -> None:
        nonlocal uses_fock
        if isinstance(e, OpPauli):
            if e.site is not None:
                sites.append(e.site)
        elif isinstance(e, (OpNumber, OpQuadrature)):
            uses_fock = True
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
    if uses_fock and sites:
        raise ValueError("cannot mix Fock N/Q/P with site-indexed Pauli in one H (MVP)")
    if uses_fock:
        return 0  # signal Fock mode
    if sites:
        return max(sites) + 1
    return 1  # bare X/Y/Z


def compile_hamiltonian(
    op: OpExpr,
    *,
    env: dict[str, OpExpr],
    scalars: dict[str, float] | None = None,
    n_qubits: int | None = None,
    fock_dim: int | None = None,
) -> Matrix:
    scalars = scalars or {}
    nq = n_qubits if n_qubits is not None else op_n_qubits(op, env, scalars)
    if nq == 0:
        dim = fock_dim if fock_dim is not None else 4
        return _eval_fock(op, env, scalars, dim)
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
