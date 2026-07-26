"""Acceptance checks for LISS-0020 CPU-only physics coverage."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_CAPSTONE = _REPO / "examples/16_quantum_observatory"


def test_observatory_cpu_lane_uses_continuous_and_sparse_models() -> None:
    main = (_CAPSTONE / "cpu/continuous_models.qpex").read_text(encoding="utf-8")
    for form in (
        "Operator H_osc",
        "Operator H_grid",
        "Operator H_sparse",
        "wavepacket(",
        "trace_out(",
        "snapshot",
    ):
        assert form in main, f"CPU observatory missing continuous/diagnostic form: {form}"


def test_observatory_readme_explains_cpu_only_representation_boundaries() -> None:
    readme = (_CAPSTONE / "README.md").read_text(encoding="utf-8")
    for term in (
        "Fock",
        "position-grid",
        "sparse-Pauli",
        "trace_out",
        "snapshot",
        "CPU-only",
    ):
        assert term in readme, f"README missing CPU boundary explanation: {term}"


if __name__ == "__main__":
    import traceback

    tests = [
        test_observatory_cpu_lane_uses_continuous_and_sparse_models,
        test_observatory_readme_explains_cpu_only_representation_boundaries,
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
    print("OK — Quantum Observatory continuous-model coverage")
