"""AT-TDD Phase 1 Red: LISS-0094 integrated simulator-port contract.

One suite covers capability/request/result/rejection VOs, FakeSimulatorPort,
deterministic seed propagation, observation-plan refs, budget pre-allocation
rejection, SIM0_EXACT/SIM1_MIXED fixtures, simulation-labelled results, and
IR/engine isolation. Concrete engines and provider SDKs are absent.
"""

from __future__ import annotations

from pathlib import Path
import sys

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.simulator_port import (
        FakeSimulatorPort,
        ObservationPlanRef,
        SimulationBudget,
        SimulationRequest,
        SimulationResult,
        SimulatorCapabilityProfile,
        ValidationReport,
    )

    return locals()


def _budget(
    api,
    *,
    max_qubits: int = 4,
    max_memory_bytes: int = 64 * 1024 * 1024,
    max_shots: int = 100,
    max_time_ms: int = 1000,
    tolerance: str | None = "1e-12",
):
    return api["SimulationBudget"](
        max_qubits=max_qubits,
        max_memory_bytes=max_memory_bytes,
        max_shots=max_shots,
        max_time_ms=max_time_ms,
        tolerance=tolerance,
    )


def _observation(api, *, mode: str = "terminal-measure"):
    return api["ObservationPlanRef"](plan_id="obs.default", mode=mode)


def _request(
    api,
    *,
    profile_id: str = "SIM0_EXACT",
    plan_id: str = "plan.verified.bell",
    qubits: int = 2,
    operations: tuple[str, ...] = ("h", "cx"),
    carrier_kind: str = "qubit",
    needs_dynamic: bool = False,
    seed: str = "seed-42",
    budget=None,
    observation=None,
    provenance: str = "verified-semantic-projection",
):
    return api["SimulationRequest"](
        plan_id=plan_id,
        profile_id=profile_id,
        qubit_count=qubits,
        operations=operations,
        carrier_kind=carrier_kind,
        needs_dynamic=needs_dynamic,
        seed=seed,
        budget=budget if budget is not None else _budget(api),
        observation=observation if observation is not None else _observation(api),
        provenance_token=provenance,
    )


def _codes(report) -> set[str]:
    return set(report.exceeded_dimensions) | set(report.missing_dimensions)


def test_versioned_capability_profile_distinguishes_dimensions() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    profile = port.capabilities("SIM0_EXACT")

    assert isinstance(profile, api["SimulatorCapabilityProfile"])
    assert profile.schema_version == "1"
    assert profile.profile_id == "SIM0_EXACT"
    assert profile.oracle_class == "exact"
    assert profile.max_qubits >= 2
    assert profile.supported_operations
    assert profile.supported_carriers
    assert profile.observation_modes
    assert profile.dynamic_supported is False


def test_fake_port_loads_sim0_and_sim1_shared_schema() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()

    sim0 = port.capabilities("SIM0_EXACT")
    sim1 = port.capabilities("SIM1_MIXED")

    assert sim0.schema_version == sim1.schema_version == "1"
    assert {sim0.profile_id, sim1.profile_id} == {"SIM0_EXACT", "SIM1_MIXED"}
    assert sim0.oracle_class == "exact"
    assert sim1.oracle_class == "mixed"
    assert sim1.max_qubits <= sim0.max_qubits


def test_validate_accepts_bounded_sim0_request() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    report = port.validate(_request(api))

    assert isinstance(report, api["ValidationReport"])
    assert report.status == "accepted"
    assert report.exceeded_dimensions == ()
    assert report.missing_dimensions == ()
    assert report.selected_alternative is None


def test_over_budget_rejected_before_allocation() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    profile = port.capabilities("SIM0_EXACT")
    request = _request(
        api,
        qubits=profile.max_qubits + 1,
        budget=_budget(api, max_qubits=profile.max_qubits + 1),
    )
    report = port.validate(request)

    assert report.status == "rejected"
    assert "max_qubits" in report.exceeded_dimensions
    assert report.selected_alternative is None

    try:
        port.execute(request)
    except ValueError as error:
        assert "max_qubits" in str(error) or "rejected" in str(error).lower()
        return
    raise AssertionError("over-budget execute must fail closed before allocation")


def test_unsupported_capability_rejected_without_fallback() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()

    carrier = port.validate(_request(api, carrier_kind="qudit"))
    assert carrier.status == "rejected"
    assert "carrier_kind" in carrier.exceeded_dimensions
    assert carrier.selected_alternative is None

    dynamic = port.validate(_request(api, needs_dynamic=True))
    assert dynamic.status == "rejected"
    assert "dynamic_supported" in dynamic.exceeded_dimensions
    assert dynamic.selected_alternative is None

    observation = port.validate(
        _request(api, observation=_observation(api, mode="provider-tomography"))
    )
    assert observation.status == "rejected"
    assert "observation_mode" in observation.exceeded_dimensions
    assert observation.selected_alternative is None


def test_execute_propagates_seed_and_labels_simulation() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    result = port.execute(_request(api, seed="seed-99"))

    assert isinstance(result, api["SimulationResult"])
    assert result.execution_kind == "simulation"
    assert result.profile_id == "SIM0_EXACT"
    assert result.seed_used == "seed-99"
    assert result.plan_id == "plan.verified.bell"
    assert result.payload is not None


def test_observation_plan_ref_required_on_exact_oracle_result() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    result = port.execute(_request(api))

    assert result.observation_plan_id == "obs.default"
    assert result.observation_mode == "terminal-measure"
    assert "probabilities" in result.payload or "expectations" in result.payload


def test_sim1_fixture_rejects_modes_beyond_flags() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    profile = port.capabilities("SIM1_MIXED")

    assert profile.oracle_class == "mixed"
    request = _request(
        api,
        profile_id="SIM1_MIXED",
        qubits=min(2, profile.max_qubits),
        needs_dynamic=True,
    )
    report = port.validate(request)
    assert report.status == "rejected"
    assert "dynamic_supported" in report.exceeded_dimensions
    assert report.selected_alternative is None


def test_missing_budget_fields_reject_explicitly() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    incomplete = api["SimulationBudget"](
        max_qubits=2,
        max_memory_bytes=None,
        max_shots=10,
        max_time_ms=None,
        tolerance=None,
    )
    report = port.validate(_request(api, budget=incomplete))

    assert report.status == "rejected"
    assert "max_memory_bytes" in report.missing_dimensions
    assert "max_time_ms" in report.missing_dimensions
    assert report.selected_alternative is None


def test_module_does_not_import_ir_engines_or_providers() -> None:
    api = _load_api()
    import compiler.staqex.simulator_port as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    forbidden = (
        "physics_ir",
        "quantum_semantic_ir",
        "qiskit",
        "cirq",
        "pennylane",
        "provider",
    )
    for token in forbidden:
        assert token not in text, token
    assert api["FakeSimulatorPort"] is not None


def test_fake_port_unknown_profile_fails_closed() -> None:
    api = _load_api()
    port = api["FakeSimulatorPort"]()
    try:
        port.capabilities("ENGINE_LIVE_UNKNOWN")
    except KeyError as error:
        assert "ENGINE_LIVE_UNKNOWN" in str(error)
        return
    raise AssertionError("unknown profile must fail closed without fallback")


if __name__ == "__main__":
    tests = tuple(
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
    print(
        f"LISS-0094 integrated Red: {len(tests) - failures} passed, {failures} failed"
    )
    raise SystemExit(1 if failures else 0)
