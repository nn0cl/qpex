"""SV-03: Failure as superposition — no exceptions; Result worlds coexist."""

from __future__ import annotations

from harness import AssertionFailure, ResultErr, ResultOk, State, assertNormEquals, assertSuperposition, assertTypeIsState, lift
from harness.report import CaseResult


def run() -> list[CaseResult]:
    out: list[CaseResult] = []

    try:
        numer = State({1.0: 0.5, 2.0: 0.5}, payload_type=float)
        denom = State({0.0: 0.5, 2.0: 0.5}, payload_type=float)
        # must not raise
        result = numer / denom
        assertTypeIsState(result)
        assertNormEquals(result, 1.0)
        # Expected:
        # (1,0)->Err, (1,2)->Ok(0.5), (2,0)->Err, (2,2)->Ok(1.0)
        # Err: 0.25+0.25=0.5; Ok(0.5):0.25; Ok(1.0):0.25
        expected = {
            ResultErr("DivByZero"): 0.5,
            ResultOk(0.5): 0.25,
            ResultOk(1.0): 0.25,
        }
        assertSuperposition(result, expected)
        out.append(
            CaseResult(
                "SV-03",
                "sv03-div-by-zero",
                "div-by-zero → Result Ok/Err superposition",
                True,
                ["assertTypeIsState", "assertNormEquals", "assertSuperposition"],
            )
        )
    except ZeroDivisionError as e:
        out.append(
            CaseResult(
                "SV-03",
                "sv03-div-by-zero",
                "div-by-zero must not raise",
                False,
                error_code="UNEXPECTED_EXCEPTION",
                message=str(e),
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-03",
                "sv03-div-by-zero",
                "div-by-zero → Result Ok/Err superposition",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    try:
        # pure success path still State[Result]
        a = lift(8.0)
        b = lift(2.0)
        r = a / b
        assertTypeIsState(r)
        assertNormEquals(r, 1.0)
        assertSuperposition(r, {ResultOk(4.0): 1.0})
        out.append(
            CaseResult(
                "SV-03",
                "sv03-div-ok",
                "successful div is State[Result.Ok]",
                True,
                ["assertTypeIsState", "assertNormEquals", "assertSuperposition"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-03",
                "sv03-div-ok",
                "successful div is State[Result.Ok]",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    return out
