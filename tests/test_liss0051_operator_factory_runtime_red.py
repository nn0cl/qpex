"""Regression tests for the remaining LISS-0051 operator lowering gap.

The official examples compile, but their linked ``Operator`` factory results
must be resolved before they are executed by the simulator.  These tests
cover all five specification cases that previously failed at runtime.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.run import run_path  # noqa: E402


_CASES = (
    (
        "SV-09/sv09-09-main_quantum_walk",
        "examples/09_complex_simulations/main_quantum_walk.qpex",
    ),
    (
        "SV-09/sv09-10-main_ssh_topological",
        "examples/10_topological_physics/main_ssh_topological.qpex",
    ),
    (
        "SV-09/sv09-15-main_orbital_mesh",
        "examples/15_orbital_mesh_walk/main_orbital_mesh.qpex",
    ),
    (
        "SV-09/sv09-16-main_observatory",
        "examples/16_quantum_observatory/main_observatory.qpex",
    ),
    (
        "SV-31/sv31-linked-run",
        "examples/09_complex_simulations/main_quantum_walk.qpex",
    ),
)


def test_remaining_operator_factory_examples_run_without_generic_call_failures() -> None:
    failures: list[str] = []

    for case_id, relative_path in _CASES:
        path = _REPO / relative_path
        try:
            result = run_path(path, seed=0, stdout=io.StringIO())
            if not result.compile_ok:
                failures.append(f"{case_id}: compile diagnostics={result.diagnostics}")
            elif result.eval.measure is None and not result.eval.joint.is_vacuum():
                failures.append(f"{case_id}: missing terminal measurement")
        except Exception as exc:  # noqa: BLE001 - expose the current runtime defect
            failures.append(f"{case_id}: {type(exc).__name__}: {exc}")

    assert not failures, "remaining operator factory Red cases:\n" + "\n".join(failures)


if __name__ == "__main__":
    test_remaining_operator_factory_examples_run_without_generic_call_failures()
    print("OK - remaining operator factory runtime cases")
