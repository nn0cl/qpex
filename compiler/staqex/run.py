"""Compile + run QPex source on the Discrete PMF Kernel."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from .finite_binder import (
    IDENTITY_ACTING_SPACE_UNDETERMINED,
    identity_acting_space_diagnostics,
)
from .pipeline import compile_path, compile_source
from .resource_enforcement import enforce_optional_budget
from .resource_profile import ResourceProfile, SimulationResourceEstimate
from .runtime.evaluator import EvalResult, Evaluator
from .runtime.joint import Joint

HARD_CODES = {
    "FORBIDDEN_KEYWORD",
    "RETIRED_KEYWORD",
    "EARLY_COLLAPSE_ERROR",
    "NESTED_WHEN_ERROR",
    "INTERFER_INDEPENDENT_STATE_ERROR",
    "EXPECT_CLASSICAL_ONLY_ERROR",
    "TYPE_MISMATCH",
    "COIN_IN_EVOLVE_ERROR",
    "NON_UNITARY_TRANSFORM_ERROR",
    "PREDICATE_PROJECTOR_ERROR",
    "CANNOT_MEASURE_CLASSICAL_VALUE_ERROR",
    "PARSE_ERROR",
    "LEX_ERROR",
    "TYPE_NOT_STATE",
    "DIMENSION_MISMATCH_ERROR",
    "LOCAL_DIMENSION_TYPE_ERROR",
    "UNSUPPORTED_LOCAL_DIMENSION",
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
    "CONFIG_HARVEST_COLLISION_ERROR",
    "MAIN_RETURN_TYPE_ERROR",
    "MISSING_RETURN_TYPE",
    "MAIN_RESULT_ERROR",
    "RETURN_TYPE_MISMATCH",
    "MISSING_RETURN_VALUE",
    "MEASURE_IN_FUNCTION_ERROR",
    "SNAPSHOT_IN_FUNCTION_ERROR",
    IDENTITY_ACTING_SPACE_UNDETERMINED,
    "DISCRETIZATION_LOWERING_ERROR",
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
    resource_profile: ResourceProfile | None = None,
    resource_estimate: SimulationResourceEstimate | None = None,
) -> RunResult:
    compiled = compile_source(source)
    compiled.diagnostics.extend(
        identity_acting_space_diagnostics(compiled.unit) if compiled.unit else []
    )
    has_hard = any(d.get("code") in HARD_CODES for d in compiled.diagnostics)
    if (require_clean and has_hard) or compiled.unit is None:
        return RunResult(
            eval=EvalResult(joint=Joint.empty()),
            diagnostics=compiled.diagnostics,
            compile_ok=False,
        )

    diagnostics = list(compiled.diagnostics)
    decision = enforce_optional_budget(
        resource_profile,
        resource_estimate,
        lane="simulator",
    )
    if decision is not None:
        diagnostics.extend(decision.diagnostics)
        if not decision.continue_execution:
            return RunResult(
                eval=EvalResult(joint=Joint.empty()),
                diagnostics=diagnostics,
                compile_ok=False,
            )

    ev = Evaluator(
        seed=seed,
        grid_hamiltonians=dict(compiled.grid_hamiltonians or {}),
    )
    out = stdout if stdout is not None else sys.stdout
    result = ev.run_unit(compiled.unit, stdout=out)
    return RunResult(eval=result, diagnostics=diagnostics, compile_ok=True)


def run_path(
    entry: str | Path,
    *,
    seed: int | None = None,
    stdout: TextIO | None = None,
    require_clean: bool = True,
) -> RunResult:
    """Compile+run an entry file with ADR 0054 module linking."""
    compiled = compile_path(entry)
    compiled.diagnostics.extend(
        identity_acting_space_diagnostics(compiled.unit) if compiled.unit else []
    )
    has_hard = any(d.get("code") in HARD_CODES for d in compiled.diagnostics)
    if (require_clean and has_hard) or compiled.unit is None:
        return RunResult(
            eval=EvalResult(joint=Joint.empty()),
            diagnostics=compiled.diagnostics,
            compile_ok=False,
        )

    ev = Evaluator(
        seed=seed,
        grid_hamiltonians=dict(compiled.grid_hamiltonians or {}),
    )
    out = stdout if stdout is not None else sys.stdout
    result = ev.run_unit(compiled.unit, stdout=out)
    return RunResult(eval=result, diagnostics=compiled.diagnostics, compile_ok=True)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="qpex", description="QPex Kernel runner (Phase 2.2)")
    p.add_argument("file", nargs="?", help="Source .sqx file")
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
