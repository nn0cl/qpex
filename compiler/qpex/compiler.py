"""Stable import path for `QPexCompiler` (LISS-0002 / inbound file list).

Implementation lives in `codegen_qasm.py`; this module is a thin re-export so
agents and docs can use `from compiler.qpex.compiler import QPexCompiler`.
"""

from __future__ import annotations

from .codegen_qasm import OpenQASM3Generator, QPexCompiler, generate_openqasm3

__all__ = ["OpenQASM3Generator", "QPexCompiler", "generate_openqasm3"]
