"""AT-TDD: LISS-0181 multi-hole Partial pipe fill (ADR 0149)."""

from __future__ import annotations

import io
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.pipeline import compile_source  # noqa: E402
from compiler.staqex.run import run_source  # noqa: E402


def test_stepwise_multi_hole_partial_via_pipe() -> None:
    codes = {
        d.get("code", "")
        for d in compile_source(
            """
            package t
            fn add3(a: State<Int>, b: State<Int>, c: State<Int>) -> State<Int> {
                return a + b + c
            }
            pub fn main() -> Unit {
                state p = add3(1, _, _)
                state x = 2
                state q = x |> p
                state y = 3
                state r = y |> q
                measure r
            }
            """
        ).diagnostics
    }
    assert "PARSE_ERROR" not in codes, codes
    assert "FUNCTION_ARITY_ERROR" not in codes, codes

    result = run_source(
        """
        package t
        fn add3(a: State<Int>, b: State<Int>, c: State<Int>) -> State<Int> {
            return a + b + c
        }
        pub fn main() -> Unit {
            state p = add3(1, _, _)
            state x = 2
            state q = x |> p
            state y = 3
            state r = y |> q
            measure r
        }
        """,
        stdout=io.StringIO(),
    )
    assert result.compile_ok, result.diagnostics
    assert result.eval.measure is not None
    assert result.eval.measure.value == 6  # 1+2+3


def test_inline_multi_hole_call_pipe_forms_partial() -> None:
    result = run_source(
        """
        package t
        fn add3(a: State<Int>, b: State<Int>, c: State<Int>) -> State<Int> {
            return a + b + c
        }
        pub fn main() -> Unit {
            state x = 2
            state q = x |> add3(1, _, _)
            state y = 3
            state r = y |> q
            measure r
        }
        """,
        stdout=io.StringIO(),
    )
    assert result.compile_ok, result.diagnostics
    assert result.eval.measure is not None
    assert result.eval.measure.value == 6


def test_one_hole_partial_pipe_still_works() -> None:
    result = run_source(
        """
        package t
        fn add(x: State<Int>, y: State<Int>) -> State<Int> {
            return x + y
        }
        pub fn main() -> Unit {
            state p = add(10, _)
            state z = 3
            state r = z |> p
            measure r
        }
        """,
        stdout=io.StringIO(),
    )
    assert result.compile_ok, result.diagnostics
    assert result.eval.measure is not None
    assert result.eval.measure.value == 13


if __name__ == "__main__":
    test_stepwise_multi_hole_partial_via_pipe()
    print("PASS test_stepwise_multi_hole_partial_via_pipe")
    test_inline_multi_hole_call_pipe_forms_partial()
    print("PASS test_inline_multi_hole_call_pipe_forms_partial")
    test_one_hole_partial_pipe_still_works()
    print("PASS test_one_hole_partial_pipe_still_works")
