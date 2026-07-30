"""Provider-neutral Algorithm Plan resource estimation and feasibility.

Distinct from host-side simulator budgets in ``resource_profile`` (ADR 0100).
This module does not import provider SDKs, prices, calibration, or routing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


RESOURCE_CATEGORIES = frozenset({"semantic", "logical", "physical"})
FORMULA_VERSION = "resource-estimate-plan-v1"
_PLAN_LITERAL_FIELDS = (
    "logical_qubits",
    "ancillas",
    "depth",
    "operations",
    "measurements",
    "classical_latency",
    "simulator_memory",
)

Diagnostic = dict[str, Any]


class ResourceCategory(str, Enum):
    semantic = "semantic"
    logical = "logical"
    physical = "physical"


@dataclass(frozen=True, slots=True)
class ResourceQuantity:
    category: ResourceCategory
    name: str
    value: int | str


@dataclass(frozen=True, slots=True)
class Unknown:
    name: str
    assumptions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EstimateProvenance:
    formula_version: str
    assumptions: tuple[str, ...]
    uncertainty: str
    profile_snapshot_id: str | None


@dataclass(frozen=True, slots=True)
class PreRoutingEstimate:
    stage: str
    quantities: tuple[ResourceQuantity, ...]
    provenance: EstimateProvenance


@dataclass(frozen=True, slots=True)
class PostRoutingEstimate:
    stage: str
    quantities: tuple[ResourceQuantity, ...]
    unknowns: tuple[Unknown, ...]
    provenance: EstimateProvenance


@dataclass(frozen=True, slots=True)
class CompositionalBudget:
    failure: Unknown
    decoder: Unknown
    link: Unknown
    factory: Unknown
    memory: ResourceQuantity
    time: Unknown
    power: Unknown
    cost: Unknown


@dataclass(frozen=True, slots=True)
class TargetProfileSnapshot:
    profile_id: str
    capabilities: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class FeasibilityReport:
    profile_id: str
    status: str
    exceeded_dimensions: tuple[str, ...]
    selected_alternative: str | None


@dataclass(frozen=True, slots=True)
class ResourceEstimateReport:
    report_id: str
    pre_routing: PreRoutingEstimate
    post_routing: PostRoutingEstimate
    budget: CompositionalBudget
    feasibility: tuple[FeasibilityReport, ...]
    provenance: EstimateProvenance


@dataclass(frozen=True, slots=True)
class SoftResourceEstimate:
    report: ResourceEstimateReport | None
    diagnostics: tuple[Diagnostic, ...]


def _diagnostic(code: str, message: str) -> Diagnostic:
    return {"code": code, "message": message}


def _quantity_categories(quantities: tuple[ResourceQuantity, ...]) -> set[str]:
    return {item.category.value for item in quantities}


def _float_forbidden(value: object) -> bool:
    return isinstance(value, float) and not isinstance(value, bool)


def _unknown_budget_entries(budget: CompositionalBudget) -> tuple[Unknown, ...]:
    return (
        budget.failure,
        budget.decoder,
        budget.link,
        budget.factory,
        budget.time,
        budget.power,
        budget.cost,
    )


def _verify_stages(report: ResourceEstimateReport) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if report.pre_routing.stage != "pre_routing":
        diagnostics.append(
            _diagnostic(
                "RESOURCE_STAGE_MISMATCH",
                "pre_routing.stage must be 'pre_routing'",
            )
        )
    if report.post_routing.stage != "post_routing":
        diagnostics.append(
            _diagnostic(
                "RESOURCE_STAGE_MISMATCH",
                "post_routing.stage must be 'post_routing'",
            )
        )
    return diagnostics


def _verify_quantities(
    stage_name: str, quantities: tuple[ResourceQuantity, ...]
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    categories = _quantity_categories(quantities)
    if len(categories) > 1:
        diagnostics.append(
            _diagnostic(
                "RESOURCE_CATEGORY_MIXED",
                f"{stage_name} mixes resource categories {sorted(categories)}",
            )
        )
    for quantity in quantities:
        if _float_forbidden(quantity.value):
            diagnostics.append(
                _diagnostic(
                    "RESOURCE_QUANTITY_FLOAT_FORBIDDEN",
                    f"{quantity.name} must be exact int or symbolic str",
                )
            )
    return diagnostics


def _verify_unknowns(unknowns: tuple[Unknown, ...]) -> list[Diagnostic]:
    return [
        _diagnostic(
            "RESOURCE_UNKNOWN_ASSUMPTIONS_REQUIRED",
            f"{unknown.name} requires compositional assumptions",
        )
        for unknown in unknowns
        if not unknown.assumptions
    ]


def _verify_budget(budget: CompositionalBudget) -> list[Diagnostic]:
    if any(not entry.assumptions for entry in _unknown_budget_entries(budget)):
        return [
            _diagnostic(
                "RESOURCE_BUDGET_ASSUMPTIONS_REQUIRED",
                "compositional Unknown budgets require assumptions",
            )
        ]
    return []


def verify_resource_estimate_report(
    report: ResourceEstimateReport,
) -> list[Diagnostic]:
    diagnostics = _verify_stages(report)
    diagnostics.extend(
        _verify_quantities("pre_routing", report.pre_routing.quantities)
    )
    diagnostics.extend(
        _verify_quantities("post_routing", report.post_routing.quantities)
    )
    diagnostics.extend(_verify_unknowns(report.post_routing.unknowns))
    diagnostics.extend(_verify_budget(report.budget))
    return diagnostics


def _default_provenance(
    *,
    assumptions: tuple[str, ...] = ("declared-logical-width",),
    uncertainty: str = "exact-count",
    profile_snapshot_id: str | None = "profile.sim0",
) -> EstimateProvenance:
    return EstimateProvenance(
        formula_version=FORMULA_VERSION,
        assumptions=assumptions,
        uncertainty=uncertainty,
        profile_snapshot_id=profile_snapshot_id,
    )


def _logical_quantity(name: str, value: int | str) -> ResourceQuantity:
    return ResourceQuantity(
        category=ResourceCategory.logical,
        name=name,
        value=value,
    )


def _awaiting_routing_post_estimate() -> PostRoutingEstimate:
    assumptions = ("awaiting-liss-0092-routing",)
    return PostRoutingEstimate(
        stage="post_routing",
        quantities=(),
        unknowns=(Unknown(name="physical_qubits", assumptions=assumptions),),
        provenance=_default_provenance(
            assumptions=assumptions,
            uncertainty="unknown",
            profile_snapshot_id="profile.ch1",
        ),
    )


def _default_compositional_budget() -> CompositionalBudget:
    return CompositionalBudget(
        failure=Unknown("failure_budget", ("independent-faults",)),
        decoder=Unknown("decoder_load", ("no-decoder-model",)),
        link=Unknown("link_budget", ("single-partition",)),
        factory=Unknown("factory_load", ("no-factory",)),
        memory=_logical_quantity("workspace_bytes", 0),
        time=Unknown("wall_time", ("unscheduled",)),
        power=Unknown("power", ("not-modeled",)),
        cost=Unknown("cost", ("no-provider-price",)),
    )


def estimate_resources(plan: Mapping[str, Any]) -> ResourceEstimateReport:
    """Build a pre-routing estimate from explicit plan literals."""

    quantities = tuple(
        _logical_quantity(name, plan[name])
        for name in _PLAN_LITERAL_FIELDS
        if name in plan
    )
    plan_id = str(plan.get("plan_id", "plan.anonymous"))
    return ResourceEstimateReport(
        report_id=f"estimate.{plan_id}",
        pre_routing=PreRoutingEstimate(
            stage="pre_routing",
            quantities=quantities,
            provenance=_default_provenance(),
        ),
        post_routing=_awaiting_routing_post_estimate(),
        budget=_default_compositional_budget(),
        feasibility=(),
        provenance=_default_provenance(),
    )


def _logical_qubit_demand(report: ResourceEstimateReport) -> int | None:
    for quantity in report.pre_routing.quantities:
        if quantity.name == "logical_qubits" and isinstance(quantity.value, int):
            return quantity.value
    return None


def assess_feasibility(
    report: ResourceEstimateReport,
    profile: TargetProfileSnapshot,
) -> FeasibilityReport:
    caps = dict(profile.capabilities)
    demand = _logical_qubit_demand(report)
    exceeded: list[str] = []
    if demand is not None and "max_logical_qubits" in caps:
        limit = int(caps["max_logical_qubits"])
        if demand > limit:
            exceeded.append("max_logical_qubits")
    return FeasibilityReport(
        profile_id=profile.profile_id,
        status="rejected" if exceeded else "feasible",
        exceeded_dimensions=tuple(exceeded),
        selected_alternative=None,
    )


def soft_resource_estimate(
    *,
    plan: Mapping[str, Any] | None,
    profiles: tuple[TargetProfileSnapshot, ...] = (),
) -> SoftResourceEstimate:
    del profiles  # soft absent path does not invent profile carriers
    if plan is None:
        return SoftResourceEstimate(
            report=None,
            diagnostics=(
                _diagnostic(
                    "RES_INPUT_ABSENT",
                    "no Algorithm Plan input; soft estimate invents nothing",
                ),
            ),
        )
    return SoftResourceEstimate(report=estimate_resources(plan), diagnostics=())
