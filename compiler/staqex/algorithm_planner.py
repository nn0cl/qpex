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


def _has_identity_provenance(decision: PlannerDecision) -> bool:
    return all(
        (
            decision.request.request_id,
            decision.request.hamiltonian_id,
            decision.request.provenance,
            decision.candidate.candidate_id,
            decision.preparation.preparation_id,
        )
    )


def _has_approximation_evidence(decision: PlannerDecision) -> bool:
    evaluation = decision.evaluation
    return bool(evaluation.approximation_bound and evaluation.resource_expression)


def _has_decision_evidence(evaluation: CandidateEvaluation) -> bool:
    return bool(
        evaluation.alternatives
        and evaluation.assumptions
        and evaluation.rejection_reasons
        and all(evaluation.rejection_reasons)
        and evaluation.policy_provenance
    )


def _has_explicit_preparation(preparation: PreparationContract) -> bool:
    return bool(
        preparation.source
        and preparation.obligations
        and not preparation.assumes_zero_state
        and not preparation.assumes_oracle
    )


def _contains_forbidden_policy(evaluation: CandidateEvaluation) -> bool:
    evidence = " ".join(
        (
            evaluation.disposition,
            evaluation.policy_provenance,
            *evaluation.alternatives,
            *evaluation.assumptions,
        )
    ).casefold()
    return "runtime" in evidence or "provider." in evidence


def _diagnostics(decision: PlannerDecision) -> list[str]:
    codes: list[str] = []
    evaluation = decision.evaluation
    if not _has_identity_provenance(decision):
        codes.append("PLANNER_PROVENANCE_INCOMPLETE")
    if (
        evaluation.disposition == "accepted"
        and decision.candidate.exactness == "approximate"
        and not _has_approximation_evidence(decision)
    ):
        codes.append("PLANNER_APPROXIMATION_INVALID")
    if not _has_decision_evidence(evaluation):
        codes.append("PLANNER_DECISION_EVIDENCE_INVALID")
    if not _has_explicit_preparation(decision.preparation):
        codes.append("PLANNER_PREPARATION_INVALID")
    if _contains_forbidden_policy(evaluation):
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
    valid = not codes

    return PlannerResult(
        disposition=evaluation.disposition if valid else "rejected",
        selected_family=(
            decision.candidate.family
            if valid and evaluation.disposition == "accepted"
            else None
        ),
        approximation_bound=evaluation.approximation_bound,
        resource_expression=evaluation.resource_expression,
        policy_provenance=evaluation.policy_provenance,
        preparation_source=decision.preparation.source,
        rejection_reasons=evaluation.rejection_reasons,
        diagnostic_codes=tuple(codes),
    )
