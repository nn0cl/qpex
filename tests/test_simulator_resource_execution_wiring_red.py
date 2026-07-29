"""AT-TDD Phase 1 Red tests for LISS-0064.

These tests define the missing execution wiring around the provider-neutral
LISS-0063 decision boundary.  They intentionally use the existing run and
QASM entry points with an explicit immutable profile and estimate; no manifest
file, provider SDK, or real QPU is involved.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.codegen_qasm import OpenQASM3Generator  # noqa: E402
from compiler.staqex.pipeline import compile_source  # noqa: E402
from compiler.staqex.resource_profile import (  # noqa: E402
    ResourceProfile,
    SimulationResourceEstimate,
    SimulatorResourceBudget,
)
from compiler.staqex.run import run_source  # noqa: E402


_SOURCE = """
package t
pub fn main() -> Unit {
    state q = |0>
    measure q
}
"""


def _profile(policy: str) -> ResourceProfile:
    return ResourceProfile(
        simulator=SimulatorResourceBudget(policy=policy, memory_limit_bytes=100)
    )


def _over_limit_estimate() -> SimulationResourceEstimate:
    return SimulationResourceEstimate(
        representation="StateVector",
        logical_qubits=3,
        estimated_bytes=101,
        workspace_factor=3,
    )


def test_local_run_warn_continues_and_preserves_resource_warning() -> None:
    result = run_source(
        _SOURCE,
        stdout=io.StringIO(),
        resource_profile=_profile("Warn"),
        resource_estimate=_over_limit_estimate(),
    )

    assert result.compile_ok, result.diagnostics
    assert any(
        diagnostic.get("code") == "SIMULATOR_RESOURCE_WARNING"
        for diagnostic in result.diagnostics
    )
    assert result.eval.measure is not None


def test_local_run_abort_stops_before_evaluator(monkeypatch: pytest.MonkeyPatch) -> None:
    def evaluator_must_not_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("resource rejection must precede evaluator execution")

    monkeypatch.setattr("compiler.staqex.run.Evaluator.run_unit", evaluator_must_not_run)

    result = run_source(
        _SOURCE,
        stdout=io.StringIO(),
        resource_profile=_profile("Abort"),
        resource_estimate=_over_limit_estimate(),
    )

    assert result.compile_ok is False
    assert any(
        diagnostic.get("code") == "SIMULATOR_RESOURCE_ERROR"
        for diagnostic in result.diagnostics
    )


def test_qasm_emission_rejects_before_lowering_even_when_policy_is_warn(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    compiled = compile_source(_SOURCE)
    assert compiled.ok and compiled.unit is not None, compiled.diagnostics

    def lowering_must_not_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("resource rejection must precede QASM lowering")

    monkeypatch.setattr(
        "compiler.staqex.backend.qasm.emitter.lower_unit_to_circuit",
        lowering_must_not_run,
    )

    emitted = OpenQASM3Generator(route=False).generate_detailed(
        compiled.unit,
        resource_profile=_profile("Warn"),
        resource_estimate=_over_limit_estimate(),
    )

    assert emitted.ok is False
    assert emitted.circuit is not None
    assert emitted.circuit.reject_code == "SIMULATOR_RESOURCE_ERROR"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
