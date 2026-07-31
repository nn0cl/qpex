"""Backend-neutral simulator capability profiles and fake port.

Fake adapters and immutable profiles only. Does not import Physics IR,
Semantic IR, engine packages, credentials, or network clients.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Protocol

SCHEMA_VERSION = "1"
_DEFAULT_OPS = ("h", "x", "cx", "rz", "measure")
_DEFAULT_CARRIERS = ("qubit",)
_DEFAULT_OBSERVATIONS = ("terminal-measure", "expectation")
_GIB = 1024 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class SimulatorCapabilityProfile:
    profile_id: str
    schema_version: str
    oracle_class: str
    max_qubits: int
    max_memory_bytes: int
    supported_operations: tuple[str, ...]
    supported_carriers: tuple[str, ...]
    observation_modes: tuple[str, ...]
    dynamic_supported: bool


@dataclass(frozen=True, slots=True)
class SimulationBudget:
    max_qubits: int | None
    max_memory_bytes: int | None
    max_shots: int | None
    max_time_ms: int | None
    tolerance: str | None


@dataclass(frozen=True, slots=True)
class ObservationPlanRef:
    plan_id: str
    mode: str


@dataclass(frozen=True, slots=True)
class SimulationRequest:
    plan_id: str
    profile_id: str
    qubit_count: int
    operations: tuple[str, ...]
    carrier_kind: str
    needs_dynamic: bool
    seed: str
    budget: SimulationBudget
    observation: ObservationPlanRef
    provenance_token: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    status: str
    exceeded_dimensions: tuple[str, ...]
    missing_dimensions: tuple[str, ...]
    selected_alternative: str | None


@dataclass(frozen=True, slots=True)
class SimulationResult:
    execution_kind: str
    profile_id: str
    plan_id: str
    seed_used: str
    observation_plan_id: str
    observation_mode: str
    payload: Mapping[str, Any]
    diagnostics: tuple[str, ...]


class SimulatorPort(Protocol):
    def capabilities(self, profile_id: str) -> SimulatorCapabilityProfile: ...

    def validate(self, request: SimulationRequest) -> ValidationReport: ...

    def execute(self, request: SimulationRequest) -> SimulationResult: ...


def _fixture_profile(
    profile_id: str,
    *,
    oracle_class: str,
    max_qubits: int,
    dynamic_supported: bool = False,
) -> SimulatorCapabilityProfile:
    return SimulatorCapabilityProfile(
        profile_id=profile_id,
        schema_version=SCHEMA_VERSION,
        oracle_class=oracle_class,
        max_qubits=max_qubits,
        max_memory_bytes=8 * _GIB,
        supported_operations=_DEFAULT_OPS,
        supported_carriers=_DEFAULT_CARRIERS,
        observation_modes=_DEFAULT_OBSERVATIONS,
        dynamic_supported=dynamic_supported,
    )


def _build_fixture_table() -> dict[str, SimulatorCapabilityProfile]:
    return {
        "SIM0_EXACT": _fixture_profile(
            "SIM0_EXACT", oracle_class="exact", max_qubits=20
        ),
        "SIM1_MIXED": _fixture_profile(
            "SIM1_MIXED", oracle_class="mixed", max_qubits=10
        ),
    }


def _missing_budget_fields(budget: SimulationBudget) -> tuple[str, ...]:
    checks = (
        ("max_qubits", budget.max_qubits),
        ("max_memory_bytes", budget.max_memory_bytes),
        ("max_shots", budget.max_shots),
        ("max_time_ms", budget.max_time_ms),
    )
    return tuple(name for name, value in checks if value is None)


def _exceeded_dimensions(
    profile: SimulatorCapabilityProfile,
    request: SimulationRequest,
) -> tuple[str, ...]:
    exceeded: list[str] = []
    if request.qubit_count > profile.max_qubits:
        exceeded.append("max_qubits")
    if request.carrier_kind not in profile.supported_carriers:
        exceeded.append("carrier_kind")
    if request.needs_dynamic and not profile.dynamic_supported:
        exceeded.append("dynamic_supported")
    if request.observation.mode not in profile.observation_modes:
        exceeded.append("observation_mode")
    if any(
        operation not in profile.supported_operations
        for operation in request.operations
    ):
        exceeded.append("supported_operations")
    return tuple(exceeded)


def _validate_request(
    profile: SimulatorCapabilityProfile,
    request: SimulationRequest,
) -> ValidationReport:
    missing = _missing_budget_fields(request.budget)
    if missing:
        return ValidationReport(
            status="rejected",
            exceeded_dimensions=(),
            missing_dimensions=missing,
            selected_alternative=None,
        )

    exceeded = _exceeded_dimensions(profile, request)
    return ValidationReport(
        status="rejected" if exceeded else "accepted",
        exceeded_dimensions=exceeded,
        missing_dimensions=(),
        selected_alternative=None,
    )


def _canned_payload(request: SimulationRequest) -> dict[str, Any]:
    # Deterministic fake oracle payload; not a physical execution claim.
    if request.qubit_count <= 0:
        return {"probabilities": {}}
    width = min(request.qubit_count, 4)
    size = 1 << width
    weight = 1.0 / float(size)
    return {
        "probabilities": {
            format(index, f"0{width}b"): weight for index in range(size)
        }
    }


def _rejection_message(report: ValidationReport) -> str:
    dims = ",".join(report.exceeded_dimensions or report.missing_dimensions)
    return f"rejected before allocation: {dims}"


class FakeSimulatorPort:
    """In-memory SIM0/SIM1 fixtures sharing one schema version."""

    def __init__(self) -> None:
        self._profiles = _build_fixture_table()

    def capabilities(self, profile_id: str) -> SimulatorCapabilityProfile:
        try:
            return self._profiles[profile_id]
        except KeyError as error:
            raise KeyError(profile_id) from error

    def validate(self, request: SimulationRequest) -> ValidationReport:
        return _validate_request(self.capabilities(request.profile_id), request)

    def execute(self, request: SimulationRequest) -> SimulationResult:
        report = self.validate(request)
        if report.status != "accepted":
            raise ValueError(_rejection_message(report))
        return SimulationResult(
            execution_kind="simulation",
            profile_id=request.profile_id,
            plan_id=request.plan_id,
            seed_used=request.seed,
            observation_plan_id=request.observation.plan_id,
            observation_mode=request.observation.mode,
            payload=_canned_payload(request),
            diagnostics=(),
        )
