"""Host-side projection of provider-neutral QPU observations."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .host import JobResult
from .observation import ObservationPlan, ObservationReport
from .qpu_orchestration import QpuJobHandle
from .qpu_submit import ProviderJobState

QPU_OBSERVATION_INCOMPLETE = "QPU_OBSERVATION_INCOMPLETE"


class QpuObservationProjector:
    """Project one completed QPU payload into the Host observation contract."""

    def project(
        self,
        handle: QpuJobHandle,
        plan: ObservationPlan,
        *,
        logical_job_id: str,
        attempt: int,
    ) -> JobResult:
        metadata = _execution_metadata(handle, plan, logical_job_id, attempt)
        result = handle.result()
        if handle.status() is not ProviderJobState.SUCCEEDED:
            return _with_metadata(result, metadata)

        payload = handle.result_payload()
        entries = _observation_entries(payload.get("observations", ()))
        reports = _reports_in_plan_order(plan, entries, logical_job_id)
        if reports is None:
            return _incomplete_result(metadata)

        return _successful_projection(result, metadata, reports)


def _execution_metadata(
    handle: QpuJobHandle,
    plan: ObservationPlan,
    logical_job_id: str,
    attempt: int,
) -> dict[str, Any]:
    return {
        "logical_job_id": logical_job_id,
        "provider_job_id": handle.job_id.opaque_id,
        "attempt": attempt,
        "additional_jobs": plan.additional_jobs,
        "additional_shots": plan.additional_shots,
    }


def _incomplete_result(metadata: dict[str, Any]) -> JobResult:
    return JobResult(
        status="failed",
        diagnostics=(
            {
                "code": QPU_OBSERVATION_INCOMPLETE,
                "message": "QPU payload does not match the observation plan",
            },
        ),
        metadata=metadata,
    )


def _successful_projection(
    result: JobResult,
    metadata: dict[str, Any],
    reports: list[ObservationReport],
) -> JobResult:
    return JobResult(
        status="succeeded",
        measurements=result.measurements,
        diagnostics=result.diagnostics,
        metadata={**result.metadata, **metadata},
        observations=tuple(reports),
    )


def _with_metadata(result: JobResult, metadata: dict[str, Any]) -> JobResult:
    return JobResult(
        status=result.status,
        measurements=(),
        diagnostics=result.diagnostics,
        metadata={**result.metadata, **metadata},
        observations=(),
    )


def _observation_entries(values: object) -> dict[str, Mapping[str, Any]] | None:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)):
        return None
    entries: dict[str, Mapping[str, Any]] = {}
    for value in values:
        if not isinstance(value, Mapping):
            return None
        checkpoint = value.get("checkpoint")
        if not isinstance(checkpoint, str) or checkpoint in entries:
            return None
        entries[checkpoint] = value
    return entries


def _reports_in_plan_order(
    plan: ObservationPlan,
    entries: dict[str, Mapping[str, Any]] | None,
    logical_job_id: str,
) -> list[ObservationReport] | None:
    if entries is None:
        return None
    expected = [request.checkpoint.name for request in plan.requests]
    if set(entries) != set(expected) or len(expected) != len(entries):
        return None

    reports: list[ObservationReport] = []
    for request in plan.requests:
        entry = entries[request.checkpoint.name]
        values = entry.get("values")
        provenance = entry.get("provenance")
        if not isinstance(values, Mapping) or not isinstance(provenance, Mapping):
            return None
        reports.append(
            ObservationReport(
                request=request,
                job_id=logical_job_id,
                values=values,
                provenance=provenance,
                portable=True,
            )
        )
    return reports


__all__ = ["QPU_OBSERVATION_INCOMPLETE", "QpuObservationProjector"]
