"""AT-TDD Phase 1 Red: LISS-0069 Slice A — Unicode math dual-accept."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.lexer import Lexer
from compiler.qpex.pipeline import compile_source
from compiler.qpex.tokens import TokenKind

KET_CLOSE = "\u27e9"  # ⟩
BRA_OPEN = "\u27e8"  # ⟨
TENSOR = "\u2297"  # ⊗
DAGGER = "\u2020"  # †


def _non_eof(tokens):
    return [token for token in tokens if token.kind is not TokenKind.EOF]


def test_unicode_ket_lexes_like_ascii_ket() -> None:
    ascii_tokens, ascii_diags = Lexer("|0>").tokenize()
    unicode_tokens, unicode_diags = Lexer(f"|0{KET_CLOSE}").tokenize()

    assert not ascii_diags
    assert not unicode_diags
    assert _non_eof(ascii_tokens)[0].kind is TokenKind.KET
    assert _non_eof(unicode_tokens)[0].kind is TokenKind.KET
    assert _non_eof(ascii_tokens)[0].literal == "0"
    assert _non_eof(unicode_tokens)[0].literal == "0"


def test_pipeline_remains_distinct_from_unicode_ket_close() -> None:
    tokens, diagnostics = Lexer(f"x |> |+{KET_CLOSE}").tokenize()

    assert not diagnostics
    kinds = [token.kind for token in _non_eof(tokens)]
    assert kinds == [TokenKind.IDENT, TokenKind.PIPE_OP, TokenKind.KET]
    assert _non_eof(tokens)[2].literal == "+"


def test_unicode_tensor_lexes_as_tensor_op() -> None:
    ascii_tokens, ascii_diags = Lexer("*|*").tokenize()
    unicode_tokens, unicode_diags = Lexer(TENSOR).tokenize()

    assert not ascii_diags
    assert not unicode_diags
    assert _non_eof(ascii_tokens)[0].kind is TokenKind.TENSOR_OP
    assert _non_eof(unicode_tokens)[0].kind is TokenKind.TENSOR_OP


def test_unicode_bra_lexes_with_label() -> None:
    tokens, diagnostics = Lexer(f"{BRA_OPEN}0|").tokenize()

    assert not diagnostics
    bra = _non_eof(tokens)[0]
    assert bra.kind is TokenKind.BRA
    assert bra.literal == "0"


def test_postfix_dagger_lexes_as_dagger_token() -> None:
    tokens, diagnostics = Lexer(f"X{DAGGER}").tokenize()

    assert not diagnostics
    kinds = [token.kind for token in _non_eof(tokens)]
    assert kinds == [TokenKind.IDENT, TokenKind.DAGGER]


def test_unicode_ket_program_compiles_like_ascii() -> None:
    ascii_ok = compile_source(
        """
        package t
        pub fn main() -> Unit {
            state psi = |0>
            measure psi
        }
        """
    )
    unicode_ok = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            state psi = |0{KET_CLOSE}
            measure psi
        }}
        """
    )

    assert ascii_ok.ok, ascii_ok.diagnostics
    assert unicode_ok.ok, unicode_ok.diagnostics


def test_unicode_tensor_bind_compiles_like_ascii() -> None:
    ascii_ok = compile_source(
        """
        package t
        pub fn main() -> Unit {
            state left = |0>
            state right = |1>
            (a, b) = left *|* right
            measure a
        }
        """
    )
    unicode_ok = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            state left = |0>
            state right = |1>
            (a, b) = left {TENSOR} right
            measure a
        }}
        """
    )

    assert ascii_ok.ok, ascii_ok.diagnostics
    assert unicode_ok.ok, unicode_ok.diagnostics


def test_postfix_dagger_compiles_like_adjoint_call() -> None:
    call_ok = compile_source(
        """
        package t
        pub fn main() -> Unit {
            Operator A = adjoint(X)
            State<Int> observed = coin()
            measure observed
        }
        """
    )
    dagger_ok = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            Operator A = X{DAGGER}
            State<Int> observed = coin()
            measure observed
        }}
        """
    )

    assert call_ok.ok, call_ok.diagnostics
    assert dagger_ok.ok, dagger_ok.diagnostics


def test_unterminated_unicode_ket_is_lex_error() -> None:
    _, diagnostics = Lexer("|0").tokenize()

    assert any(diagnostic.get("code") == "LEX_ERROR" for diagnostic in diagnostics)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("OK - LISS-0069 Slice A Phase 2 Green")
