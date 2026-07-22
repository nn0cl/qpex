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
    FOR = auto()
    TO = auto()
    TIMES = auto()
    UNDER = auto()

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
    TENSOR_OP = auto()  # *|*
    CARET = auto()  # ^
    KET = auto()  # |0>, |+>, |01>, …

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    EQ = auto()
    EQEQ = auto()
    NEQ = auto()
    BANG = auto()  # !  (open-control polarity; != is NEQ)
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
    "times": TokenKind.TIMES,
    "for": TokenKind.FOR,  # evolve (…) for dt {…} | evolve psi under H for t
    "under": TokenKind.UNDER,
}

FORBIDDEN: set[str] = {
    "if",
    "switch",
    "while",
    # `for` is contextual inside evolve; bare C-style for-loops still fail to parse
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
    "if": (
        "NON_UNITARY_DECOHERENCE_ERROR: 'if' destroys unitary evolution on "
        "superpositions. Apply a linear operator (H, CNOT, e^{-iHt}, …) or "
        "perform an explicit `measure`; do not branch on an unmeasured quantum wire."
    ),
    "switch": (
        "NON_UNITARY_DECOHERENCE_ERROR: 'switch' is classical control flow. "
        "Use a linear operator or explicit `measure`."
    ),
    "while": (
        "NON_UNITARY_DECOHERENCE_ERROR: 'while' is classical iteration. "
        "Use `evolve … under H for t` or `evolve … times N {…}` for closed dynamics."
    ),
    "break": "Syntax Error: 'break' is forbidden; early exit tears the joint.",
    "return": "Syntax Error: 'return' is forbidden; use block result / evolve.",
    "new": "Syntax Error: Construct with Foo(args); 'new' is forbidden.",
    "null": "Syntax Error: Use Result / when basis labels / empty(); 'null' is forbidden.",
    "try": "Syntax Error: Exceptions are forbidden; use Result + when.",
    "catch": "Syntax Error: Exceptions are forbidden; use Result + when.",
    "throw": "Syntax Error: Exceptions are forbidden; use Result + when.",
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
