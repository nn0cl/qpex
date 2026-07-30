"""Provider-neutral Hamiltonian algorithm planning for LISS-0088.

The planner records policy evidence and obligations. It does not emit gates,
call a simulator, select a provider, or run a numerical method.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PlannerProfile:
    profile_id: str
    resource_envelope: tuple[str, ...]


@dataclass(frozen=True)
class PlannerRequest:
    request_id: str
    hamiltonian_id: str
    observable_ids: tuple[str, ...]
    provenance: tuple[str, ...]
    operation: str
    profile: PlannerProfile
    constraints: tuple[str, ...]


@dataclass(frozen=True)
class AlgorithmCandidate:
    candidate_id: str
    family: str
    exactness: str
    parameters: tuple[str, ...]
    prerequisites: tuple[str, ...]


@dataclass(frozen=True)
class CandidateEvaluation:
    evaluation_id: str
    disposition: str
    alternatives: tuple[str, ...]
    assumptions: tuple[str, ...]
    rejection_reasons: tuple[str, ...]
    policy_provenance: str
    approximation_bound: str | None
    resource_expression: str


@dataclass(frozen=True)
class PreparationContract:
    preparation_id: str
    source: str
    obligations: tuple[str, ...]
    assumes_zero_state: bool
    assumes_oracle: bool


@dataclass(frozen=True)
class PlannerDecision:
    request: PlannerRequest
    candidate: AlgorithmCandidate
    evaluation: CandidateEvaluation
    preparation: PreparationContract


@dataclass(frozen=True)
class PlannerResult:
    disposition: str
    selected_family: str | None
    approximation_bound: str | None
    resource_expression: str
    policy_provenance: str
    preparation_source: str
    rejection_reasons: tuple[str, ...]
    diagnostic_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _diagnostics(decision: PlannerDecision) -> list[str]:
    codes: list[str] = []
    if not all(
        (
            decision.request.request_id,
            decision.request.hamiltonian_id,
            decision.request.provenance,
            decision.candidate.candidate_id,
            decision.preparation.preparation_id,
        )
    ):
        codes.append("PLANNER_PROVENANCE_INCOMPLETE")

    evaluation = decision.evaluation
    if evaluation.disposition == "accepted" and decision.candidate.exactness == "approximate":
        if not evaluation.approximation_bound or not evaluation.resource_expression:
            codes.append("PLANNER_APPROXIMATION_INVALID")

    if not (
        evaluation.alternatives
        and evaluation.assumptions
        and evaluation.rejection_reasons
        and all(evaluation.rejection_reasons)
        and evaluation.policy_provenance
    ):
        codes.append("PLANNER_DECISION_EVIDENCE_INVALID")

    preparation = decision.preparation
    if (
        not preparation.source
        or not preparation.obligations
        or preparation.assumes_zero_state
        or preparation.assumes_oracle
    ):
        codes.append("PLANNER_PREPARATION_INVALID")

    evidence = " ".join(
        (
            evaluation.disposition,
            evaluation.policy_provenance,
            *evaluation.alternatives,
            *evaluation.assumptions,
        )
    ).casefold()
    if "runtime" in evidence or "provider." in evidence:
        codes.append("PLANNER_POLICY_INVALID")

    if evaluation.disposition == "accepted" and decision.candidate.family in {
        "qubitization",
        "lcu",
    }:
        codes.append("PLANNER_UNSUPPORTED_METHOD_INVALID")
    return sorted(set(codes))


def plan_algorithm(decision: PlannerDecision) -> PlannerResult:
    """Evaluate one immutable, provider-neutral planning decision."""

    codes = _diagnostics(decision)
    evaluation = decision.evaluation
    disposition = evaluation.disposition
    selected_family = decision.candidate.family if disposition == "accepted" else None
    if codes:
        disposition = "rejected"
        selected_family = None

    return PlannerResult(
        disposition=disposition,
        selected_family=selected_family,
        approximation_bound=evaluation.approximation_bound,
        resource_expression=evaluation.resource_expression,
        policy_provenance=evaluation.policy_provenance,
        preparation_source=decision.preparation.source,
        rejection_reasons=evaluation.rejection_reasons,
        diagnostic_codes=tuple(codes),
    )
