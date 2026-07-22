"""AT-TDD: OpenQASM 3.0 codegen (`OpenQASM3Generator` / `QPexCompiler`)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.codegen_qasm import OpenQASM3Generator, QPexCompiler  # noqa: E402
from compiler.qpex.pipeline import compile_source  # noqa: E402


def _assert_valid_qasm3(text: str) -> None:
    assert "OPENQASM 3.0;" in text
    assert 'include "stdgates.inc";' in text
    assert re.search(r"qubit\[\d+\]\s+q;", text)
    assert re.search(r"bit\[\d+\]\s+c;", text)
    assert "measure" in text
    # No vendor SDKs leaked into output
    assert "braket" not in text.lower()
    assert "qiskit" not in text.lower()


def test_portable_bell_via_compiler() -> None:
    path = _REPO / "examples/03_quantum_information/portable_bell_qpu.qpex"
    qasm = QPexCompiler().compile_to_qasm3(str(path))
    _assert_valid_qasm3(qasm)
    assert "h q[" in qasm
    assert "cx q[" in qasm
    assert "c[0] = measure q[" in qasm


def test_generator_from_unit() -> None:
    src = """
package t
public fun main() {
  state a = |+>
  state b = |0>
  state b = cnot(a, b)
  measure b
}
"""
    compiled = compile_source(src)
    assert compiled.ok and compiled.unit is not None
    qasm = OpenQASM3Generator(route=False).generate(compiled.unit)
    _assert_valid_qasm3(qasm)
    assert qasm.startswith("OPENQASM 3.0;")


def test_apply_and_capply_gates() -> None:
    src = """
package t
public fun main() {
  state q = |0>
  state q = apply(X, q)
  state q = apply(Y, q)
  state q = apply(Z, q)
  state q = apply(H, q)
  state t = |0>
  state t = capply(q, X, t)
  state t = capply(q, Z, t)
  measure t
}
"""
    compiled = compile_source(src)
    assert compiled.ok and compiled.unit is not None, compiled.diagnostics
    qasm = OpenQASM3Generator(route=False).generate(compiled.unit)
    _assert_valid_qasm3(qasm)
    assert "x q[" in qasm
    assert "y q[" in qasm
    assert "z q[" in qasm
    assert "h q[" in qasm
    assert "cx q[" in qasm
    assert "cz q[" in qasm


def test_bell_example_file_roundtrip() -> None:
    path = _REPO / "examples/03_quantum_information/bell_state.qpex"
    qasm = QPexCompiler(route=True).compile_to_qasm3(str(path))
    _assert_valid_qasm3(qasm)


def test_stdlib_only_module() -> None:
    import ast
    from pathlib import Path

    import compiler.qpex.codegen_qasm as mod

    tree = ast.parse(Path(mod.__file__).read_text(encoding="utf-8"))
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.extend(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.append(node.module.split(".")[0])
    # Relative package imports only (compiler.qpex.*); ban vendor SDKs
    forbidden = {"braket", "qiskit", "amazon", "cirq", "pennylane"}
    assert not (forbidden & set(imported)), imported


if __name__ == "__main__":
    test_portable_bell_via_compiler()
    test_generator_from_unit()
    test_apply_and_capply_gates()
    test_bell_example_file_roundtrip()
    test_stdlib_only_module()
    print("OK — OpenQASM 3 codegen")
