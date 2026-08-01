"""Dense exact QFT / IQFT / CQFT matrices for Joint apply (LISS-0228)."""

from __future__ import annotations

import cmath
import math

from dataclasses import dataclass

from .matrix import Matrix, mat_dag


@dataclass
class DenseMatrixOp:
    """Runtime dense Operator for outer products / materialized unitaries."""

    matrix: list[list[complex]]
    n_qubits: int


def qft_matrix(n_qubits: int) -> Matrix:
    """Exact QFT on ``n_qubits`` (MSB = index bit 0). Dim = 2**n."""
    if n_qubits < 1:
        raise ValueError("qft requires n_qubits >= 1")
    dim = 2**n_qubits
    omega = cmath.exp(2j * math.pi / dim)
    scale = 1.0 / math.sqrt(dim)
    return [
        [scale * (omega ** (j * k)) for k in range(dim)] for j in range(dim)
    ]


def iqft_matrix(n_qubits: int) -> Matrix:
    """Exact inverse QFT = adjoint of ``qft_matrix``."""
    return mat_dag(qft_matrix(n_qubits))


def cqft_matrix(n_target: int, *, inverse: bool = False) -> Matrix:
    """Filled-control QFT on ``n_target`` qubits (control is MSB wire).

    Acting space is 1 + n_target qubits. When control bit is 0, identity on
    targets; when 1, apply (i)QFT on the target subspace.
    """
    if n_target < 1:
        raise ValueError("cqft requires n_target >= 1")
    n_all = 1 + n_target
    dim = 2**n_all
    base = iqft_matrix(n_target) if inverse else qft_matrix(n_target)
    tdim = 2**n_target
    out: Matrix = [[0j] * dim for _ in range(dim)]
    # control=0 block: identity
    for i in range(tdim):
        out[i][i] = 1 + 0j
    # control=1 block: QFT on targets
    for j in range(tdim):
        for k in range(tdim):
            out[tdim + j][tdim + k] = base[j][k]
    return out
