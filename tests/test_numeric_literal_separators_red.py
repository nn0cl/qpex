"""AT-TDD Phase 1 Red tests for LISS-0061 / ADR 0101."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.lexer import Lexer
from compiler.qpex.tokens import TokenKind


def test_java_style_separators_preserve_numeric_tokens_and_lexemes() -> None:
    tokens, diagnostics = Lexer("1_000 1_000.25 1.0e1_0").tokenize()
    tokens = tokens[:-1]  # exclude the normal EOF sentinel

    assert not diagnostics
    assert [token.kind for token in tokens] == [
        TokenKind.INT,
        TokenKind.FLOAT,
        TokenKind.FLOAT,
    ]
    assert [token.lexeme for token in tokens] == [
        "1_000",
        "1_000.25",
        "1.0e1_0",
    ]
    assert [token.literal for token in tokens] == [1000, 1000.25, 1.0e10]


def test_malformed_separator_placement_has_specific_diagnostic() -> None:
    malformed = ("100_", "1__000", "1_.0", "1._0", "1e_4", "1e+_4")

    for source in malformed:
        _, diagnostics = Lexer(source).tokenize()

        assert any(
            diagnostic.get("code") == "NUMERIC_LITERAL_SEPARATOR_ERROR"
            for diagnostic in diagnostics
        ), source


def test_leading_underscore_remains_a_private_identifier() -> None:
    tokens, diagnostics = Lexer("_100").tokenize()

    assert not diagnostics
    assert tokens[0].kind is TokenKind.IDENT
    assert tokens[0].lexeme == "_100"


if __name__ == "__main__":
    test_java_style_separators_preserve_numeric_tokens_and_lexemes()
    test_malformed_separator_placement_has_specific_diagnostic()
    print("OK - LISS-0061 Phase 1 Red tests")
