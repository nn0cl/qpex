"""Static CH0 OpenQASM subset emission and Fake independent parse port.

Additive backend adapter for the P0 CH0_COMMON_PHYSICAL portable artifact.
Does not import Semantic IR builders, engine packages, credentials, or
network clients. Parse success is not a physical-executability claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

OPENQASM_VERSION = "3.0"
SUBSET_ID = "CH0_STATIC_V1"
PROFILE_ID = "CH0_COMMON_PHYSICAL"
MAX_QUBITS = 5
ALLOWED_OPERATIONS = ("h", "x", "cx", "rz", "measure")
FORBIDDEN_FEATURES = ("dynamic", "timing", "subroutine")


@dataclass(frozen=True, slots=True)
class OpenQasmSubsetManifest:
    subset_id: str
    openqasm_version: str
    profile_id: str
    max_qubits: int
    allowed_operations: tuple[str, ...]
    forbidden_features: tuple[str, ...]
    supports_parameters: bool
    supports_measurement: bool


@dataclass(frozen=True, slots=True)
class Ch0EmitRequest:
    plan_id: str
    profile_id: str
    qubit_count: int
    operations: tuple[str, ...]
    parameters: tuple[tuple[str, str], ...]
    measurement_targets: tuple[str, ...]
    needs_dynamic: bool
    needs_timing: bool
    needs_subroutine: bool
    provenance_token: str


@dataclass(frozen=True, slots=True)
class EmitDiagnostic:
    code: str
    message: str
    source_span_token: str


@dataclass(frozen=True, slots=True)
class ParseReport:
    ok: bool
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class Ch0EmitResult:
    status: str
    qasm_text: str | None
    manifest: OpenQasmSubsetManifest
    diagnostics: tuple[EmitDiagnostic, ...]
    parse_ok: bool
    target_executable_claimed: bool
    measurement_targets: tuple[str, ...]
    parameters: tuple[tuple[str, str], ...]


class IndependentQasmParsePort(Protocol):
    def parse(self, text: str) -> ParseReport: ...


def load_ch0_manifest() -> OpenQasmSubsetManifest:
    return OpenQasmSubsetManifest(
        subset_id=SUBSET_ID,
        openqasm_version=OPENQASM_VERSION,
        profile_id=PROFILE_ID,
        max_qubits=MAX_QUBITS,
        allowed_operations=ALLOWED_OPERATIONS,
        forbidden_features=FORBIDDEN_FEATURES,
        supports_parameters=True,
        supports_measurement=True,
    )


def _diagnostic(code: str, message: str, source: str = "") -> EmitDiagnostic:
    return EmitDiagnostic(code=code, message=message, source_span_token=source)


def _reject(
    manifest: OpenQasmSubsetManifest,
    request: Ch0EmitRequest,
    diagnostics: tuple[EmitDiagnostic, ...],
) -> Ch0EmitResult:
    return Ch0EmitResult(
        status="rejected",
        qasm_text=None,
        manifest=manifest,
        diagnostics=diagnostics,
        parse_ok=False,
        target_executable_claimed=False,
        measurement_targets=request.measurement_targets,
        parameters=request.parameters,
    )


def _accept(
    manifest: OpenQasmSubsetManifest,
    request: Ch0EmitRequest,
    qasm_text: str,
) -> Ch0EmitResult:
    return Ch0EmitResult(
        status="accepted",
        qasm_text=qasm_text,
        manifest=manifest,
        diagnostics=(),
        parse_ok=True,
        target_executable_claimed=False,
        measurement_targets=request.measurement_targets,
        parameters=request.parameters,
    )


def _profile_and_shape_diagnostics(
    manifest: OpenQasmSubsetManifest,
    request: Ch0EmitRequest,
) -> list[EmitDiagnostic]:
    diagnostics: list[EmitDiagnostic] = []
    source = request.provenance_token
    if request.profile_id != manifest.profile_id:
        diagnostics.append(
            _diagnostic(
                "CH0_PROFILE_MISMATCH",
                f"profile {request.profile_id!r} is not {manifest.profile_id!r}",
                source,
            )
        )
    if not request.operations and not request.measurement_targets:
        diagnostics.append(
            _diagnostic(
                "CH0_EMPTY_PLAN",
                "empty plans cannot emit a success artifact",
                source,
            )
        )
    if request.qubit_count > manifest.max_qubits:
        diagnostics.append(
            _diagnostic(
                "CH0_QUBIT_BOUND",
                f"qubit_count {request.qubit_count} exceeds {manifest.max_qubits}",
                source,
            )
        )
    return diagnostics


def _operation_diagnostics(
    manifest: OpenQasmSubsetManifest,
    request: Ch0EmitRequest,
) -> list[EmitDiagnostic]:
    return [
        _diagnostic(
            "CH0_UNSUPPORTED_OPERATION",
            f"operation {operation!r} is outside the CH0 subset",
            f"{request.provenance_token}:{operation}",
        )
        for operation in request.operations
        if operation not in manifest.allowed_operations
    ]


def _deferred_feature_diagnostics(request: Ch0EmitRequest) -> list[EmitDiagnostic]:
    checks = (
        (request.needs_dynamic, "CH0_FORBIDDEN_DYNAMIC", "dynamic regions"),
        (request.needs_timing, "CH0_FORBIDDEN_TIMING", "timing/barriers"),
        (request.needs_subroutine, "CH0_FORBIDDEN_SUBROUTINE", "subroutine emission"),
    )
    return [
        _diagnostic(
            code,
            f"{label} are deferred outside the P0 CH0 package",
            request.provenance_token,
        )
        for enabled, code, label in checks
        if enabled
    ]


def _validate(
    manifest: OpenQasmSubsetManifest,
    request: Ch0EmitRequest,
) -> tuple[EmitDiagnostic, ...]:
    diagnostics = _profile_and_shape_diagnostics(manifest, request)
    diagnostics.extend(_operation_diagnostics(manifest, request))
    diagnostics.extend(_deferred_feature_diagnostics(request))
    return tuple(diagnostics)


def _render_header(manifest: OpenQasmSubsetManifest, request: Ch0EmitRequest) -> list[str]:
    lines = [
        f"OPENQASM {manifest.openqasm_version};",
        f"// subset {manifest.subset_id}",
        f"// profile {manifest.profile_id}",
        f"// plan {request.plan_id}",
        'include "stdgates.inc";',
        f"qubit[{request.qubit_count}] q;",
    ]
    if request.measurement_targets:
        lines.append(f"bit[{len(request.measurement_targets)}] c;")
    return lines


def _render_parameters(request: Ch0EmitRequest) -> list[str]:
    lines: list[str] = []
    for name, value in request.parameters:
        lines.append(f"input float[64] {name}; // = {value}")
        lines.append(f"// param {name}={value}")
    return lines


def _render_operations(request: Ch0EmitRequest) -> list[str]:
    lines: list[str] = []
    qubit_ops = [operation for operation in request.operations if operation != "measure"]
    for index, operation in enumerate(qubit_ops):
        if operation == "cx" and request.qubit_count >= 2:
            lines.append("cx q[0], q[1];")
        elif operation == "rz":
            lines.append("rz(theta) q[0];" if request.parameters else "rz(0.0) q[0];")
        else:
            target = index % max(request.qubit_count, 1)
            lines.append(f"{operation} q[{target}];")
    return lines


def _render_measurements(request: Ch0EmitRequest) -> list[str]:
    if "measure" not in request.operations and not request.measurement_targets:
        return []
    lines: list[str] = []
    for bit_index, classical in enumerate(request.measurement_targets):
        qubit_index = min(bit_index, max(request.qubit_count - 1, 0))
        lines.append(f"c[{bit_index}] = measure q[{qubit_index}]; // {classical}")
        lines.append(f"// measure-target {classical}")
    return lines


def _render_qasm(manifest: OpenQasmSubsetManifest, request: Ch0EmitRequest) -> str:
    lines = _render_header(manifest, request)
    lines.extend(_render_parameters(request))
    lines.extend(_render_operations(request))
    lines.extend(_render_measurements(request))
    return "\n".join(lines) + "\n"


class FakeIndependentQasmParser:
    """Structural Fake parse port for CH0 success artifacts."""

    def parse(self, text: str) -> ParseReport:
        if not text.strip():
            return ParseReport(
                ok=False,
                code="CH0_PARSE_EMPTY",
                message="empty OpenQASM text is not a success artifact",
            )
        if f"OPENQASM {OPENQASM_VERSION};" not in text:
            return ParseReport(
                ok=False,
                code="CH0_PARSE_HEADER",
                message="missing declared OPENQASM header",
            )
        return ParseReport(ok=True, code="CH0_PARSE_OK", message="structural ok")


def emit_ch0(
    request: Ch0EmitRequest,
    *,
    parser: IndependentQasmParsePort | None = None,
) -> Ch0EmitResult:
    manifest = load_ch0_manifest()
    diagnostics = _validate(manifest, request)
    if diagnostics:
        return _reject(manifest, request, diagnostics)

    active_parser = parser if parser is not None else FakeIndependentQasmParser()
    qasm_text = _render_qasm(manifest, request)
    parse_report = active_parser.parse(qasm_text)
    if not parse_report.ok:
        return _reject(
            manifest,
            request,
            (
                _diagnostic(
                    parse_report.code,
                    parse_report.message,
                    request.provenance_token,
                ),
            ),
        )
    return _accept(manifest, request, qasm_text)
