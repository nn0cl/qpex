"""OpenQASM emit — delegates to Phase 4.1 QASM3Emitter (ADR 0036)."""

from __future__ import annotations

from ..ast_nodes import CompilationUnit
from ..backend.qasm import EmitResult, emit_openqasm3 as _backend_emit

__all__ = ["EmitResult", "emit_openqasm3"]


def emit_openqasm3(unit: CompilationUnit, **kwargs) -> EmitResult:
    return _backend_emit(unit, **kwargs)
