"""AT-TDD Phase 1 Red tests for LISS-0066.

These tests define the provider-neutral Host projection boundary.  The fake
ports are deterministic and local; no provider SDK, credential, network, or
live QPU is involved.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import MeasurementEnvelope  # noqa: E402
from compiler.staqex.observation import (  # noqa: E402
    CheckpointIdentity,
    ObservationRequest,
    plan_observations,
)
from compiler.staqex.qpu_submit import (  # noqa: E402
    ProviderJobId,
    ProviderJobState,
    QpuArtifact,
    QpuJobPort,
    QpuSubmitPort,
    QpuSubmitRequest,
)


class FakeSubmitPort(QpuSubmitPort):
    def submit(self, request: QpuSubmitRequest) -> ProviderJobId:
        return ProviderJobId("local-fake", f"provider-{request.attempt}")


class FakeJobPort(QpuJobPort):
    def __init__(self) -> None:
        self.state = ProviderJobState.SUCCEEDED
        self.payload: dict[str, object] = {
            "measurements": (
                {"value": 0, "marginal": {0: 1.0}, "output": "0"},
            ),
            "observations": (
                {
                    "checkpoint": "magnetization",
                    "values": {"expectation": 0.2},
                    "provenance": {"shots": 100},
                },
                {
                    "checkpoint": "energy",
                    "values": {"expectation": -1.1},
                    "provenance": {"shots": 100},
                },
            ),
        }

    def status(self, job_id: ProviderJobId) -> ProviderJobState:
        return self.state

    def wait(self, job_id: ProviderJobId) -> ProviderJobState:
        return self.state

    def result(self, job_id: ProviderJobId) -> dict[str, object]:
        return dict(self.payload)

    def cancel(self, job_id: ProviderJobId) -> ProviderJobState:
        self.state = ProviderJobState.CANCELLED
        return self.state


def _projector():
    try:
        from compiler.staqex.qpu_observation import QpuObservationProjector
    except ModuleNotFoundError as exc:
        raise AssertionError(
            "LISS-0066 Phase 2 QPU observation projector is not implemented"
        ) from exc
    return QpuObservationProjector


def _artifact() -> QpuArtifact:
    return QpuArtifact(
        qasm="OPENQASM 3.0;",
        target_profile="local-fake",
        provenance={"source": "ising.qpex"},
        content_hash="sha256:artifact",
    )


def _plan():
    return plan_observations(
        "ising",
        (
            ObservationRequest(
                checkpoint=CheckpointIdentity("energy", "final"),
                observable="energy(H)",
                projection="expectation",
                target_lane="qpu",
                source_formula="expectation(H)",
            ),
            ObservationRequest(
                checkpoint=CheckpointIdentity("magnetization", "final"),
                observable="M",
                projection="expectation",
                target_lane="qpu",
                source_formula="expectation(M)",
            ),
        ),
    )


def _handle(jobs: FakeJobPort, *, attempt: int = 1):
    from compiler.staqex.qpu_orchestration import QpuSubmitService

    return QpuSubmitService(
        submit_port=FakeSubmitPort(), job_port=jobs
    ).submit(QpuSubmitRequest(_artifact(), {}, "logical-job-1", attempt=attempt))


def _project(jobs: FakeJobPort, *, attempt: int = 1):
    return _projector()().project(
        _handle(jobs, attempt=attempt),
        _plan(),
        logical_job_id="logical-job-1",
        attempt=attempt,
    )


def test_successful_qpu_observations_follow_source_plan_order() -> None:
    result = _project(FakeJobPort())

    assert result.status == "succeeded"
    assert [report.request.checkpoint.name for report in result.observations] == [
        "energy",
        "magnetization",
    ]


def test_incomplete_qpu_observations_fail_closed_without_values() -> None:
    jobs = FakeJobPort()
    jobs.payload["observations"] = (
        {
            "checkpoint": "energy",
            "values": {"expectation": -1.1},
            "provenance": {"shots": 100},
        },
    )

    result = _project(jobs)

    assert result.status == "failed"
    assert result.measurements == ()
    assert result.observations == ()
    assert any(
        diagnostic["code"] == "QPU_OBSERVATION_INCOMPLETE"
        for diagnostic in result.diagnostics
    )


@pytest.mark.parametrize("state", [ProviderJobState.FAILED, ProviderJobState.CANCELLED])
def test_failed_or_cancelled_qpu_job_exposes_no_partial_observations(
    state: ProviderJobState,
) -> None:
    jobs = FakeJobPort()
    jobs.state = state

    result = _project(jobs)

    assert result.status == state.value
    assert result.measurements == ()
    assert result.observations == ()
    assert any(diagnostic["code"] == "QPU_RESULT_UNAVAILABLE" for diagnostic in result.diagnostics)


def test_terminal_measurement_remains_separate_from_observation_reports() -> None:
    result = _project(FakeJobPort())

    assert result.measurements == (
        MeasurementEnvelope(value=0, marginal={0: 1.0}, vacuum=False, sink=None, output="0"),
    )
    assert result.observations


def test_attempt_metadata_preserves_logical_and_provider_job_identity() -> None:
    result = _project(FakeJobPort(), attempt=2)

    assert result.metadata["logical_job_id"] == "logical-job-1"
    assert result.metadata["attempt"] == 2
    assert result.metadata["provider_job_id"] == "provider-2"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
