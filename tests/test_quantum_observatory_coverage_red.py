"""AT-TDD Phase 1 Red: remaining shipped-surface coverage for LISS-0020.

The assertions are intentionally ahead of the current Green slice. They define
the next modular example increment without changing production or example
source during Phase 1.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_CAPSTONE = _REPO / "examples/16_quantum_observatory"


def _source(relative: str) -> str:
    return (_CAPSTONE / relative).read_text(encoding="utf-8")


def test_cpu_narrative_uses_state_algebra_and_non_destructive_diagnostics() -> None:
    main = _source("main_observatory.qpex")
    for form in ("when", "map(", "project(", "interfer(", "snapshot"):
        assert form in main, f"capstone CPU narrative missing implemented form: {form}"


def test_instrument_modules_use_distinct_shipped_physics_operations() -> None:
    expected = {
        "operators/interferometer.qpex": ("interfer(", "phase("),
        "operators/walk_step.qpex": ("walk_shift", "apply("),
        "operators/search_oracle.qpex": ("diffuse", "phase("),
        "operators/bell_channel.qpex": ("capply(", "ocapply("),
    }
    for relative, forms in expected.items():
        source = _source(relative)
        for form in forms:
            assert form in source, f"{relative} missing implemented operation: {form}"


def test_capstone_documents_cpu_only_continuous_models_and_reused_examples() -> None:
    readme = _source("README.md")
    for reference in (
        "examples/05_harmonic_oscillator/quantum_oscillator.qpex",
        "examples/05_harmonic_oscillator/grid_oscillator.qpex",
        "examples/06_statistical_physics/quantum_ising_4.qpex",
        "Fock",
        "grid",
        "CPU-only",
    ):
        assert reference in readme, f"README missing model boundary: {reference}"


def test_cpu_control_surface_covers_open_and_mixed_control_variants() -> None:
    main = _source("main_observatory.qpex")
    for form in ("capply(", "ocapply(", "!", "toffoli"):
        assert form in main, f"capstone CPU narrative missing control form: {form}"


def test_capstone_kitchen_sink_covers_newly_approved_language_surfaces() -> None:
    """Phase 1 contract for the next all-in-one teaching narrative."""
    main = _source("main_observatory.qpex")
    expected_forms = (
        "interface Evolvable<T>",
        "impl Evolvable<Float> for",
        "|>",
        "QubitRegister<3>",
        "Param<Angle>",
        "using Suzuki(order = 2, steps = 8)",
        "using Suzuki(order = 2, tolerance = 1e-4, error = EmpiricalEstimate)",
        "qft(",
        "iqft(",
        "DensityState<Qubit>",
        "JumpSet([RawMatrix(",
        "measure ",
    )
    for form in expected_forms:
        assert form in main, f"capstone kitchen-sink surface missing: {form}"


def test_capstone_kitchen_sink_keeps_one_terminal_measurement_boundary() -> None:
    main = _source("main_observatory.qpex")
    assert main.count("measure ") == 1
    assert main.rstrip().endswith("measure observed\n}")


if __name__ == "__main__":
    import traceback

    tests = [
        test_cpu_narrative_uses_state_algebra_and_non_destructive_diagnostics,
        test_instrument_modules_use_distinct_shipped_physics_operations,
        test_capstone_documents_cpu_only_continuous_models_and_reused_examples,
        test_cpu_control_surface_covers_open_and_mixed_control_variants,
        test_capstone_kitchen_sink_covers_newly_approved_language_surfaces,
        test_capstone_kitchen_sink_keeps_one_terminal_measurement_boundary,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception:  # noqa: BLE001 - standalone Phase 1 runner
            failures += 1
            traceback.print_exc()
    if failures:
        raise SystemExit(f"{failures}/{len(tests)} Phase 1 Red tests failed")
    print("OK — Quantum Observatory coverage slice")
