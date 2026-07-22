"""Compile + run QPex source on the Discrete PMF Kernel."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from .pipeline import compile_path, compile_source
from .runtime.evaluator import EvalResult, Evaluator
from .runtime.joint import Joint

HARD_CODES = {
    "FORBIDDEN_KEYWORD",
    "EARLY_COLLAPSE_ERROR",
    "NESTED_WHEN_ERROR",
    "INTERFER_INDEPENDENT_STATE_ERROR",
    "EXPECT_CLASSICAL_ONLY_ERROR",
    "COIN_IN_EVOLVE_ERROR",
    "NON_UNITARY_TRANSFORM_ERROR",
    "PREDICATE_PROJECTOR_ERROR",
    "CANNOT_MEASURE_CLASSICAL_VALUE_ERROR",
    "PARSE_ERROR",
    "LEX_ERROR",
    "TYPE_NOT_STATE",
    "DIMENSION_MISMATCH_ERROR",
    "TOPLEVEL_EXECUTION_ERROR",
    "PRODUCT_BIND_ERROR",
    "PRODUCT_ARITY_ERROR",
    "PRODUCT_TYPE_MISMATCH",
    "MODULE_NOT_FOUND_ERROR",
    "MODULE_CYCLE_ERROR",
    "IMMUTABLE_ASSIGNMENT_ERROR",
    "ENUM_TYPE_MISMATCH",
    "ACCESS_CONTROL_VIOLATION_ERROR",
    "PRIVATE_ACCESS_VIOLATION_ERROR",
    "MODULE_PRIVATE_ACCESS_ERROR",
    "PACKAGE_NOT_EXPORTED_ERROR",
}


@dataclass
class RunResult:
    eval: EvalResult
    diagnostics: list[dict[str, Any]]
    compile_ok: bool


def run_source(
    source: str,
    *,
    seed: int | None = None,
    stdout: TextIO | None = None,
    require_clean: bool = True,
) -> RunResult:
    compiled = compile_source(source)
    has_hard = any(d.get("code") in HARD_CODES for d in compiled.diagnostics)
    if (require_clean and has_hard) or compiled.unit is None:
        return RunResult(
            eval=EvalResult(joint=Joint.empty()),
            diagnostics=compiled.diagnostics,
            compile_ok=False,
        )

    ev = Evaluator(seed=seed)
    out = stdout if stdout is not None else sys.stdout
    result = ev.run_unit(compiled.unit, stdout=out)
    return RunResult(eval=result, diagnostics=compiled.diagnostics, compile_ok=True)


def run_path(
    entry: str | Path,
    *,
    seed: int | None = None,
    stdout: TextIO | None = None,
    require_clean: bool = True,
) -> RunResult:
    """Compile+run an entry file with ADR 0054 module linking."""
    compiled = compile_path(entry)
    has_hard = any(d.get("code") in HARD_CODES for d in compiled.diagnostics)
    if (require_clean and has_hard) or compiled.unit is None:
        return RunResult(
            eval=EvalResult(joint=Joint.empty()),
            diagnostics=compiled.diagnostics,
            compile_ok=False,
        )

    ev = Evaluator(seed=seed)
    out = stdout if stdout is not None else sys.stdout
    result = ev.run_unit(compiled.unit, stdout=out)
    return RunResult(eval=result, diagnostics=compiled.diagnostics, compile_ok=True)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="qpex", description="QPex Kernel runner (Phase 2.2)")
    p.add_argument("file", nargs="?", help="Source .qpex file")
    p.add_argument("-e", "--eval", dest="expr", help="Run source string")
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args(argv)

    if args.expr:
        result = run_source(args.expr, seed=args.seed, stdout=sys.stdout)
    elif args.file:
        result = run_path(args.file, seed=args.seed, stdout=sys.stdout)
    else:
        p.error("provide a file or -e source")

    if not result.compile_ok:
        for d in result.diagnostics:
            print(f"{d.get('code')}: {d.get('message')}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
