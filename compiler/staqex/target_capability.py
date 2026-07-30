"""Provider-neutral target capability profiles and physical target port.

Fake adapters and immutable profiles only. Does not import Physics IR,
Semantic IR, provider SDKs, credentials, or network clients.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

from .target_routing import TargetSnapshot


Diagnostic = dict[str, Any]
SCHEMA_VERSION = "1"
_FIXTURE_QUBITS = {
    "CH0_COMMON_PHYSICAL": 2,
    "CH1_DIGITAL_RESEARCH": 4,
    "NH5_REFERENCE": 8,
}


@dataclass(frozen=True, slots=True)
class Freshness:
    status: str
    age_token: str | None


@dataclass(frozen=True, slots=True)
class CapabilityUnknown:
    name: str
    reason: str


@dataclass(frozen=True, slots=True)
class TargetCapabilityProfile:
    profile_id: str
    schema_version: str
    snapshot_id: str
    native_operations: tuple[str, ...]
    connectivity: tuple[tuple[int, int], ...]
    physical_qubits: tuple[int, ...]
    measurement_supported: bool
    reset_supported: bool
    timing_resolution: str
    dynamic_supported: bool
    carrier_kind: str
    computation_model: str
    qudit_dimensions: tuple[int, ...]
    max_logical_qubits: int
    max_physical_qubits: int
    max_concurrent_measurements: int
    deployment_policy: str
    resource_policy: str
    power_policy: str
    memory_policy: str
    consent_policy: str
    freshness: Freshness
    unknowns: tuple[CapabilityUnknown, ...]


@dataclass(frozen=True, slots=True)
class SupportDecision:
    status: str
    exceeded_dimensions: tuple[str, ...]
    selected_alternative: str | None


class PhysicalTargetPort(Protocol):
    def load_profile(self, profile_id: str) -> TargetCapabilityProfile: ...


def _diagnostic(code: str, message: str) -> Diagnostic:
    return {"code": code, "message": message}


def _verify_freshness(profile: TargetCapabilityProfile) -> list[Diagnostic]:
    if profile.freshness.status != "stale":
        return []
    return [
        _diagnostic(
            "CAPABILITY_STALE",
            "capability freshness is stale; facts must remain explicit",
        )
    ]


def _verify_unknowns(profile: TargetCapabilityProfile) -> list[Diagnostic]:
    return [
        _diagnostic(
            "CAPABILITY_UNKNOWN_REASON_REQUIRED",
            f"{unknown.name} requires an explicit reason",
        )
        for unknown in profile.unknowns
        if not unknown.reason
    ]


def _policy_fields(profile: TargetCapabilityProfile) -> tuple[str, ...]:
    return (
        profile.carrier_kind,
        profile.computation_model,
        profile.deployment_policy,
        profile.resource_policy,
        profile.power_policy,
        profile.memory_policy,
        profile.consent_policy,
    )


def _verify_policies(profile: TargetCapabilityProfile) -> list[Diagnostic]:
    if any(not field for field in _policy_fields(profile)) or not profile.qudit_dimensions:
        return [
            _diagnostic(
                "CAPABILITY_POLICY_INCOMPLETE",
                "model and policy fields must be explicit",
            )
        ]
    return []


def verify_capability_profile(
    profile: TargetCapabilityProfile,
) -> list[Diagnostic]:
    diagnostics = _verify_freshness(profile)
    diagnostics.extend(_verify_unknowns(profile))
    diagnostics.extend(_verify_policies(profile))
    return diagnostics


def evaluate_support(
    profile: TargetCapabilityProfile,
    demand: Mapping[str, Any],
) -> SupportDecision:
    exceeded: list[str] = []
    logical_qubits = demand.get("logical_qubits")
    if (
        isinstance(logical_qubits, int)
        and logical_qubits > profile.max_logical_qubits
    ):
        exceeded.append("max_logical_qubits")
    if demand.get("needs_dynamic") and not profile.dynamic_supported:
        exceeded.append("dynamic_supported")
    return SupportDecision(
        status="rejected" if exceeded else "supported",
        exceeded_dimensions=tuple(exceeded),
        selected_alternative=None,
    )


def project_to_routing_snapshot(
    profile: TargetCapabilityProfile,
) -> TargetSnapshot:
    return TargetSnapshot(
        snapshot_id=profile.snapshot_id,
        profile_id=profile.profile_id,
        schema_version=profile.schema_version,
        physical_qubits=profile.physical_qubits,
        connectivity=profile.connectivity,
        native_operations=profile.native_operations,
        measurement_supported=profile.measurement_supported,
        reset_supported=profile.reset_supported,
        timing_resolution=profile.timing_resolution,
        max_concurrent_measurements=profile.max_concurrent_measurements,
        max_logical_qubits=profile.max_logical_qubits,
    )


def _line_connectivity(qubits: int) -> tuple[tuple[int, int], ...]:
    return tuple((index, index + 1) for index in range(qubits - 1))


def _fixture_profile(
    profile_id: str,
    *,
    qubits: int,
    dynamic_supported: bool = False,
) -> TargetCapabilityProfile:
    return TargetCapabilityProfile(
        profile_id=profile_id,
        schema_version=SCHEMA_VERSION,
        snapshot_id=f"cap.{profile_id.lower()}",
        native_operations=("rz", "sx", "cx"),
        connectivity=_line_connectivity(qubits),
        physical_qubits=tuple(range(qubits)),
        measurement_supported=True,
        reset_supported=True,
        timing_resolution="1ns",
        dynamic_supported=dynamic_supported,
        carrier_kind="qubit",
        computation_model="digital-gate",
        qudit_dimensions=(2,),
        max_logical_qubits=qubits,
        max_physical_qubits=qubits,
        max_concurrent_measurements=1,
        deployment_policy="local",
        resource_policy="abort-on-exceed",
        power_policy="unknown",
        memory_policy="bounded",
        consent_policy="local-only",
        freshness=Freshness(status="fresh", age_token="0s"),
        unknowns=(),
    )


class FakePhysicalTargetPort:
    """In-memory CH0/CH1/NH5 fixtures sharing one schema version."""

    def __init__(self) -> None:
        self._profiles = {
            profile_id: _fixture_profile(profile_id, qubits=qubits)
            for profile_id, qubits in _FIXTURE_QUBITS.items()
        }

    def load_profile(self, profile_id: str) -> TargetCapabilityProfile:
        try:
            return self._profiles[profile_id]
        except KeyError as error:
            raise KeyError(profile_id) from error
