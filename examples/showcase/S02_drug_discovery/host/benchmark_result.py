"""S02 Host-side BenchmarkResult DTO and builder (LISS-0323, WP-0093 work
unit D).

Maps S02's classical/quantum boundary onto already-shipped Kernel
primitives -- terminal `measure` and `MeasurementEnvelope.vacuum` -- into
the accepted S02 spec's Result contract. Does not define
`Observable<T>`/`Projection<T>`/`Observation<T>` as Kernel types (WP-0092's
own open decision) and does not compute real scores or classical baselines
(deferred to work unit E; no S02 `.sqx` program exists yet to produce
them).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from compiler.staqex.host import JobResult


@dataclass(frozen=True)
class BenchmarkResult:
    """Host report for one S02 execution.

    An empty, missing, or unverifiable terminal observation is recorded as
    a `"failed"` feasibility_verdict with no terminal_selection -- never a
    fabricated selection or score.
    """

    feasibility_verdict: str  # "feasible" | "failed"
    terminal_selection: Any | None
    resource_metadata: dict[str, Any] = field(default_factory=dict)
    optimality_claim: str = "none"


def build_benchmark_result(job_result: JobResult) -> BenchmarkResult:
    """Build a BenchmarkResult from a JobResult's terminal measurement.

    Resource metadata is copied verbatim from the JobResult; nothing is
    invented when the JobResult does not provide it.
    """

    resource_metadata = dict(job_result.metadata)

    if not job_result.measurements:
        return BenchmarkResult(
            feasibility_verdict="failed",
            terminal_selection=None,
            resource_metadata=resource_metadata,
        )

    envelope = job_result.measurements[-1]
    if envelope.vacuum:
        return BenchmarkResult(
            feasibility_verdict="failed",
            terminal_selection=None,
            resource_metadata=resource_metadata,
        )

    return BenchmarkResult(
        feasibility_verdict="feasible",
        terminal_selection=envelope.value,
        resource_metadata=resource_metadata,
    )
