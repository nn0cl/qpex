"""QPex token kinds (ADR 0035)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenKind(Enum):
    # Active keywords
    CLASS = auto()
    INTERFACE = auto()
    PACKAGE = auto()
    IMPORT = auto()
    FUN = auto()
    STATE = auto()
    LET = auto()
    WHEN = auto()
    COIN = auto()
    DIRAC = auto()
    VACUUM = auto()
    EVOLVE = auto()
    MEASURE = auto()
    SNAPSHOT = auto()
    INSPECT = auto()

    # Contextual (parser soft keywords)
    ELSE = auto()
    PUBLIC = auto()
    TRUE = auto()
    FALSE = auto()
    TO = auto()

    # Forbidden (hard error — still emitted so diagnostics have spans)
    FORBIDDEN = auto()

    # Retired (linter / fix-it)
    RETIRED = auto()

    # Literals / idents / ops
    IDENT = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()

    PIPE_OP = auto()  # |>

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQ = auto()
    EQEQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()
    ARROW = auto()  # ->

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    DOT = auto()
    COLON = auto()
    SEMI = auto()

    EOF = auto()
    ERROR = auto()


ACTIVE: dict[str, TokenKind] = {
    "class": TokenKind.CLASS,
    "interface": TokenKind.INTERFACE,
    "package": TokenKind.PACKAGE,
    "import": TokenKind.IMPORT,
    "fun": TokenKind.FUN,
    "state": TokenKind.STATE,
    "let": TokenKind.LET,
    "when": TokenKind.WHEN,
    "coin": TokenKind.COIN,
    "dirac": TokenKind.DIRAC,
    "vacuum": TokenKind.VACUUM,
    "evolve": TokenKind.EVOLVE,
    "measure": TokenKind.MEASURE,
    "snapshot": TokenKind.SNAPSHOT,
    "inspect": TokenKind.INSPECT,
}

CONTEXTUAL: dict[str, TokenKind] = {
    "else": TokenKind.ELSE,
    "public": TokenKind.PUBLIC,
    "true": TokenKind.TRUE,
    "false": TokenKind.FALSE,
    "to": TokenKind.TO,
}

FORBIDDEN: set[str] = {
    "if",
    "switch",
    "while",
    "for",
    "break",
    "return",
    "new",
    "null",
    "try",
    "catch",
    "throw",
    "Thread",
    "async",
    "await",
}

RETIRED: dict[str, str] = {
    "observe": "measure",
    "span": "when",
    "fn": "fun",
    "trait": "interface",
}

FORBIDDEN_MESSAGES: dict[str, str] = {
    "if": "Syntax Error: 'if' is forbidden in QPex. Use 'when' for state superposition.",
    "switch": "Syntax Error: 'switch' is forbidden in QPex. Use 'when' for state superposition.",
    "while": "Syntax Error: 'while' is forbidden in QPex. Use 'evolve' for pure iteration.",
    "for": "Syntax Error: 'for' is forbidden in QPex. Use 'evolve' for pure iteration.",
    "break": "Syntax Error: 'break' is forbidden; early exit tears the joint.",
    "return": "Syntax Error: 'return' is forbidden; use block result / evolve.",
    "new": "Syntax Error: Construct with Foo(args); 'new' is forbidden.",
    "null": "Syntax Error: Use Result / when basis labels / Vacuum; 'null' is forbidden.",
    "try": "Syntax Error: Exceptions are forbidden; use Result + when / project.",
    "catch": "Syntax Error: Exceptions are forbidden; use Result + when / project.",
    "throw": "Syntax Error: Exceptions are forbidden; use Result + when / project.",
    "Thread": "Syntax Error: Concurrency is when / joint product; threads are forbidden.",
    "async": "Syntax Error: Concurrency is when / joint product; async is forbidden.",
    "await": "Syntax Error: Concurrency is when / joint product; await is forbidden.",
}


@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    lexeme: str
    line: int
    col: int
    literal: Any = None
    meta: dict[str, str] | None = None  # e.g. replacement for RETIRED
