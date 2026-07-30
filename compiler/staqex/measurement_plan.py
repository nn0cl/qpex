"""Provider-neutral measurement grouping and shot allocation contracts."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True, slots=True)
class ObservableSpec:
    observable_id: str
    terms: tuple[str, ...]
    origin_id: str


@dataclass(frozen=True, slots=True)
class CompatibilityWitness:
    group_id: str
    relation: str
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MeasurementGroup:
    group_id: str
    observable_ids: tuple[str, ...]
    witness: CompatibilityWitness
    basis: str


@dataclass(frozen=True, slots=True)
class ConfidenceTarget:
    confidence: str
    interval: str
    estimator: str


@dataclass(frozen=True, slots=True)
class CovarianceAssumption:
    kind: str
    evidence: str


@dataclass(frozen=True, slots=True)
class ShotAllocation:
    group_id: str
    shots: str
    lower_bound: str
    rounding: str


@dataclass(frozen=True, slots=True)
class MeasurementPlan:
    plan_id: str
    profile: str
    observables: tuple[ObservableSpec, ...]
    groups: tuple[MeasurementGroup, ...]
    confidence_target: ConfidenceTarget
    covariance: CovarianceAssumption
    allocations: tuple[ShotAllocation, ...]
    total_shots: str
    provenance: tuple[str, ...]


def reconstruct_observable(
    plan: MeasurementPlan, observable_id: str
) -> MeasurementGroup:
    for group in plan.groups:
        if observable_id in group.observable_ids:
            return group
    raise KeyError(observable_id)


def allocate_shots(
    groups: tuple[MeasurementGroup, ...],
    target: ConfidenceTarget,
    covariance: CovarianceAssumption,
    *,
    total_shots: str,
) -> tuple[ShotAllocation, ...]:
    """Allocate an explicit budget deterministically across ordered groups.

    The first contract uses equal group weights.  The target and covariance
    records are validated here so future weighted estimators can be added
    without turning an absent policy into an implicit default.
    """

    _require_statistical_policy(target, covariance)
    budget = _parse_nonnegative_integer(total_shots)
    if not groups or budget < len(groups):
        raise ValueError("MEASUREMENT_ALLOCATION_INVALID: budget is too small")

    quotient, remainder = divmod(budget, len(groups))
    return tuple(
        ShotAllocation(
            group_id=group.group_id,
            shots=str(quotient + (index < remainder)),
            lower_bound="1",
            rounding="largest-remainder",
        )
        for index, group in enumerate(groups)
    )


def verify_measurement_plan(plan: MeasurementPlan) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    observable_ids = [item.observable_id for item in plan.observables]
    if len(observable_ids) != len(set(observable_ids)):
        diagnostics.append(
            _diagnostic("MEASUREMENT_OBSERVABLE_ID_CONFLICT", "observable IDs repeat")
        )

    observable_set = set(observable_ids)
    group_ids = [group.group_id for group in plan.groups]
    if len(group_ids) != len(set(group_ids)):
        diagnostics.append(
            _diagnostic("MEASUREMENT_GROUP_ID_CONFLICT", "group IDs repeat")
        )

    for group in plan.groups:
        if group.witness.group_id != group.group_id:
            diagnostics.append(
                _diagnostic(
                    "MEASUREMENT_WITNESS_INVALID",
                    f"witness does not identify {group.group_id}",
                )
            )
        if group.witness.relation != "commutes":
            diagnostics.append(
                _diagnostic(
                    "MEASUREMENT_GROUP_INCOMPATIBLE",
                    f"group {group.group_id} is not compatible",
                )
            )
        for observable_id in group.observable_ids:
            if observable_id not in observable_set:
                diagnostics.append(
                    _diagnostic(
                        "MEASUREMENT_MAPPING_INCOMPLETE",
                        f"unknown observable {observable_id}",
                    )
                )

    diagnostics.extend(_verify_statistical_policy(plan))
    diagnostics.extend(_verify_allocations(plan))
    for observable in plan.observables:
        if not observable.origin_id or observable.origin_id not in plan.provenance:
            diagnostics.append(
                _diagnostic(
                    "MEASUREMENT_PROVENANCE_INCOMPLETE",
                    f"observable {observable.observable_id} lacks provenance",
                )
            )
    return diagnostics


def _verify_statistical_policy(plan: MeasurementPlan) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    try:
        confidence = Decimal(plan.confidence_target.confidence)
    except (InvalidOperation, ValueError):
        confidence = Decimal("-1")
    if not 0 < confidence < 1 or not plan.confidence_target.interval:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_STATISTICAL_TARGET_INVALID",
                "confidence target is incomplete or outside (0, 1)",
            )
        )
    if not plan.confidence_target.estimator:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_STATISTICAL_TARGET_INVALID",
                "estimator is required",
            )
        )
    if not plan.covariance.kind or not plan.covariance.evidence:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_COVARIANCE_INVALID",
                "covariance assumption requires kind and evidence",
            )
        )
    return diagnostics


def _verify_allocations(plan: MeasurementPlan) -> list[dict[str, str]]:
    diagnostics: list[dict[str, str]] = []
    allocation_groups = {item.group_id for item in plan.allocations}
    expected_groups = {group.group_id for group in plan.groups}
    if allocation_groups != expected_groups:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_ALLOCATION_INVALID",
                "allocations must cover exactly the measurement groups",
            )
        )
    try:
        total = sum(_parse_nonnegative_integer(item.shots) for item in plan.allocations)
        expected = _parse_nonnegative_integer(plan.total_shots)
    except ValueError:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_ALLOCATION_INVALID",
                "shot counts and total budget must be nonnegative integers",
            )
        )
        return diagnostics
    if total != expected:
        diagnostics.append(
            _diagnostic(
                "MEASUREMENT_ALLOCATION_INVALID",
                "allocation does not conserve the total budget",
            )
        )
    for item in plan.allocations:
        if item.rounding != "largest-remainder" or item.lower_bound != "1":
            diagnostics.append(
                _diagnostic(
                    "MEASUREMENT_ALLOCATION_INVALID",
                    f"allocation policy for {item.group_id} is not deterministic",
                )
            )
    return diagnostics


def _require_statistical_policy(
    target: ConfidenceTarget, covariance: CovarianceAssumption
) -> None:
    if not target.confidence or not target.interval or not target.estimator:
        raise ValueError("MEASUREMENT_STATISTICAL_TARGET_INVALID: incomplete target")
    if not covariance.kind or not covariance.evidence:
        raise ValueError("MEASUREMENT_COVARIANCE_INVALID: incomplete assumption")


def _parse_nonnegative_integer(value: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("MEASUREMENT_ALLOCATION_INVALID: integer required") from error
    if parsed < 0:
        raise ValueError("MEASUREMENT_ALLOCATION_INVALID: negative budget")
    return parsed


def _diagnostic(code: str, message: str) -> dict[str, str]:
    return {"code": code, "message": message}
