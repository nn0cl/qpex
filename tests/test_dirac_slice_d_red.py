"""AT-TDD Phase 1 Red: LISS-0073 Slice D — ket–bra outer / projector."""

from __future__ import annotations

import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.ast_nodes import BraLit, Call, KetLit, StateBind, Var
from compiler.qpex.pipeline import compile_source

BRA_OPEN = "\u27e8"  # ⟨
KET_CLOSE = "\u27e9"  # ⟩
EBNF_PATH = _REPO / "docs" / "specs" / "grammar" / "qpex.ebnf"


def _codes(compiled) -> set[str]:
    return {diagnostic.get("code", "") for diagnostic in compiled.diagnostics}


def _main_binds(compiled) -> list[StateBind]:
    assert compiled.unit is not None, compiled.diagnostics
    assert compiled.unit.main is not None, "expected MainDecl"
    return [stmt for stmt in compiled.unit.main.body.stmts if isinstance(stmt, StateBind)]


def test_ket_bra_parses_as_outer_call() -> None:
    compiled = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            Operator P = |0{KET_CLOSE}{BRA_OPEN}1|
            State observed = coin()
            measure observed
        }}
        """
    )

    assert "PARSE_ERROR" not in _codes(compiled), compiled.diagnostics
    binds = [bind for bind in _main_binds(compiled) if bind.name == "P"]
    assert len(binds) == 1
    expr = binds[0].expr
    assert isinstance(expr, Call)
    assert isinstance(expr.callee, Var) and expr.callee.name == "outer"
    assert len(expr.args) == 2
    assert isinstance(expr.args[0], KetLit) and expr.args[0].label == "0"
    assert isinstance(expr.args[1], BraLit) and expr.args[1].label == "1"


def test_matching_ket_bra_parses_as_projector() -> None:
    compiled = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            Operator P = |0{KET_CLOSE}{BRA_OPEN}0|
            State observed = coin()
            measure observed
        }}
        """
    )

    assert "PARSE_ERROR" not in _codes(compiled), compiled.diagnostics
    binds = [bind for bind in _main_binds(compiled) if bind.name == "P"]
    expr = binds[0].expr
    assert isinstance(expr, Call)
    assert isinstance(expr.callee, Var) and expr.callee.name == "projector"
    assert len(expr.args) == 1
    assert isinstance(expr.args[0], KetLit) and expr.args[0].label == "0"


def test_outer_and_projector_punctuation_typecheck() -> None:
    compiled = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            Operator O = |0{KET_CLOSE}{BRA_OPEN}1|
            Operator P = |+{KET_CLOSE}{BRA_OPEN}+|
            State observed = coin()
            measure observed
        }}
        """
    )

    assert compiled.ok, compiled.diagnostics
    assert "OPERATOR_ALGEBRA_TYPE_ERROR" not in _codes(compiled)


def test_alone_ket_still_parses_without_following_bra() -> None:
    compiled = compile_source(
        f"""
        package t
        pub fn main() -> Unit {{
            state ket = |0{KET_CLOSE}
            State observed = coin()
            measure observed
        }}
        """
    )

    assert compiled.ok, compiled.diagnostics
    binds = [bind for bind in _main_binds(compiled) if bind.name == "ket"]
    assert isinstance(binds[0].expr, KetLit)
    assert binds[0].expr.label == "0"


def test_ebnf_documents_ket_bra_outer_and_ophop_note() -> None:
    text = EBNF_PATH.read_text(encoding="utf-8")
    assert "ket_bra_outer" in text or re.search(
        r"ket_lit.*bra_lit|outer|projector", text
    ), "EBNF must document |ψ⟩⟨φ| outer/projector surface"
    assert "OpHop" in text or "hop" in text.lower(), (
        "EBNF must note relation to site-local OpHop / hop(i,j)"
    )


def main() -> None:
    test_ket_bra_parses_as_outer_call()
    print("PASS test_ket_bra_parses_as_outer_call")
    test_matching_ket_bra_parses_as_projector()
    print("PASS test_matching_ket_bra_parses_as_projector")
    test_outer_and_projector_punctuation_typecheck()
    print("PASS test_outer_and_projector_punctuation_typecheck")
    test_alone_ket_still_parses_without_following_bra()
    print("PASS test_alone_ket_still_parses_without_following_bra")
    test_ebnf_documents_ket_bra_outer_and_ophop_note()
    print("PASS test_ebnf_documents_ket_bra_outer_and_ophop_note")
    print("OK - LISS-0073 Slice D")


if __name__ == "__main__":
    main()
