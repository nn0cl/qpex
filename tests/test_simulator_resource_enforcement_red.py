"""AT-TDD Phase 1 Red tests for LISS-0063.

The enforcement boundary is intentionally absent until Phase 2 Green. These
tests define the provider-neutral decision contract without requiring a real
QPU, filesystem adapter, or third-party simulator.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.resource_profile import (  # noqa: E402
    ResourceProfile,
    SimulationResourceEstimate,
    SimulatorResourceBudget,
)


def _enforce():
    try:
        from compiler.staqex.resource_enforcement import (  # type: ignore[import-not-found]
            enforce_simulator_budget,
        )
    except ModuleNotFoundError as exc:
        raise AssertionError(
            "LISS-0063 Phase 2 resource enforcement boundary is not implemented"
        ) from exc
    return enforce_simulator_budget


def _estimate(bytes_used: int) -> SimulationResourceEstimate:
    return SimulationResourceEstimate(
        representation="StateVector",
        logical_qubits=3,
        estimated_bytes=bytes_used,
        workspace_factor=3,
    )


def test_warn_allows_local_simulation_and_returns_warning() -> None:
    enforce_simulator_budget = _enforce()
    profile = ResourceProfile(
        simulator=SimulatorResourceBudget(policy="Warn", memory_limit_bytes=100)
    )

    decision = enforce_simulator_budget(profile, _estimate(101), lane="simulator")

    assert decision.continue_execution is True
    assert any(
        diagnostic["code"] == "SIMULATOR_RESOURCE_WARNING"
        for diagnostic in decision.diagnostics
    )


def test_abort_stops_local_simulation_before_evaluation() -> None:
    enforce_simulator_budget = _enforce()
    profile = ResourceProfile(
        simulator=SimulatorResourceBudget(policy="Abort", memory_limit_bytes=100)
    )

    decision = enforce_simulator_budget(profile, _estimate(101), lane="simulator")

    assert decision.continue_execution is False
    assert any(
        diagnostic["code"] == "SIMULATOR_RESOURCE_ERROR"
        for diagnostic in decision.diagnostics
    )


def test_qasm_lane_aborts_even_when_manifest_policy_is_warn() -> None:
    enforce_simulator_budget = _enforce()
    profile = ResourceProfile(
        simulator=SimulatorResourceBudget(policy="Warn", memory_limit_bytes=100)
    )

    decision = enforce_simulator_budget(profile, _estimate(101), lane="qasm")

    assert decision.continue_execution is False
    assert any(
        diagnostic["code"] == "SIMULATOR_RESOURCE_ERROR"
        for diagnostic in decision.diagnostics
    )


def test_estimate_under_limit_continues_without_resource_diagnostic() -> None:
    enforce_simulator_budget = _enforce()
    profile = ResourceProfile(
        simulator=SimulatorResourceBudget(policy="Abort", memory_limit_bytes=100)
    )

    decision = enforce_simulator_budget(profile, _estimate(100), lane="simulator")

    assert decision.continue_execution is True
    assert decision.diagnostics == ()


if __name__ == "__main__":
    tests = [
        test_warn_allows_local_simulation_and_returns_warning,
        test_abort_stops_local_simulation_before_evaluation,
        test_qasm_lane_aborts_even_when_manifest_policy_is_warn,
        test_estimate_under_limit_continues_without_resource_diagnostic,
    ]
    for test in tests:
        test()
    print("OK - LISS-0063 Phase 1 Red tests")
