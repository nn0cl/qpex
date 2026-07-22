"""Compiler pipeline: Lexer → Parser → Early Collapse → Typecheck."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_nodes import CompilationUnit
from .early_collapse import check_early_collapse
from .lexer import Lexer
from .parser import ParseError, Parser
from .typecheck import TypeChecker


@dataclass
class CompileResult:
    unit: CompilationUnit | None
    diagnostics: list[dict[str, Any]]
    checker: TypeChecker | None = None

    @property
    def ok(self) -> bool:
        hard = {"FORBIDDEN_KEYWORD", "EARLY_COLLAPSE_ERROR", "PARSE_ERROR", "LEX_ERROR", "TYPE_NOT_STATE"}
        return not any(d.get("code") in hard for d in self.diagnostics)


def compile_source(source: str) -> CompileResult:
    lexer = Lexer(source)
    tokens, lex_diags = lexer.tokenize()
    diags: list[dict[str, Any]] = list(lex_diags)

    unit: CompilationUnit | None = None
    checker: TypeChecker | None = None
    try:
        parser = Parser(tokens)
        unit = parser.parse()
        diags.extend(parser.diagnostics)
    except ParseError as e:
        diags.append(
            {
                "code": "PARSE_ERROR",
                "line": e.line,
                "col": e.col,
                "message": e.message,
            }
        )
        return CompileResult(unit=None, diagnostics=diags)

    diags.extend(check_early_collapse(unit))

    checker = TypeChecker()
    diags.extend(checker.check_unit(unit))

    return CompileResult(unit=unit, diagnostics=diags, checker=checker)


def analyze_source(source: str) -> list[dict[str, Any]]:
    """Drop-in for spec-verification compile_gate (same diagnostic dict shape)."""
    return compile_source(source).diagnostics
