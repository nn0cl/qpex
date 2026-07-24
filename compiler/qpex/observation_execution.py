"""Local observation execution port and deterministic fake adapter."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Mapping, Protocol, runtime_checkable

from .host import JobResult
from .observation import ObservationPlan, ObservationReport


class ObservationExecutionValidationError(ValueError):
    """Hard, provider-neutral observation execution diagnostic."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class HostExecutionContext:
    """Opaque Host execution identity passed to an observation adapter."""

    program_id: str
    job_id: str
    seed: int
    target_lane: str = "simulator"

    def __post_init__(self) -> None:
        if not self.program_id.strip() or not self.job_id.strip():
            raise ObservationExecutionValidationError(
                "OBSERVATION_EXECUTION_CONTEXT_ERROR",
                "program_id and job_id must not be empty",
            )


@runtime_checkable
class ObservationValueSource(Protocol):
    """Port supplying explicitly fake or simulator-owned observation values."""

    def value(self, observable: str, projection: str) -> Any:
        ...


class FakeObservationValueSource:
    """Deterministic value source for contract tests and local planning."""

    def __init__(self, seed: int) -> None:
        self.seed = seed

    def value(self, observable: str, projection: str) -> Any:
        key = f"{self.seed}:{projection}:{observable}".encode("utf-8")
        digest = hashlib.sha256(key).digest()
        scalar = int.from_bytes(digest[:8], "big") / float(2**64)
        if projection == "counts":
            return {0: round(scalar * 1000), 1: round((1.0 - scalar) * 1000)}
        if projection == "probability":
            return {0: scalar, 1: 1.0 - scalar}
        return scalar


@runtime_checkable
class ObservationExecutionPort(Protocol):
    """Host port for executing an immutable observation plan."""

    def execute(self, plan: ObservationPlan, execution: HostExecutionContext) -> JobResult:
        ...


class LocalObservationAdapter:
    """Local adapter that turns fake values into provider-neutral reports."""

    _SUPPORTED_PROJECTIONS = frozenset({"expectation", "probability", "counts"})

    def __init__(self, value_source: ObservationValueSource) -> None:
        self._value_source = value_source

    def execute(
        self,
        plan: ObservationPlan,
        execution: HostExecutionContext,
    ) -> JobResult:
        reports: list[ObservationReport] = []
        for request in plan.requests:
            if request.projection not in self._SUPPORTED_PROJECTIONS:
                raise ObservationExecutionValidationError(
                    "OBSERVATION_PROJECTION_UNSUPPORTED",
                    self._unsupported_projection_message(request, execution),
                )
            reports.append(self._report_for(request, plan, execution))

        metadata = {
            "program_id": execution.program_id,
            "target_lane": execution.target_lane,
            "seed": execution.seed,
            "additional_shots": plan.additional_shots,
            "additional_jobs": plan.additional_jobs,
            "child_jobs": 0,
            "value_source": type(self._value_source).__name__,
        }
        return JobResult(
            status="succeeded",
            observations=tuple(reports),
            metadata=metadata,
        )

    def _report_for(self, request, plan, execution) -> ObservationReport:
        value = self._value_source.value(request.observable, request.projection)
        return ObservationReport(
            request=request,
            job_id=execution.job_id,
            values={request.projection: value},
            provenance={
                "program_id": execution.program_id,
                "checkpoint": request.checkpoint.name,
                "stage": request.checkpoint.stage,
                "target_lane": execution.target_lane,
                "seed": execution.seed,
                "value_source": type(self._value_source).__name__,
                "additional_shots": plan.additional_shots,
                "additional_jobs": plan.additional_jobs,
            },
        )

    @staticmethod
    def _unsupported_projection_message(request, execution) -> str:
        return (
            f"projection `{request.projection}` is unsupported for "
            f"target lane `{execution.target_lane}` at checkpoint "
            f"`{request.checkpoint.name}`"
        )
