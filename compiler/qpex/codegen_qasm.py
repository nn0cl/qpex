"""OpenQASM 3.0 codegen facade (Python standard library only).

Public API requested by AT-TDD:
  - `OpenQASM3Generator` — typed AST / CompilationUnit → OpenQASM 3.0 text
  - `QPexCompiler.compile_to_qasm3(path)` — file → QASM string

Lowering reuses the existing Phase 4.1 QPU backend (`backend.qasm`) so SV-10/11
and CLI `emit-qasm` stay consistent. No third-party quantum SDKs are imported.
"""

from __future__ import annotations

from pathlib import Path

from .ast_nodes import CompilationUnit
from .backend.qasm import EmitResult, QASM3Emitter, emit_openqasm3
from .pipeline import compile_path, compile_source


class OpenQASM3Generator:
    """Convert a type-checked QPex compilation unit into OpenQASM 3.0 text."""

    def __init__(self, *, topology: str = "linear", route: bool = True) -> None:
        self.topology = topology
        self.route = route

    def generate(self, unit: CompilationUnit) -> str:
        """Emit OpenQASM 3.0 for `unit` (header, registers, gates, measure)."""
        result = self.generate_detailed(unit)
        if not result.ok:
            raise RuntimeError("OpenQASM 3 emission failed")
        text = result.qasm
        return text if text.endswith("\n") else text + "\n"

    def generate_detailed(self, unit: CompilationUnit) -> EmitResult:
        return QASM3Emitter(topology=self.topology, route=self.route).emit_unit(unit)

    def generate_from_source(self, source: str) -> str:
        compiled = compile_source(source)
        if not compiled.ok or compiled.unit is None:
            codes = [d.get("code") for d in compiled.diagnostics]
            raise ValueError(f"QPex compile failed before QASM emit: {codes}")
        return self.generate(compiled.unit)


class QPexCompiler:
    """Thin compiler entry for path-based QASM export."""

    def __init__(self, *, topology: str = "linear", route: bool = True) -> None:
        self._gen = OpenQASM3Generator(topology=topology, route=route)

    def compile_to_qasm3(self, file_path: str) -> str:
        """Compile `file_path` (typecheck + lower) to an OpenQASM 3.0 string."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"QPex source not found: {file_path}")
        compiled = compile_path(path)
        if not compiled.ok or compiled.unit is None:
            codes = [d.get("code") for d in compiled.diagnostics]
            raise ValueError(
                f"QPex compile failed for `{file_path}` before QASM emit: {codes}"
            )
        return self._gen.generate(compiled.unit)


def generate_openqasm3(unit: CompilationUnit, **kwargs) -> str:
    """Convenience wrapper used by CLI / tests."""
    return OpenQASM3Generator(**kwargs).generate(unit)


__all__ = [
    "EmitResult",
    "OpenQASM3Generator",
    "QPexCompiler",
    "emit_openqasm3",
    "generate_openqasm3",
]
