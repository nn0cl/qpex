"""AT-TDD Phase 1 Red tests for the CPU/simulator Lindblad MVP."""

from __future__ import annotations

import cmath
import math
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.runtime.lindblad import (  # noqa: E402
    NumericalTraceDefect,
    evolve_lindblad,
    trace_of,
)


def test_fixed_step_rk4_amplitude_damping_preserves_trace_and_matches_reference() -> None:
    gamma = 0.7
    rho0 = [[0j, 0j], [0j, 1.0 + 0j]]
    hamiltonian = [[0j, 0j], [0j, 0j]]
    lowering = [[0j, math.sqrt(gamma)], [0j, 0j]]

    evolved = evolve_lindblad(
        rho0,
        hamiltonian,
        [lowering],
        total_time=0.2,
        dt=0.01,
    )

    assert abs(trace_of(evolved) - 1.0) < 1e-12
    assert abs(evolved[1][1].real - cmath.exp(-gamma * 0.2).real) < 1e-8


def test_fixed_step_rk4_is_deterministic() -> None:
    rho0 = [[1.0 + 0j, 0j], [0j, 0j]]
    hamiltonian = [[0j, 0j], [0j, 0j]]

    first = evolve_lindblad(rho0, hamiltonian, [], total_time=0.1, dt=0.01)
    second = evolve_lindblad(rho0, hamiltonian, [], total_time=0.1, dt=0.01)

    assert first == second


def test_trace_defect_is_a_hard_runtime_failure() -> None:
    rho0 = [[0.9 + 0j, 0j], [0j, 0j]]
    hamiltonian = [[0j, 0j], [0j, 0j]]

    try:
        evolve_lindblad(rho0, hamiltonian, [], total_time=0.1, dt=0.01)
    except NumericalTraceDefect:
        return
    raise AssertionError("invalid trace must raise NumericalTraceDefect")


if __name__ == "__main__":
    for test in (
        test_fixed_step_rk4_amplitude_damping_preserves_trace_and_matches_reference,
        test_fixed_step_rk4_is_deterministic,
        test_trace_defect_is_a_hard_runtime_failure,
    ):
        test()
    print("OK — Lindblad runtime Red tests")
