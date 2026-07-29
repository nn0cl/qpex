"""Dependency-free finite-dimensional Lindblad evolution for the CPU lane."""

from __future__ import annotations

from .matrix import Matrix, mat_add, mat_dag, mat_mul, mat_scale
from .numeric_policy import PHYSICAL_TOLERANCE


TRACE_EPSILON = PHYSICAL_TOLERANCE


class NumericalTraceDefect(RuntimeError):
    """Raised when a density evolution leaves the declared trace tolerance."""


def trace_of(rho: Matrix) -> complex:
    return sum(rho[index][index] for index in range(len(rho)))


def lindblad_rhs(
    rho: Matrix,
    hamiltonian: Matrix,
    jumps: list[Matrix],
) -> Matrix:
    """Evaluate -i[H,rho] + sum(L rho L† - {L†L,rho}/2)."""
    _check_square_pair(rho, hamiltonian)
    derivative = mat_scale(
        mat_add(mat_mul(hamiltonian, rho), mat_scale(mat_mul(rho, hamiltonian), -1.0)),
        -1j,
    )
    for jump in jumps:
        _check_square_pair(rho, jump)
        jump_dag = mat_dag(jump)
        jump_rho_jump_dag = mat_mul(mat_mul(jump, rho), jump_dag)
        jump_dag_jump = mat_mul(jump_dag, jump)
        anticommutator = mat_add(
            mat_mul(jump_dag_jump, rho), mat_mul(rho, jump_dag_jump)
        )
        derivative = mat_add(
            derivative,
            mat_add(jump_rho_jump_dag, mat_scale(anticommutator, -0.5)),
        )
    return derivative


def evolve_lindblad(
    rho: Matrix,
    hamiltonian: Matrix,
    jumps: list[Matrix],
    *,
    total_time: float,
    dt: float,
    trace_epsilon: float = TRACE_EPSILON,
) -> Matrix:
    """Evolve a finite density matrix with deterministic fixed-step RK4."""
    _check_square_pair(rho, hamiltonian)
    if dt <= 0.0:
        raise ValueError("Lindblad dt must be positive")
    if total_time < 0.0:
        raise ValueError("Lindblad total_time must be non-negative")
    steps_float = total_time / dt
    steps = round(steps_float)
    if abs(steps_float - steps) > trace_epsilon:
        raise ValueError("Lindblad total_time must be an integer multiple of dt")
    _assert_trace(rho, trace_epsilon)

    current = _copy_matrix(rho)
    for _ in range(steps):
        k1 = lindblad_rhs(current, hamiltonian, jumps)
        k2 = lindblad_rhs(
            mat_add(current, mat_scale(k1, dt / 2.0)), hamiltonian, jumps
        )
        k3 = lindblad_rhs(
            mat_add(current, mat_scale(k2, dt / 2.0)), hamiltonian, jumps
        )
        k4 = lindblad_rhs(mat_add(current, mat_scale(k3, dt)), hamiltonian, jumps)
        weighted = mat_add(
            mat_add(k1, mat_scale(k2, 2.0)),
            mat_add(mat_scale(k3, 2.0), k4),
        )
        current = mat_add(current, mat_scale(weighted, dt / 6.0))
        _assert_trace(current, trace_epsilon)
    return current


def _assert_trace(rho: Matrix, epsilon: float) -> None:
    defect = abs(trace_of(rho) - 1.0)
    if defect > epsilon:
        raise NumericalTraceDefect(
            f"density trace defect {defect:.3e} exceeds tolerance {epsilon:.3e}"
        )


def _check_square_pair(left: Matrix, right: Matrix) -> None:
    if not left or any(len(row) != len(left) for row in left):
        raise ValueError("density matrices must be non-empty square matrices")
    if len(right) != len(left) or any(len(row) != len(left) for row in right):
        raise ValueError("Lindblad matrices must share one square dimension")


def _copy_matrix(matrix: Matrix) -> Matrix:
    return [[complex(value) for value in row] for row in matrix]
