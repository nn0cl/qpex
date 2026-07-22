"""Early Collapse semantic check (ADR 0027) — measure must be terminal in main."""

from __future__ import annotations

from .ast_nodes import CompilationUnit, Measure, Stmt


def check_early_collapse(unit: CompilationUnit) -> list[dict]:
    diags: list[dict] = []
    if unit.main is None:
        return diags

    stmts: list[Stmt] = unit.main.body.stmts
    measure_idxs = [i for i, s in enumerate(stmts) if isinstance(s, Measure)]

    if not measure_idxs:
        # main without measure — separate diagnostic optional; not EARLY_COLLAPSE
        return diags

    for mi in measure_idxs:
        # any non-empty stmt after this measure → early collapse
        for j in range(mi + 1, len(stmts)):
            diags.append(
                {
                    "code": "EARLY_COLLAPSE_ERROR",
                    "line": stmts[mi].span.line,
                    "col": stmts[mi].span.col,
                    "message": (
                        f"measure at line {stmts[mi].span.line} is not terminal; "
                        f"code continues at line {stmts[j].span.line}"
                    ),
                }
            )
            break

    # multiple measures: only last may be terminal; earlier ones are early collapse
    if len(measure_idxs) > 1:
        for mi in measure_idxs[:-1]:
            # already flagged if anything follows; if next is also measure, flag
            if mi + 1 < len(stmts):
                # ensure we have a diag for this measure
                if not any(
                    d.get("line") == stmts[mi].span.line and d.get("code") == "EARLY_COLLAPSE_ERROR"
                    for d in diags
                ):
                    diags.append(
                        {
                            "code": "EARLY_COLLAPSE_ERROR",
                            "line": stmts[mi].span.line,
                            "col": stmts[mi].span.col,
                            "message": "measure must be the final statement of main",
                        }
                    )

    return diags
