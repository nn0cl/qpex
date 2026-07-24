"""Provider-neutral host Job boundary (LISS-0022, ADR-0065).

This module deliberately converts Kernel results into host DTOs.  Callers do
not receive the evaluator's Joint, AST, or provider-specific objects.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TextIO
from uuid import uuid4

from .pipeline import CompileResult, compile_path, compile_source
from .runtime.evaluator import EvalResult, Evaluator, KernelError
from .observation import ObservationReport


@dataclass(frozen=True)
class MeasurementEnvelope:
    """Opaque host representation of one terminal measurement."""

    value: Any | None
    marginal: dict[Any, float]
    vacuum: bool
    sink: str | None
    output: str


@dataclass(frozen=True)
class JobResult:
    """Provider-neutral result returned after a Job reaches a terminal state."""

    status: str
    measurements: tuple[MeasurementEnvelope, ...] = ()
    diagnostics: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    # Keep this additive field last so existing positional DTO construction
    # retains the pre-observation argument order.
    observations: tuple[ObservationReport, ...] = ()


class Job:
    """A completed local Job with the same surface used by future adapters."""

    def __init__(self, job_id: str, result: JobResult) -> None:
        self.id = job_id
        self._result = result

    def status(self) -> str:
        return self._result.status

    def wait(self) -> JobResult:
        return self._result

    def result(self) -> JobResult:
        return self._result

    def cancel(self) -> str:
        if self._result.status in {"queued", "running"}:
            return "accepted"
        return "already-complete"


def submit_source(
    source: str,
    *,
    settings: dict[str, Any] | None = None,
    stdout: TextIO | None = None,
) -> Job:
    """Submit source to the local adapter and return a provider-neutral Job."""

    settings = dict(settings or {})
    job_id = f"local-{uuid4().hex}"
    return _submit_compiled(
        compile_source(source), settings=settings, stdout=stdout, job_id=job_id
    )


def submit_path(
    entry: str,
    *,
    settings: dict[str, Any] | None = None,
    stdout: TextIO | None = None,
) -> Job:
    """Submit a linked source path through the same local Job adapter."""

    settings = dict(settings or {})
    job_id = f"local-{uuid4().hex}"
    return _submit_compiled(
        compile_path(entry), settings=settings, stdout=stdout, job_id=job_id
    )


def _submit_compiled(
    compiled: CompileResult,
    *,
    settings: dict[str, Any],
    stdout: TextIO | None,
    job_id: str,
) -> Job:
    if compiled.unit is None or not compiled.ok:
        return Job(
            job_id,
            JobResult(
                status="failed",
                diagnostics=tuple(compiled.diagnostics),
                metadata={"target": settings.get("target", "local")},
            ),
        )

    try:
        evaluator = Evaluator(seed=settings.get("seed"))
        evaluated = evaluator.run_unit(compiled.unit, stdout=stdout)
    except KernelError as exc:
        return Job(
            job_id,
            JobResult(
                status="failed",
                diagnostics=({"code": "RUNTIME_ERROR", "message": str(exc)},),
                metadata={"target": settings.get("target", "local")},
            ),
        )

    measurement = _measurement_envelope(evaluated)
    measurements = () if measurement is None else (measurement,)
    metadata = {"target": settings.get("target", "local")}
    if evaluated.mixed_state_measured:
        metadata["state_type"] = "DensityState"
        metadata["execution_lane"] = evaluated.execution_lane or "cpu/simulator"
    if evaluated.measurement_kind is not None:
        metadata["measurement_kind"] = evaluated.measurement_kind
    return Job(
        job_id,
        JobResult(
            status="succeeded",
            measurements=measurements,
            diagnostics=tuple(compiled.diagnostics),
            metadata=metadata,
        ),
    )


def run_source(
    source: str,
    *,
    settings: dict[str, Any] | None = None,
    stdout: TextIO | None = None,
) -> JobResult:
    """Blocking convenience API equivalent to submit followed by result."""

    return submit_source(source, settings=settings, stdout=stdout).result()


def run_path(
    entry: str,
    *,
    settings: dict[str, Any] | None = None,
    stdout: TextIO | None = None,
) -> JobResult:
    """Blocking convenience API for a linked source path."""

    return submit_path(entry, settings=settings, stdout=stdout).result()


def _measurement_envelope(evaluated: EvalResult) -> MeasurementEnvelope | None:
    measured = evaluated.measure
    if measured is None:
        return None
    return MeasurementEnvelope(
        value=measured.value,
        marginal=dict(measured.marginal),
        vacuum=measured.vacuum,
        sink=measured.sink,
        output=measured.output,
    )
