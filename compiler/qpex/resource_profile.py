"""Host-side resource profile loading and simulator estimates.

This module deliberately stops at an immutable, provider-neutral DTO boundary.
The Kernel does not discover or read project files; callers provide a manifest
path and receive a validated profile plus structured diagnostics.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomllib


DEFAULT_BINDER_TERM_LIMIT = 100_000
EMERGENCY_BINDER_TERM_LIMIT = 1_000_000
DEFAULT_SIMULATOR_MEMORY_LIMIT_BYTES = 8_589_934_592
RESOURCE_SCHEMA_VERSION = 1
FORMULA_VERSION = "resource-estimate-v1"
COMPLEX_F64_BYTES = 16

_POLICIES = frozenset({"Warn", "Abort"})


@dataclass(frozen=True)
class _EstimateModel:
    """Named factors for one simulator representation."""

    dimension_base: int
    workspace_factor: int


_ESTIMATE_MODELS: dict[str, _EstimateModel] = {
    "StateVector": _EstimateModel(dimension_base=2, workspace_factor=3),
    "DensityState": _EstimateModel(dimension_base=4, workspace_factor=3),
    "LindbladRK4": _EstimateModel(dimension_base=4, workspace_factor=6),
}


@dataclass(frozen=True)
class BinderExpansionBudget:
    term_limit: int = DEFAULT_BINDER_TERM_LIMIT
    policy: str = "Abort"


@dataclass(frozen=True)
class SimulatorResourceBudget:
    policy: str = "Abort"
    memory_limit_bytes: int = DEFAULT_SIMULATOR_MEMORY_LIMIT_BYTES


@dataclass(frozen=True)
class ResourceDiagnostic:
    code: str
    message: str
    path: str | None = None

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.path is not None:
            result["path"] = self.path
        return result


@dataclass(frozen=True)
class ResourceProfile:
    schema_version: int = RESOURCE_SCHEMA_VERSION
    binder: BinderExpansionBudget = BinderExpansionBudget()
    simulator: SimulatorResourceBudget = SimulatorResourceBudget()
    diagnostics: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class SimulationResourceEstimate:
    representation: str
    logical_qubits: int
    estimated_bytes: int
    workspace_factor: int
    formula_version: str = FORMULA_VERSION


def _diagnostic(code: str, message: str, path: Path | None = None) -> dict[str, Any]:
    return ResourceDiagnostic(
        code=code,
        message=message,
        path=str(path) if path is not None else None,
    ).as_dict()


def _default_profile(
    *, diagnostics: tuple[dict[str, Any], ...] = ()
) -> ResourceProfile:
    return ResourceProfile(diagnostics=diagnostics)


def _read_manifest(
    path: Path,
) -> tuple[dict[str, Any] | None, tuple[dict[str, Any], ...]]:
    try:
        with path.open("rb") as stream:
            return tomllib.load(stream), ()
    except tomllib.TOMLDecodeError as exc:
        return None, (
            _diagnostic(
                "RESOURCE_MANIFEST_PARSE_ERROR",
                f"invalid qpex.toml: {exc}",
                path,
            ),
        )
    except OSError as exc:
        return None, (
            _diagnostic(
                "RESOURCE_MANIFEST_NOT_FOUND",
                f"cannot read requested manifest: {exc}",
                path,
            ),
        )


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _manifest_path(manifest_path: Path | None, project_root: Path) -> Path:
    if manifest_path is not None:
        return Path(manifest_path)
    return Path(project_root) / "qpex.toml"


def _invalid_settings(
    *,
    term_limit: Any,
    binder_policy: Any,
    simulator_policy: Any,
    memory_limit: Any,
) -> bool:
    return (
        not _positive_int(term_limit)
        or term_limit > EMERGENCY_BINDER_TERM_LIMIT
        or binder_policy not in _POLICIES
        or simulator_policy not in _POLICIES
        or not _positive_int(memory_limit)
    )


def _settings_diagnostic(path: Path) -> ResourceProfile:
    return _default_profile(
        diagnostics=(
            _diagnostic(
                "RESOURCE_SETTING_INVALID",
                "resource limits must be positive, policies must be Warn or Abort, "
                "and binder term_limit must not exceed the emergency ceiling",
                path,
            ),
        )
    )


def load_resource_profile(
    manifest_path: Path | None,
    project_root: Path,
) -> ResourceProfile:
    """Load a manifest or return the versioned default profile.

    ``manifest_path`` is explicit when supplied. Otherwise only
    ``project_root / 'qpex.toml'`` is considered; parent directories are never
    searched implicitly.
    """

    path = _manifest_path(manifest_path, project_root)
    if not path.exists():
        if manifest_path is not None:
            return _default_profile(
                diagnostics=(
                    _diagnostic(
                        "RESOURCE_MANIFEST_NOT_FOUND",
                        "explicitly requested manifest does not exist",
                        path,
                    ),
                )
            )
        return _default_profile()

    raw, read_diagnostics = _read_manifest(path)
    if raw is None:
        return _default_profile(diagnostics=read_diagnostics)

    schema_version = raw.get("schema_version")
    if schema_version != RESOURCE_SCHEMA_VERSION:
        return _default_profile(
            diagnostics=(
                _diagnostic(
                    "RESOURCE_MANIFEST_SCHEMA_ERROR",
                    f"unsupported schema_version `{schema_version}`; expected {RESOURCE_SCHEMA_VERSION}",
                    path,
                ),
            )
        )

    resources = raw.get("resources", {})
    binder_raw = resources.get("binder", {}) if isinstance(resources, dict) else {}
    simulator_raw = resources.get("simulator", {}) if isinstance(resources, dict) else {}
    if not isinstance(binder_raw, dict) or not isinstance(simulator_raw, dict):
        return _settings_diagnostic(path)

    term_limit = binder_raw.get("term_limit", DEFAULT_BINDER_TERM_LIMIT)
    binder_policy = binder_raw.get("policy", "Abort")
    memory_limit = simulator_raw.get(
        "memory_limit_bytes", DEFAULT_SIMULATOR_MEMORY_LIMIT_BYTES
    )
    simulator_policy = simulator_raw.get("policy", "Abort")
    if _invalid_settings(
        term_limit=term_limit,
        binder_policy=binder_policy,
        simulator_policy=simulator_policy,
        memory_limit=memory_limit,
    ):
        return _settings_diagnostic(path)

    return ResourceProfile(
        schema_version=RESOURCE_SCHEMA_VERSION,
        binder=BinderExpansionBudget(term_limit=term_limit, policy=binder_policy),
        simulator=SimulatorResourceBudget(
            policy=simulator_policy,
            memory_limit_bytes=memory_limit,
        ),
    )


def estimate_simulator_resources(
    representation: str,
    *,
    logical_qubits: int,
) -> SimulationResourceEstimate:
    """Estimate storage using the representation-aware MVP formulas."""

    if not isinstance(logical_qubits, int) or logical_qubits < 0:
        raise ValueError("logical_qubits must be a non-negative integer")

    model = _ESTIMATE_MODELS.get(representation)
    if model is None:
        raise ValueError(f"unsupported simulator representation `{representation}`")
    dimension = model.dimension_base**logical_qubits

    return SimulationResourceEstimate(
        representation=representation,
        logical_qubits=logical_qubits,
        estimated_bytes=dimension * COMPLEX_F64_BYTES * model.workspace_factor,
        workspace_factor=model.workspace_factor,
    )
