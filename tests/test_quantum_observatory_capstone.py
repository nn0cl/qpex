"""AT-TDD Phase 1 Red tests for LISS-0020 Quantum Observatory.

These tests intentionally fail until the capstone example and its catalog
integration are implemented. Phase 1 contains no production or example code.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))
_SV_ROOT = _REPO / "tests/spec_verification"
if str(_SV_ROOT) not in sys.path:
    sys.path.insert(0, str(_SV_ROOT))

from compiler.qpex.codegen_qasm import QPexCompiler  # noqa: E402
from compiler.qpex.pipeline import compile_path  # noqa: E402
from compiler.qpex.run import run_path  # noqa: E402
from tests.spec_verification.suites.sv09_examples import EXAMPLES  # noqa: E402


_CAPSTONE = _REPO / "examples/16_quantum_observatory"
_ENTRY = _CAPSTONE / "main_observatory.qpex"
_QPU_ENTRY = _CAPSTONE / "qpu/portable_observatory_link.qpex"


def test_capstone_module_graph_and_readmes_exist() -> None:
    expected = [
        _CAPSTONE / "README.md",
        _CAPSTONE / "domain/observatory_config.qpex",
        _CAPSTONE / "domain/topology.qpex",
        _CAPSTONE / "domain/link_parties.qpex",
        _CAPSTONE / "operators/ssh_hamiltonian.qpex",
        _CAPSTONE / "operators/interferometer.qpex",
        _CAPSTONE / "operators/walk_step.qpex",
        _CAPSTONE / "operators/search_oracle.qpex",
        _CAPSTONE / "operators/bell_channel.qpex",
        _ENTRY,
        _QPU_ENTRY,
    ]
    missing = [str(path.relative_to(_REPO)) for path in expected if not path.is_file()]
    assert not missing, f"missing capstone module graph: {missing}"


def test_capstone_is_registered_as_an_official_example() -> None:
    assert ("16_quantum_observatory", "main_observatory.qpex") in EXAMPLES


def test_capstone_cpu_entry_compiles_and_reaches_terminal_measure() -> None:
    compiled = compile_path(_ENTRY)
    assert compiled.ok, compiled.diagnostics

    result = run_path(_ENTRY, seed=0, stdout=io.StringIO())
    assert result.compile_ok, result.diagnostics
    assert result.eval.measure is not None or result.eval.joint.is_vacuum()


def test_capstone_qpu_lane_emits_portable_openqasm3() -> None:
    qasm = QPexCompiler(route=True).compile_to_qasm3(str(_QPU_ENTRY))
    assert qasm.startswith("OPENQASM 3.0;")
    assert 'include "stdgates.inc";' in qasm
    assert "qubit[" in qasm
    assert "measure" in qasm
    assert "braket" not in qasm.lower()
    assert "qiskit" not in qasm.lower()


def test_capstone_readme_contains_surface_coverage_and_deferred_honesty() -> None:
    readme = (_CAPSTONE / "README.md").read_text(encoding="utf-8")
    for term in (
        "Coverage matrix",
        "State<T>",
        "namespace",
        "evolve under H",
        "OpenQASM",
        "QFT",
        "Lindblad",
        "until",
        "currying",
        "Suzuki",
    ):
        assert term in readme, f"README missing coverage/honesty term: {term}"


if __name__ == "__main__":
    import traceback

    tests = [
        test_capstone_module_graph_and_readmes_exist,
        test_capstone_is_registered_as_an_official_example,
        test_capstone_cpu_entry_compiles_and_reaches_terminal_measure,
        test_capstone_qpu_lane_emits_portable_openqasm3,
        test_capstone_readme_contains_surface_coverage_and_deferred_honesty,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception:  # noqa: BLE001 - simple standalone test runner
            failures += 1
            traceback.print_exc()
    if failures:
        raise SystemExit(f"{failures}/{len(tests)} Phase 1 Red tests failed")
    print("OK — Quantum Observatory capstone")
