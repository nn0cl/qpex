"""SV-23: Static unitarity checks — NON_UNITARY_TRANSFORM_ERROR (ADR 0045)."""

from __future__ import annotations

import sys
from pathlib import Path

from harness import AssertionFailure, as_main
from harness.report import CaseResult

_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.pipeline import compile_source  # noqa: E402


def _codes(src: str) -> list[str]:
    return [d.get("code", "") for d in compile_source(src).diagnostics]


def run() -> list[CaseResult]:
    out: list[CaseResult] = []

    cases = [
        (
            "sv23-project-ket",
            "project on |+> → NON_UNITARY_TRANSFORM_ERROR",
            "NON_UNITARY_TRANSFORM_ERROR",
            as_main(
                """
state psi = |+>
state bad = project(psi, x -> x == 0)
measure bad
"""
            ),
        ),
        (
            "sv23-map-constant",
            "map(_, x -> 0) on ket → NON_UNITARY_TRANSFORM_ERROR",
            "NON_UNITARY_TRANSFORM_ERROR",
            as_main(
                """
state psi = |+>
state bad = map(psi, x -> 0)
measure bad
"""
            ),
        ),
        (
            "sv23-when-collapse",
            "when arms same literal on ket → NON_UNITARY_TRANSFORM_ERROR",
            "NON_UNITARY_TRANSFORM_ERROR",
            as_main(
                """
state psi = |+>
state bad = when (psi) { 0 -> 7, else -> 7 }
measure bad
"""
            ),
        ),
        (
            "sv23-apply-non-unitary",
            "apply(2X) → NON_UNITARY_TRANSFORM_ERROR",
            "NON_UNITARY_TRANSFORM_ERROR",
            as_main(
                """
Operator Bad = 2.0 * X
state psi = |0>
state psi = apply(Bad, psi)
measure psi
"""
            ),
        ),
        (
            "sv23-apply-hadamard-ok",
            "normalized (X+Z)/√2 apply accepted",
            None,
            as_main(
                """
Operator Had = 0.7071067811865476 * (X + Z)
state psi = |0>
state psi = apply(Had, psi)
measure psi
"""
            ),
        ),
        (
            "sv23-classical-project-ok",
            "project on classical coin (Ising-style) accepted",
            None,
            as_main(
                """
state s = coin()
state kept = project(s, v -> v == 1)
measure kept
"""
            ),
        ),
    ]

    for case_id, title, expect, src in cases:
        try:
            codes = _codes(src)
            if expect is None:
                if "NON_UNITARY_TRANSFORM_ERROR" in codes:
                    raise AssertionFailure(
                        "NON_UNITARY_TRANSFORM_ERROR", f"unexpected: {codes}"
                    )
            else:
                if expect not in codes:
                    raise AssertionFailure(expect, f"got {codes}")
            out.append(
                CaseResult("SV-23", case_id, title, True, [expect or "ok"])
            )
        except AssertionFailure as e:
            out.append(
                CaseResult(
                    "SV-23",
                    case_id,
                    title,
                    False,
                    [],
                    error_code=e.code,
                    message=str(e.message),
                )
            )

    # gauge example still compiles
    try:
        src = (_REPO / "examples/08_qft_and_fields/gauge_symmetry.qpex").read_text(
            encoding="utf-8"
        )
        codes = _codes(src)
        if "NON_UNITARY_TRANSFORM_ERROR" in codes:
            raise AssertionFailure("NON_UNITARY_TRANSFORM_ERROR", str(codes))
        out.append(
            CaseResult(
                "SV-23",
                "sv23-gauge-phase-project-ok",
                "gauge_symmetry phase+project still accepted",
                True,
                ["examples"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-23",
                "sv23-gauge-phase-project-ok",
                "gauge_symmetry phase+project still accepted",
                False,
                [],
                error_code=e.code,
                message=str(e.message),
            )
        )

    return out
