"""AT-TDD Phase 1 Red tests for LISS-0065.

The tests define a provider-neutral Host orchestration contract.  The fake
ports are deliberately local and deterministic; no SDK, credential, network,
or live QPU is involved.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.qpu_submit import (  # noqa: E402
    ProviderJobId,
    ProviderJobState,
    QpuArtifact,
    QpuJobPort,
    QpuSubmitPort,
    QpuSubmitRequest,
)
from compiler.qpex.workflow import ExecutionPolicy, JobRequest, ParamBinding  # noqa: E402


class FakeSubmitPort:
    def __init__(self) -> None:
        self.requests: list[QpuSubmitRequest] = []

    def submit(self, request: QpuSubmitRequest) -> ProviderJobId:
        self.requests.append(request)
        return ProviderJobId("local-fake", f"job-{len(self.requests)}")


class FakeJobPort:
    def __init__(self) -> None:
        self.states = {"job-1": ProviderJobState.QUEUED}
        self.cancelled: list[ProviderJobId] = []
        self.result_payload: dict[str, object] = {
            "status": "succeeded",
            "measurements": ({"value": 0, "marginal": {0: 1.0}},),
        }

    def status(self, job_id: ProviderJobId) -> ProviderJobState:
        return self.states[job_id.opaque_id]

    def wait(self, job_id: ProviderJobId) -> ProviderJobState:
        self.states[job_id.opaque_id] = ProviderJobState.SUCCEEDED
        return self.states[job_id.opaque_id]

    def result(self, job_id: ProviderJobId) -> dict[str, object]:
        return dict(self.result_payload)

    def cancel(self, job_id: ProviderJobId) -> ProviderJobState:
        self.cancelled.append(job_id)
        self.states[job_id.opaque_id] = ProviderJobState.CANCELLED
        return self.states[job_id.opaque_id]


def _service():
    try:
        from compiler.qpex.qpu_orchestration import (  # type: ignore[import-not-found]
            QpuSubmitService,
            qpu_request_from_job_request,
        )
    except ModuleNotFoundError as exc:
        raise AssertionError(
            "LISS-0065 Phase 2 Host orchestration is not implemented"
        ) from exc
    return QpuSubmitService, qpu_request_from_job_request


def _artifact() -> QpuArtifact:
    return QpuArtifact(
        qasm="OPENQASM 3.0;",
        target_profile="local-fake",
        provenance={"source": "bell.qpex"},
        content_hash="sha256:artifact",
    )


def _workflow_request() -> JobRequest:
    return JobRequest(
        experiment="BellExperiment",
        bindings=(ParamBinding("theta", 0.5),),
        execution=ExecutionPolicy(target="local-fake", shots=100, seed=7),
    )


def test_workflow_request_maps_explicitly_to_qpu_submit_request() -> None:
    _, qpu_request_from_job_request = _service()

    request = qpu_request_from_job_request(
        _workflow_request(),
        _artifact(),
        idempotency_key="host-job-1",
    )

    assert isinstance(request, QpuSubmitRequest)
    assert request.artifact == _artifact()
    assert request.execution_settings == {
        "target": "local-fake",
        "shots": 100,
        "seed": 7,
        "experiment": "BellExperiment",
        "bindings": {"theta": 0.5},
    }
    assert request.idempotency_key == "host-job-1"
    assert request.attempt == 1


def test_service_exposes_fixed_lifecycle_through_opaque_provider_job_id() -> None:
    QpuSubmitService, _ = _service()
    submit = FakeSubmitPort()
    jobs = FakeJobPort()
    service = QpuSubmitService(submit_port=submit, job_port=jobs)

    handle = service.submit(
        QpuSubmitRequest(
            artifact=_artifact(),
            execution_settings={"shots": 100},
            idempotency_key="host-job-1",
        )
    )

    assert handle.job_id == ProviderJobId("local-fake", "job-1")
    assert handle.status() == ProviderJobState.QUEUED
    assert handle.wait().status == "succeeded"


@pytest.mark.parametrize("terminal_state", [ProviderJobState.FAILED, ProviderJobState.CANCELLED])
def test_non_success_job_result_does_not_expose_partial_measurements(
    terminal_state: ProviderJobState,
) -> None:
    QpuSubmitService, _ = _service()
    submit = FakeSubmitPort()
    jobs = FakeJobPort()
    jobs.states["job-1"] = terminal_state
    jobs.result_payload = {
        "status": terminal_state.value,
        "measurements": ({"value": 1, "marginal": {1: 1.0}},),
    }
    service = QpuSubmitService(submit_port=submit, job_port=jobs)
    handle = service.submit(
        QpuSubmitRequest(_artifact(), {"shots": 100}, "host-job-1")
    )

    result = handle.result()

    assert result.status == terminal_state.value
    assert result.measurements == ()
    assert any(diagnostic["code"] == "QPU_RESULT_UNAVAILABLE" for diagnostic in result.diagnostics)


def test_cancel_is_explicit_and_returns_cancelled_result_without_measurements() -> None:
    QpuSubmitService, _ = _service()
    submit = FakeSubmitPort()
    jobs = FakeJobPort()
    service = QpuSubmitService(submit_port=submit, job_port=jobs)
    handle = service.submit(
        QpuSubmitRequest(_artifact(), {"shots": 100}, "host-job-1")
    )

    result = handle.cancel()

    assert result.status == "cancelled"
    assert result.measurements == ()
    assert jobs.cancelled == [ProviderJobId("local-fake", "job-1")]


def test_retry_is_explicit_and_increments_attempt_without_changing_idempotency_key() -> None:
    QpuSubmitService, _ = _service()
    submit = FakeSubmitPort()
    jobs = FakeJobPort()
    service = QpuSubmitService(submit_port=submit, job_port=jobs)
    request = QpuSubmitRequest(_artifact(), {"shots": 100}, "host-job-1")
    service.submit(request)

    service.retry(request)

    assert len(submit.requests) == 2
    assert submit.requests[1].idempotency_key == "host-job-1"
    assert submit.requests[1].attempt == 2


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
