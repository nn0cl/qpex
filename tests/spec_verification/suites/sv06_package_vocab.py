"""SV-06: Packages as subspaces + Forbidden/Retired vocabulary (ADR 0035)."""

from __future__ import annotations

from pathlib import Path

from harness.assertions import AssertionFailure, assertCompileError
from harness.compile_gate import PackageEnv, analyze_source
from harness.report import CaseResult

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def run() -> list[CaseResult]:
    out: list[CaseResult] = []

    # Package namespace: same class name in different packages
    try:
        env = PackageEnv(packages={})
        env.define("alpha.physics", "Particle")
        env.define("beta.physics", "Particle")
        left = env.resolve("alpha.physics", "Particle")
        right = env.resolve("beta.physics", "Particle")
        if left == right:
            raise AssertionFailure("PACKAGE_RESOLVE_ERROR", "qualified names collided")
        product = env.tensor_compose(left, right)
        if "alpha.physics.Particle" not in product or "beta.physics.Particle" not in product:
            raise AssertionFailure("PACKAGE_RESOLVE_ERROR", f"bad tensor label {product}")
        out.append(
            CaseResult(
                "SV-06",
                "sv06-package-tensor",
                "same class name across packages; tensor compose",
                True,
                ["namespace resolve", "tensor_compose"],
            )
        )
    except (AssertionFailure, LookupError, ValueError) as e:
        code = getattr(e, "code", "PACKAGE_RESOLVE_ERROR")
        out.append(
            CaseResult(
                "SV-06",
                "sv06-package-tensor",
                "package resolve",
                False,
                error_code=code,
                message=str(e),
            )
        )

    # Forbidden keywords
    try:
        src = (FIXTURES / "forbidden_if.qpex").read_text(encoding="utf-8")
        diags = analyze_source(src)
        assertCompileError(diags, "FORBIDDEN_KEYWORD")
        out.append(
            CaseResult(
                "SV-06",
                "sv06-forbidden-if",
                "`if` → FORBIDDEN_KEYWORD",
                True,
                ["assertCompileError(FORBIDDEN_KEYWORD)"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-06",
                "sv06-forbidden-if",
                "`if` forbidden",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    try:
        src = (FIXTURES / "forbidden_null_throw.qpex").read_text(encoding="utf-8")
        diags = analyze_source(src)
        assertCompileError(diags, "FORBIDDEN_KEYWORD")
        tokens = {d.get("token") for d in diags if d.get("code") == "FORBIDDEN_KEYWORD"}
        if not {"null", "throw"} <= tokens:
            raise AssertionFailure("FORBIDDEN_KEYWORD", f"expected null+throw, got {tokens}")
        out.append(
            CaseResult(
                "SV-06",
                "sv06-forbidden-null-throw",
                "`null`/`throw` → FORBIDDEN_KEYWORD",
                True,
                ["assertCompileError(FORBIDDEN_KEYWORD)"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-06",
                "sv06-forbidden-null-throw",
                "null/throw forbidden",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    # Retired keywords
    try:
        src = (FIXTURES / "retired_observe_span.qpex").read_text(encoding="utf-8")
        diags = analyze_source(src)
        assertCompileError(diags, "RETIRED_KEYWORD")
        out.append(
            CaseResult(
                "SV-06",
                "sv06-retired-observe-span",
                "`observe`/`span` → RETIRED_KEYWORD",
                True,
                ["assertCompileError(RETIRED_KEYWORD)"],
            )
        )
    except AssertionFailure as e:
        out.append(
            CaseResult(
                "SV-06",
                "sv06-retired-observe-span",
                "retired keywords",
                False,
                error_code=e.code,
                message=str(e),
            )
        )

    return out
