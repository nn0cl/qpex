"""AT-TDD Phase 1 Red: LISS-0097 P0 static CH0 OpenQASM contract.

One suite covers subset manifest, fail-closed emission, parameters,
measurement metadata, Fake independent parse, deferred-feature rejection,
and isolation from Semantic IR / simulator fallback / SDKs. Dynamic,
timing, subroutine emission, and third-party parsers are out of scope.
"""

from __future__ import annotations

from pathlib import Path
import sys

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _load_api():
    from compiler.staqex.backend.qasm.ch0_emit import (
        Ch0EmitRequest,
        Ch0EmitResult,
        EmitDiagnostic,
        FakeIndependentQasmParser,
        OpenQasmSubsetManifest,
        emit_ch0,
        load_ch0_manifest,
    )

    return locals()


def _request(
    api,
    *,
    plan_id: str = "plan.ch0.bell",
    qubits: int = 2,
    operations: tuple[str, ...] = ("h", "cx", "measure"),
    parameters: tuple[tuple[str, str], ...] = (("theta", "0.0"),),
    measurement_targets: tuple[str, ...] = ("c0",),
    needs_dynamic: bool = False,
    needs_timing: bool = False,
    needs_subroutine: bool = False,
    provenance: str = "verified-semantic-projection",
):
    return api["Ch0EmitRequest"](
        plan_id=plan_id,
        profile_id="CH0_COMMON_PHYSICAL",
        qubit_count=qubits,
        operations=operations,
        parameters=parameters,
        measurement_targets=measurement_targets,
        needs_dynamic=needs_dynamic,
        needs_timing=needs_timing,
        needs_subroutine=needs_subroutine,
        provenance_token=provenance,
    )


def _codes(result) -> set[str]:
    return {diagnostic.code for diagnostic in result.diagnostics}


def test_manifest_declares_version_subset_and_bounds() -> None:
    api = _load_api()
    manifest = api["load_ch0_manifest"]()

    assert isinstance(manifest, api["OpenQasmSubsetManifest"])
    assert manifest.subset_id == "CH0_STATIC_V1"
    assert manifest.openqasm_version  # explicit declared version string
    assert manifest.profile_id == "CH0_COMMON_PHYSICAL"
    assert manifest.max_qubits >= 2
    assert manifest.allowed_operations
    assert "dynamic" in manifest.forbidden_features
    assert "timing" in manifest.forbidden_features
    assert "subroutine" in manifest.forbidden_features


def test_emit_accepts_bounded_static_ch0_plan() -> None:
    api = _load_api()
    result = api["emit_ch0"](_request(api), parser=api["FakeIndependentQasmParser"]())

    assert isinstance(result, api["Ch0EmitResult"])
    assert result.status == "accepted"
    assert result.qasm_text is not None
    assert result.qasm_text.strip() != ""
    assert result.manifest.subset_id == "CH0_STATIC_V1"
    assert result.manifest.openqasm_version in result.qasm_text
    assert result.parse_ok is True
    assert result.target_executable_claimed is False


def test_empty_plan_rejects_without_empty_program() -> None:
    api = _load_api()
    result = api["emit_ch0"](
        _request(api, plan_id="plan.empty", operations=(), measurement_targets=()),
        parser=api["FakeIndependentQasmParser"](),
    )

    assert result.status == "rejected"
    assert result.qasm_text is None
    assert "CH0_EMPTY_PLAN" in _codes(result)
    assert all(isinstance(item, api["EmitDiagnostic"]) for item in result.diagnostics)


def test_over_bound_qubits_reject_fail_closed() -> None:
    api = _load_api()
    manifest = api["load_ch0_manifest"]()
    result = api["emit_ch0"](
        _request(api, qubits=manifest.max_qubits + 1),
        parser=api["FakeIndependentQasmParser"](),
    )

    assert result.status == "rejected"
    assert result.qasm_text is None
    assert "CH0_QUBIT_BOUND" in _codes(result)


def test_unsupported_operation_rejects_with_source_linked_diagnostic() -> None:
    api = _load_api()
    result = api["emit_ch0"](
        _request(api, operations=("h", "magic_gate", "measure")),
        parser=api["FakeIndependentQasmParser"](),
    )

    assert result.status == "rejected"
    assert result.qasm_text is None
    assert "CH0_UNSUPPORTED_OPERATION" in _codes(result)
    diagnostic = next(
        item for item in result.diagnostics if item.code == "CH0_UNSUPPORTED_OPERATION"
    )
    assert diagnostic.source_span_token  # non-empty provenance link


def test_parameters_and_measurement_metadata_appear_in_success_artifact() -> None:
    api = _load_api()
    result = api["emit_ch0"](
        _request(
            api,
            parameters=(("theta", "1.25"), ("phi", "0.5")),
            measurement_targets=("c0", "c1"),
        ),
        parser=api["FakeIndependentQasmParser"](),
    )

    assert result.status == "accepted"
    text = result.qasm_text
    assert "theta" in text and "1.25" in text
    assert "phi" in text and "0.5" in text
    assert "measure" in text.lower()
    assert "c0" in text and "c1" in text
    assert result.measurement_targets == ("c0", "c1")
    assert result.parameters == (("theta", "1.25"), ("phi", "0.5"))


def test_fake_parser_accepts_success_and_rejects_empty() -> None:
    api = _load_api()
    parser = api["FakeIndependentQasmParser"]()
    accepted = api["emit_ch0"](_request(api), parser=parser)
    assert accepted.parse_ok is True
    assert parser.parse(accepted.qasm_text).ok is True

    empty = parser.parse("")
    assert empty.ok is False
    assert empty.code == "CH0_PARSE_EMPTY"


def test_deferred_dynamic_timing_subroutine_reject_without_emission() -> None:
    api = _load_api()
    parser = api["FakeIndependentQasmParser"]()

    dynamic = api["emit_ch0"](_request(api, needs_dynamic=True), parser=parser)
    assert dynamic.status == "rejected"
    assert dynamic.qasm_text is None
    assert "CH0_FORBIDDEN_DYNAMIC" in _codes(dynamic)

    timing = api["emit_ch0"](_request(api, needs_timing=True), parser=parser)
    assert timing.status == "rejected"
    assert timing.qasm_text is None
    assert "CH0_FORBIDDEN_TIMING" in _codes(timing)

    subroutine = api["emit_ch0"](_request(api, needs_subroutine=True), parser=parser)
    assert subroutine.status == "rejected"
    assert subroutine.qasm_text is None
    assert "CH0_FORBIDDEN_SUBROUTINE" in _codes(subroutine)


def test_module_does_not_fallback_to_simulator_or_import_sdks() -> None:
    api = _load_api()
    import compiler.staqex.backend.qasm.ch0_emit as mod

    text = Path(mod.__file__).read_text(encoding="utf-8")
    forbidden = (
        "simulator_port",
        "quantum_semantic_ir",
        "physics_ir",
        "qiskit",
        "cirq",
        "pennylane",
        "provider",
    )
    for token in forbidden:
        assert token not in text, token
    assert api["emit_ch0"] is not None


def test_wrong_profile_rejects_without_silent_degrade() -> None:
    api = _load_api()
    request = api["Ch0EmitRequest"](
        plan_id="plan.wrong-profile",
        profile_id="SIM0_EXACT",
        qubit_count=2,
        operations=("h", "measure"),
        parameters=(),
        measurement_targets=("c0",),
        needs_dynamic=False,
        needs_timing=False,
        needs_subroutine=False,
        provenance_token="verified-semantic-projection",
    )
    result = api["emit_ch0"](request, parser=api["FakeIndependentQasmParser"]())

    assert result.status == "rejected"
    assert result.qasm_text is None
    assert "CH0_PROFILE_MISMATCH" in _codes(result)


if __name__ == "__main__":
    tests = tuple(
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    )
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
    print(
        f"LISS-0097 CH0 integrated Red: {len(tests) - failures} passed, {failures} failed"
    )
    raise SystemExit(1 if failures else 0)
