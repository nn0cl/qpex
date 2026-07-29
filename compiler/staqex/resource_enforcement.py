"""Execution-boundary checks for simulator resource budgets.

This module consumes immutable resource DTOs. It does not load manifests,
allocate simulator state, emit QASM, or contact a provider.
"""

from __future__ import annotations

from dataclasses import dataclass

from .resource_profile import ResourceProfile, SimulationResourceEstimate


_SIMULATOR_LANE = "simulator"
_QASM_LANE = "qasm"
_QPU_LANE = "qpu"
_LANES = frozenset({_SIMULATOR_LANE, _QASM_LANE, _QPU_LANE})


@dataclass(frozen=True)
class SimulatorBudgetDecision:
    """Immutable result of checking one estimate against one profile."""

    continue_execution: bool
    diagnostics: tuple[dict[str, object], ...] = ()


def enforce_optional_budget(
    profile: ResourceProfile | None,
    estimate: SimulationResourceEstimate | None,
    *,
    lane: str,
) -> SimulatorBudgetDecision | None:
    """Enforce a configured budget while preserving legacy no-input calls."""
    if profile is None and estimate is None:
        return None
    if profile is None or estimate is None:
        raise ValueError(
            "resource_profile and resource_estimate must be provided together"
        )
    return enforce_simulator_budget(profile, estimate, lane=lane)


def enforce_simulator_budget(
    profile: ResourceProfile,
    estimate: SimulationResourceEstimate,
    *,
    lane: str,
) -> SimulatorBudgetDecision:
    """Decide whether an estimate may cross the requested execution lane.

    ``Warn`` can continue only on the local simulator lane. QASM and QPU are
    deployment boundaries and therefore reject an exceeded estimate even when
    the manifest selected ``Warn``.
    """
    if lane not in _LANES:
        raise ValueError(f"unsupported execution lane `{lane}`")

    limit = profile.simulator.memory_limit_bytes
    if estimate.estimated_bytes <= limit:
        return SimulatorBudgetDecision(continue_execution=True)

    warning_allowed = _warning_allowed(profile, lane)
    return SimulatorBudgetDecision(
        continue_execution=warning_allowed,
        diagnostics=(_resource_diagnostic(profile, estimate, lane, warning_allowed),),
    )


def _warning_allowed(profile: ResourceProfile, lane: str) -> bool:
    """Return whether an exceeded estimate may continue on this lane."""
    return lane == _SIMULATOR_LANE and profile.simulator.policy == "Warn"


def _resource_diagnostic(
    profile: ResourceProfile,
    estimate: SimulationResourceEstimate,
    lane: str,
    warning_allowed: bool,
) -> dict[str, object]:
    """Build one contextual diagnostic without changing the decision policy."""
    limit = profile.simulator.memory_limit_bytes
    action = "continue" if warning_allowed else "abort"
    code = (
        "SIMULATOR_RESOURCE_WARNING"
        if warning_allowed
        else "SIMULATOR_RESOURCE_ERROR"
    )
    return {
        "code": code,
        "message": (
            f"simulator estimate exceeds memory limit; action={action}; "
            f"representation={estimate.representation}; "
            f"logical_qubits={estimate.logical_qubits}; "
            f"estimated_bytes={estimate.estimated_bytes}; "
            f"memory_limit_bytes={limit}; "
            f"policy={profile.simulator.policy}; "
            f"workspace_factor={estimate.workspace_factor}; "
            f"formula_version={estimate.formula_version}"
        ),
        "representation": estimate.representation,
        "logical_qubits": estimate.logical_qubits,
        "estimated_bytes": estimate.estimated_bytes,
        "memory_limit_bytes": limit,
        "policy": profile.simulator.policy,
        "lane": lane,
        "workspace_factor": estimate.workspace_factor,
        "formula_version": estimate.formula_version,
    }
