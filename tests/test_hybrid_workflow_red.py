"""AT-TDD Phase 2 Red: provider-neutral hybrid workflow DTOs."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import Job, JobResult, MeasurementEnvelope  # noqa: E402
from compiler.staqex.workflow import (  # noqa: E402
    ExecutionPolicy,
    ParamBinding,
    WorkflowPlan,
    WorkflowReport,
    WorkflowValidationError,
)


def _completed_job() -> Job:
    return Job(
        "fake-1",
        JobResult(
            status="succeeded",
            measurements=(
                MeasurementEnvelope(
                    value=0.25,
                    marginal={0: 0.75, 1: 0.25},
                    vacuum=False,
                    sink=None,
                    output="",
                ),
            ),
            metadata={"observable": "energy"},
        ),
    )


def test_workflow_creates_provider_neutral_job_request() -> None:
    plan = WorkflowPlan(
        experiment="GroundState",
        parameters=("theta",),
        observables=("energy",),
    )

    request = plan.request(
        bindings=(ParamBinding("theta", 0.5),),
        execution=ExecutionPolicy(shots=1000, seed=7),
    )

    assert request.experiment == "GroundState"
    assert request.bindings == (ParamBinding("theta", 0.5),)
    assert request.execution.shots == 1000


def test_workflow_waits_for_job_result_before_projection() -> None:
    plan = WorkflowPlan(
        experiment="GroundState",
        parameters=("theta",),
        observables=("energy",),
    )
    seen: list[str] = []

    def submit(request):
        seen.append(request.experiment)
        return _completed_job()

    projection = plan.run_once(
        submit,
        bindings=(ParamBinding("theta", 0.5),),
        execution=ExecutionPolicy(shots=1000),
        observable="energy",
    )

    assert seen == ["GroundState"]
    assert projection.observable == "energy"
    assert projection.value == 0.25


def test_workflow_rejects_undeclared_binding_and_observable() -> None:
    plan = WorkflowPlan(
        experiment="GroundState",
        parameters=("theta",),
        observables=("energy",),
    )

    try:
        plan.request(
            bindings=(ParamBinding("phi", 0.5),),
            execution=ExecutionPolicy(),
        )
    except WorkflowValidationError:
        pass
    else:
        raise AssertionError("undeclared parameter must be rejected")

    try:
        plan.run_once(
            lambda request: _completed_job(),
            bindings=(ParamBinding("theta", 0.5),),
            execution=ExecutionPolicy(),
            observable="variance",
        )
    except WorkflowValidationError:
        pass
    else:
        raise AssertionError("undeclared observable must be rejected")


def test_workflow_dtos_are_immutable() -> None:
    binding = ParamBinding("theta", 0.5)
    try:
        binding.value = 0.7
    except AttributeError:
        pass
    else:
        raise AssertionError("ParamBinding must be immutable")


def test_workflow_iterates_after_completed_results_and_stops_at_until() -> None:
    plan = WorkflowPlan(
        experiment="GroundState",
        parameters=("theta",),
        observables=("energy",),
    )
    submitted: list[float] = []

    def submit(request):
        theta = request.bindings[0].value
        submitted.append(theta)
        return Job(
            f"fake-{len(submitted)}",
            JobResult(
                status="succeeded",
                measurements=(
                    MeasurementEnvelope(
                        value=1.0 - theta,
                        marginal={},
                        vacuum=False,
                        sink=None,
                        output="",
                    ),
                ),
            ),
        )

    report = plan.run_iterative(
        submit,
        initial=(ParamBinding("theta", 0.0),),
        execution=ExecutionPolicy(shots=10),
        observable="energy",
        update=lambda bindings, projection: (
            ParamBinding("theta", bindings[0].value + 0.5),
        ),
        until=lambda projection, iteration: projection.value <= 0.5,
        max_iterations=4,
    )

    assert isinstance(report, WorkflowReport)
    assert report.status == "succeeded"
    assert report.iterations == 2
    assert submitted == [0.0, 0.5]
    assert report.final_bindings == (ParamBinding("theta", 0.5),)
    assert len(report.projections) == 2


if __name__ == "__main__":
    for test in (
        test_workflow_creates_provider_neutral_job_request,
        test_workflow_waits_for_job_result_before_projection,
        test_workflow_rejects_undeclared_binding_and_observable,
        test_workflow_dtos_are_immutable,
        test_workflow_iterates_after_completed_results_and_stops_at_until,
    ):
        test()
    print("OK — hybrid workflow tests")
