"""Phase 2 Green checks for the immutable QPU IR lowering slice."""

from compiler.qpex.backend.qasm.emitter import QASM3Emitter
from compiler.qpex.pipeline import compile_source


def test_openqasm_adapter_consumes_qpu_ir_in_memory() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            QubitRegister<1> reg = system()
            forEach q in reg {
                apply(H, q)
            }
            State<Int> observed = coin()
            measure observed
        }
        """
    )
    assert compiled.ok, compiled.diagnostics

    emitted = QASM3Emitter(route=False).emit_qpu_program(compiled.qpu_ir)
    assert emitted.ok, emitted.notes
    assert "h q[0];" in emitted.qasm
    assert "measure q[0]" in emitted.qasm


def test_qpu_program_root_is_immutable_and_preserves_node_provenance() -> None:
    compiled = compile_source(
        """
        package t
        pub fn main() -> Unit {
            QubitRegister<1> reg = system()
            forEach q in reg {
                apply(H, q)
            }
            State<Int> observed = coin()
            measure observed
        }
        """
    )
    assert compiled.ok
    program = compiled.qpu_ir
    assert type(program).__name__ == "QpuProgram"
    assert program["instructions"][0].provenance["source"] == "forEach.apply"

