"""AT-TDD: LISS-0145 binder where ||."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.finite_binder import lower_finite_binder_operators  # noqa: E402
from compiler.staqex.pipeline import compile_source  # noqa: E402


def _codes(source: str) -> set[str]:
    return {d.get("code", "") for d in compile_source(source).diagnostics}


def test_where_or_lowers() -> None:
    source = """
    package t
    pub fn main() -> Unit {
        QubitRegister<3> register = system()
        Operator H = sum (i in Index<0..2>, j in Index<0..2>) where i < j || j == 0 {
            Z[i] * Z[j]
        }
        state a = |0>
        measure a
    }
    """
    codes = _codes(source)
    assert "LEX_ERROR" not in codes
    assert "PARSE_ERROR" not in codes
    compiled = compile_source(source)
    assert compiled.unit is not None
    lowered, _ = lower_finite_binder_operators(compiled.unit)
    assert "H" in lowered


def test_statement_or_still_errors() -> None:
    codes = _codes(
        """
        package t
        pub fn main() -> Unit {
            Float x = 1.0
            Float y = 0.0
            Float z = x || y
            measure z
        }
        """
    )
    assert "LEX_ERROR" in codes or "PARSE_ERROR" in codes or "FORBIDDEN_KEYWORD" in codes


if __name__ == "__main__":
    test_where_or_lowers()
    print("PASS test_where_or_lowers")
    test_statement_or_still_errors()
    print("PASS test_statement_or_still_errors")
