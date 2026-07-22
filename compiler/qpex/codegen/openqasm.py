"""OpenQASM emit — ADR 0036 CLI path.

Prefer `compiler.qpex.codegen_qasm.OpenQASM3Generator` /
`QPexCompiler.compile_to_qasm3` for the public AT-TDD API.
"""

from __future__ import annotations

from ..ast_nodes import CompilationUnit
from ..backend.qasm import EmitResult, emit_openqasm3 as _backend_emit

__all__ = ["EmitResult", "emit_openqasm3"]


def emit_openqasm3(unit: CompilationUnit, **kwargs) -> EmitResult:
    return _backend_emit(unit, **kwargs)
