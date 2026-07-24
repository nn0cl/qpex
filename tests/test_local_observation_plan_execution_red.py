"""Acceptance tests for the LISS-0047 local observation execution contract."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _api():
    from compiler.qpex.observation_execution import (
        FakeObservationValueSource,
        HostExecutionContext,
        LocalObservationAdapter,
        ObservationExecutionValidationError,
    )

    return (
        FakeObservationValueSource,
        HostExecutionContext,
        LocalObservationAdapter,
        ObservationExecutionValidationError,
    )


def _plan():
    from compiler.qpex.observation import CheckpointIdentity, ObservationRequest, plan_observations

    request = ObservationRequest(
        checkpoint=CheckpointIdentity(name="energy", stage="final"),
        observable="energy(H)",
        projection="expectation",
        target_lane="simulator",
        source_formula="expectation(H)",
        extra_shots=100,
        separate_job=True,
    )
    return plan_observations("ising", (request,))


def test_port_accepts_opaque_host_context_and_returns_job_result():
    FakeSource, HostContext, Adapter, _ = _api()
    context = HostContext(program_id="ising", job_id="job-local-1", seed=7)
    result = Adapter(FakeSource(seed=7)).execute(_plan(), context)

    assert result.status == "succeeded"
    assert result.observations[0].job_id == "job-local-1"


def test_fake_value_source_is_reproducible_for_the_same_seed():
    FakeSource, _, _, _ = _api()

    first = FakeSource(seed=11).value("energy(H)", "expectation")
    second = FakeSource(seed=11).value("energy(H)", "expectation")

    assert first == second


def test_separate_job_records_cost_without_creating_child_jobs():
    FakeSource, HostContext, Adapter, _ = _api()
    result = Adapter(FakeSource(seed=3)).execute(
        _plan(), HostContext(program_id="ising", job_id="job-local-2", seed=3)
    )

    assert result.metadata["additional_shots"] == 100
    assert result.metadata["additional_jobs"] == 1
    assert result.metadata["child_jobs"] == 0


def test_unsupported_projection_is_a_hard_provider_neutral_diagnostic():
    FakeSource, HostContext, Adapter, ValidationError = _api()
    plan = _plan()
    request = plan.requests[0]
    unsupported = type(request)(
        checkpoint=request.checkpoint,
        observable=request.observable,
        projection="tomography",
        target_lane="simulator",
        source_formula=request.source_formula,
    )
    from compiler.qpex.observation import plan_observations

    try:
        Adapter(FakeSource(seed=1)).execute(
            plan_observations("ising", (unsupported,)),
            HostContext(program_id="ising", job_id="job-local-3", seed=1),
        )
    except ValidationError as error:
        assert error.code == "OBSERVATION_PROJECTION_UNSUPPORTED"
    else:
        raise AssertionError("unsupported projections must be rejected")


if __name__ == "__main__":
    tests = [
        test_port_accepts_opaque_host_context_and_returns_job_result,
        test_fake_value_source_is_reproducible_for_the_same_seed,
        test_separate_job_records_cost_without_creating_child_jobs,
        test_unsupported_projection_is_a_hard_provider_neutral_diagnostic,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
    print(f"Local observation execution: {len(tests) - failures} passed, {failures} failed")
    raise SystemExit(1 if failures else 0)
