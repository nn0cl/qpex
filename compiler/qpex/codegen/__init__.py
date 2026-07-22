"""Codegen backends (OpenQASM / future QIR)."""

from .openqasm import EmitResult, emit_openqasm3

__all__ = ["EmitResult", "emit_openqasm3"]
