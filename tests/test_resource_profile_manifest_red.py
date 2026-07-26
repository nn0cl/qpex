"""AT-TDD Phase 1 Red tests for LISS-0062.

The resource-profile boundary is intentionally absent until Phase 2 Green.
These tests define the user-visible manifest defaults, validation diagnostics,
and representation-aware simulator estimates without implementing TOML or
changing the Kernel.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _resource_api():
    try:
        from compiler.qpex.resource_profile import (  # type: ignore[import-not-found]
            estimate_simulator_resources,
            load_resource_profile,
        )
    except ModuleNotFoundError as exc:
        raise AssertionError(
            "LISS-0062 Phase 2 resource_profile boundary is not implemented"
        ) from exc
    return load_resource_profile, estimate_simulator_resources


def test_missing_manifest_uses_versioned_defaults(tmp_path: Path) -> None:
    load_resource_profile, _ = _resource_api()
    profile = load_resource_profile(None, tmp_path)

    assert profile.schema_version == 1
    assert profile.binder.term_limit == 100_000
    assert profile.binder.policy == "Abort"
    assert profile.simulator.policy == "Abort"


def test_qpex_manifest_loads_an_immutable_profile(tmp_path: Path) -> None:
    load_resource_profile, _ = _resource_api()
    (tmp_path / "qpex.toml").write_text(
        """schema_version = 1

[resources.binder]
term_limit = 50_000
policy = "Abort"

[resources.simulator]
policy = "Warn"
memory_limit_bytes = 8_589_934_592
""",
        encoding="utf-8",
    )

    profile = load_resource_profile(None, tmp_path)

    assert profile.binder.term_limit == 50_000
    assert profile.simulator.policy == "Warn"
    assert profile.simulator.memory_limit_bytes == 8_589_934_592


def test_unknown_manifest_schema_is_a_hard_configuration_diagnostic(tmp_path: Path) -> None:
    load_resource_profile, _ = _resource_api()
    manifest = tmp_path / "unsupported.toml"
    manifest.write_text("schema_version = 99\n", encoding="utf-8")

    result = load_resource_profile(manifest, tmp_path)

    assert any(d["code"] == "RESOURCE_MANIFEST_SCHEMA_ERROR" for d in result.diagnostics)


def test_simulator_estimate_records_representation_and_formula_version(
    tmp_path: Path,
) -> None:
    _, estimate_simulator_resources = _resource_api()
    state_vector = estimate_simulator_resources("StateVector", logical_qubits=3)
    density = estimate_simulator_resources("DensityState", logical_qubits=3)
    lindblad = estimate_simulator_resources("LindbladRK4", logical_qubits=3)

    assert state_vector.estimated_bytes == 2**3 * 16 * 3
    assert density.estimated_bytes == 4**3 * 16 * 3
    assert lindblad.estimated_bytes == 4**3 * 16 * 6
    assert state_vector.formula_version == density.formula_version == lindblad.formula_version


if __name__ == "__main__":
    import tempfile

    tests = [
        test_missing_manifest_uses_versioned_defaults,
        test_qpex_manifest_loads_an_immutable_profile,
        test_unknown_manifest_schema_is_a_hard_configuration_diagnostic,
        test_simulator_estimate_records_representation_and_formula_version,
    ]
    passed, failed = 0, 0
    for test in tests:
        try:
            with tempfile.TemporaryDirectory() as directory:
                test(Path(directory))
            passed += 1
        except Exception as exc:  # noqa: BLE001 -- Red run report only
            failed += 1
            print(f"RED (expected): {test.__name__}: {type(exc).__name__}: {exc}")
    print(f"\n{passed} passed, {failed} failed (LISS-0062 Phase 1 Red)")
