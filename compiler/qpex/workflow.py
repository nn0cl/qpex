"""Provider-neutral host workflow contracts (LISS-0035, ADR 0072)."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence

from .host import Job, JobResult


class WorkflowValidationError(ValueError):
    """A workflow request or result projection violates its contract."""


@dataclass(frozen=True, slots=True)
class ParamBinding:
    parameter: str
    value: Any


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    target: str = "local"
    shots: int | None = None
    seed: int | None = None


@dataclass(frozen=True, slots=True)
class JobRequest:
    experiment: str
    bindings: tuple[ParamBinding, ...]
    execution: ExecutionPolicy


@dataclass(frozen=True, slots=True)
class MeasurementProjection:
    observable: str
    value: Any | None
    marginal: Mapping[Any, float]
    metadata: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class WorkflowReport:
    status: str
    iterations: int
    final_bindings: tuple[ParamBinding, ...]
    projections: tuple[MeasurementProjection, ...]


class WorkflowPlan:
    """Immutable workflow definition for one experiment contract."""

    def __init__(
        self,
        *,
        experiment: str,
        parameters: Sequence[str] = (),
        observables: Sequence[str] = (),
    ) -> None:
        self.experiment = experiment
        self.parameters = tuple(parameters)
        self.observables = tuple(observables)
        if len(set(self.parameters)) != len(self.parameters):
            raise WorkflowValidationError("workflow parameters must be unique")
        if len(set(self.observables)) != len(self.observables):
            raise WorkflowValidationError("workflow observables must be unique")

    def request(
        self,
        *,
        bindings: Sequence[ParamBinding] = (),
        execution: ExecutionPolicy | None = None,
    ) -> JobRequest:
        binding_tuple = tuple(bindings)
        names = tuple(binding.parameter for binding in binding_tuple)
        if len(set(names)) != len(names):
            raise WorkflowValidationError("parameter bindings must be unique")
        undeclared = set(names) - set(self.parameters)
        if undeclared:
            raise WorkflowValidationError(
                f"undeclared workflow parameters: {sorted(undeclared)}"
            )
        missing = set(self.parameters) - set(names)
        if missing:
            raise WorkflowValidationError(
                f"missing workflow parameters: {sorted(missing)}"
            )
        return JobRequest(
            experiment=self.experiment,
            bindings=binding_tuple,
            execution=execution or ExecutionPolicy(),
        )

    def run_once(
        self,
        submit: Callable[[JobRequest], Job],
        *,
        bindings: Sequence[ParamBinding] = (),
        execution: ExecutionPolicy | None = None,
        observable: str,
    ) -> MeasurementProjection:
        if observable not in self.observables:
            raise WorkflowValidationError(
                f"undeclared workflow observable: {observable}"
            )
        request = self.request(bindings=bindings, execution=execution)
        return self._run_request(submit, request, observable)

    def run_iterative(
        self,
        submit: Callable[[JobRequest], Job],
        *,
        initial: Sequence[ParamBinding],
        execution: ExecutionPolicy | None = None,
        observable: str,
        update: Callable[[tuple[ParamBinding, ...], MeasurementProjection], Sequence[ParamBinding]],
        until: Callable[[MeasurementProjection, int], bool],
        max_iterations: int,
    ) -> WorkflowReport:
        """Run host feedback iterations over completed Job projections."""

        if max_iterations <= 0:
            raise WorkflowValidationError("max_iterations must be positive")
        bindings = tuple(initial)
        projections: list[MeasurementProjection] = []
        for iteration in range(1, max_iterations + 1):
            request = self.request(bindings=bindings, execution=execution)
            projection = self._run_request(submit, request, observable)
            projections.append(projection)
            if until(projection, iteration):
                return WorkflowReport(
                    status="succeeded",
                    iterations=iteration,
                    final_bindings=bindings,
                    projections=tuple(projections),
                )
            bindings = tuple(update(bindings, projection))
        return WorkflowReport(
            status="max_iterations",
            iterations=max_iterations,
            final_bindings=bindings,
            projections=tuple(projections),
        )

    def _run_request(
        self,
        submit: Callable[[JobRequest], Job],
        request: JobRequest,
        observable: str,
    ) -> MeasurementProjection:
        job = submit(request)
        result = job.result()
        if result.status != "succeeded":
            raise WorkflowValidationError(
                f"workflow Job did not succeed: {result.status}"
            )
        return self._project(result, observable)

    @staticmethod
    def _project(result: JobResult, observable: str) -> MeasurementProjection:
        if not result.measurements:
            raise WorkflowValidationError("JobResult contains no measurement")
        envelope = next(
            (
                item
                for item in result.measurements
                if item.sink == observable
                or getattr(result, "metadata", {}).get("observable") == observable
            ),
            result.measurements[0],
        )
        return MeasurementProjection(
            observable=observable,
            value=envelope.value,
            marginal=MappingProxyType(dict(envelope.marginal)),
            metadata=MappingProxyType(dict(result.metadata)),
        )
