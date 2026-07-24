"""Provider-neutral observation planning for LISS-0044.

This module describes requested observations at the Host boundary. It does not
measure a Kernel state, create a provider Job, or expose simulator internals
without an explicit capability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping, Sequence


class ObservationValidationError(ValueError):
    """Hard validation failure for an observation request or plan."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class CheckpointIdentity:
    """Stable identity for one requested execution stage."""

    name: str
    stage: str

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.stage.strip():
            raise ObservationValidationError(
                "OBSERVATION_CHECKPOINT_ID_ERROR",
                "checkpoint name and stage must not be empty",
            )


@dataclass(frozen=True)
class SnapshotCapability:
    """Explicit permission for a simulator-only internal snapshot."""

    name: str
    lane: str

    def __post_init__(self) -> None:
        if self.lane != "simulator":
            raise ObservationValidationError(
                "OBSERVATION_SNAPSHOT_CAPABILITY_ERROR",
                "snapshot capabilities are simulator-only",
            )


@dataclass(frozen=True)
class ObservationRequest:
    """One explicit portable observation or simulator diagnostic request."""

    checkpoint: CheckpointIdentity
    observable: str
    projection: str
    target_lane: str
    source_formula: str
    capability: SnapshotCapability | None = None
    extra_shots: int = 0
    separate_job: bool = False

    def __post_init__(self) -> None:
        if not self.observable.strip() or not self.projection.strip():
            raise ObservationValidationError(
                "OBSERVATION_REQUEST_ERROR",
                "observable and projection must not be empty",
            )
        if self.target_lane not in {"simulator", "qpu"}:
            raise ObservationValidationError(
                "OBSERVATION_TARGET_LANE_ERROR",
                "target_lane must be simulator or qpu",
            )
        if not self.source_formula.strip():
            raise ObservationValidationError(
                "OBSERVATION_PROVENANCE_ERROR",
                "source_formula must not be empty",
            )
        if self.extra_shots < 0:
            raise ObservationValidationError(
                "OBSERVATION_RESOURCE_ERROR",
                "extra_shots must not be negative",
            )
        if self.is_snapshot:
            if self.target_lane == "qpu":
                raise ObservationValidationError(
                    "OBSERVATION_QPU_SNAPSHOT_UNSUPPORTED",
                    "QPU execution cannot expose an internal state snapshot",
                )
            if self.capability is None or self.capability.name != self.projection:
                raise ObservationValidationError(
                    "OBSERVATION_SNAPSHOT_CAPABILITY_REQUIRED",
                    "a matching simulator snapshot capability is required",
                )
        elif self.projection not in {"expectation", "probability", "counts"}:
            raise ObservationValidationError(
                "OBSERVATION_PROJECTION_ERROR",
                f"unsupported portable projection: {self.projection}",
            )

    @property
    def is_snapshot(self) -> bool:
        return self.projection in {"state_vector", "density_snapshot"}

    @property
    def portable(self) -> bool:
        return not self.is_snapshot


@dataclass(frozen=True)
class ObservationReport:
    """Completed observation result without exposing Kernel/provider objects."""

    request: ObservationRequest
    job_id: str
    values: Mapping[str, Any]
    provenance: Mapping[str, Any]
    portable: bool | None = None

    def __post_init__(self) -> None:
        if not self.job_id.strip():
            raise ObservationValidationError(
                "OBSERVATION_JOB_ID_ERROR",
                "job_id must not be empty",
            )
        object.__setattr__(self, "values", MappingProxyType(dict(self.values)))
        object.__setattr__(self, "provenance", MappingProxyType(dict(self.provenance)))
        if self.portable is None:
            object.__setattr__(self, "portable", self.request.portable)


@dataclass(frozen=True)
class ObservationPlan:
    """Explicit work requested by checkpoints; no work is inserted implicitly."""

    program_id: str
    requests: tuple[ObservationRequest, ...] = ()
    inserted_measurements: int = 0
    additional_jobs: int = 0
    additional_shots: int = 0


def plan_observations(
    program_id: str,
    requests: Sequence[ObservationRequest] = (),
) -> ObservationPlan:
    """Create an explicit plan and account for requested extra resources."""

    if not program_id.strip():
        raise ObservationValidationError(
            "OBSERVATION_PROGRAM_ID_ERROR",
            "program_id must not be empty",
        )
    normalized = tuple(requests)
    return ObservationPlan(
        program_id=program_id,
        requests=normalized,
        additional_jobs=sum(1 for request in normalized if request.separate_job),
        additional_shots=sum(request.extra_shots for request in normalized),
    )
