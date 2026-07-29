"""Host-side orchestration for provider-neutral QPU submission.

This module coordinates the existing submit and job ports.  It deliberately
does not contain provider SDK, credential, transport, or retry policy logic.
"""

from __future__ import annotations

from dataclasses import replace
from collections.abc import Mapping, Sequence
from typing import Any

from .host import JobResult, MeasurementEnvelope
from .qpu_submit import (
    ProviderJobId,
    ProviderJobState,
    QpuArtifact,
    QpuJobPort,
    QpuSubmitPort,
    QpuSubmitRequest,
)
from .workflow import JobRequest

QPU_RESULT_UNAVAILABLE = "QPU_RESULT_UNAVAILABLE"


def qpu_request_from_job_request(
    job_request: JobRequest,
    artifact: QpuArtifact,
    *,
    idempotency_key: str,
) -> QpuSubmitRequest:
    """Map a workflow request into the provider-neutral QPU DTO."""

    settings: dict[str, Any] = {
        "target": job_request.execution.target,
        "shots": job_request.execution.shots,
        "seed": job_request.execution.seed,
        "experiment": job_request.experiment,
        "bindings": {
            binding.parameter: binding.value for binding in job_request.bindings
        },
    }
    return QpuSubmitRequest(
        artifact=artifact,
        execution_settings=settings,
        idempotency_key=idempotency_key,
    )


class QpuJobHandle:
    """Host-facing handle for one opaque provider job."""

    def __init__(self, job_id: ProviderJobId, job_port: QpuJobPort) -> None:
        self.job_id = job_id
        self._job_port = job_port

    def status(self) -> ProviderJobState:
        return self._job_port.status(self.job_id)

    def wait(self) -> JobResult:
        self._job_port.wait(self.job_id)
        return self.result()

    def result(self) -> JobResult:
        state = self.status()
        if state is not ProviderJobState.SUCCEEDED:
            return _unavailable_result(state)
        return _successful_result(self.result_payload())

    def result_payload(self) -> Mapping[str, Any]:
        """Return the provider-neutral payload for a succeeded QPU job."""

        if self.status() is not ProviderJobState.SUCCEEDED:
            return {}
        return self._job_port.result(self.job_id)

    def cancel(self) -> JobResult:
        self._job_port.cancel(self.job_id)
        return self.result()


class QpuSubmitService:
    """Submit and explicitly retry QPU jobs through Host ports."""

    def __init__(self, *, submit_port: QpuSubmitPort, job_port: QpuJobPort) -> None:
        self._submit_port = submit_port
        self._job_port = job_port

    def submit(self, request: QpuSubmitRequest) -> QpuJobHandle:
        if request.attempt < 1:
            raise ValueError("QPU submit attempt must be one-based")
        return QpuJobHandle(
            self._submit_port.submit(request),
            self._job_port,
        )

    def retry(self, request: QpuSubmitRequest) -> QpuJobHandle:
        retried = replace(request, attempt=request.attempt + 1)
        return self.submit(retried)


def _unavailable_result(state: ProviderJobState) -> JobResult:
    return JobResult(
        status=state.value,
        diagnostics=(
            {
                "code": QPU_RESULT_UNAVAILABLE,
                "message": f"result unavailable for {state.value} job",
            },
        ),
    )


def _successful_result(payload: Mapping[str, Any]) -> JobResult:
    return JobResult(
        status=ProviderJobState.SUCCEEDED.value,
        measurements=_measurements(payload.get("measurements", ())),
        metadata=dict(payload.get("metadata", {})),
        diagnostics=tuple(payload.get("diagnostics", ())),
    )


def _measurements(values: object) -> tuple[MeasurementEnvelope, ...]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        return ()
    result: list[MeasurementEnvelope] = []
    for value in values:
        if not isinstance(value, Mapping):
            continue
        result.append(
            MeasurementEnvelope(
                value=value.get("value"),
                marginal=dict(value.get("marginal", {})),
                vacuum=bool(value.get("vacuum", False)),
                sink=value.get("sink"),
                output=str(value.get("output", "")),
            )
        )
    return tuple(result)


__all__ = [
    "QpuJobHandle",
    "QpuSubmitService",
    "qpu_request_from_job_request",
]
