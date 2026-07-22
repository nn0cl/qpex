"""OpenQASM 3 emission scaffold (ADR 0036) — portable DAG → QPU sketch."""

from __future__ import annotations

from dataclasses import dataclass

from ..ast_nodes import (
    Coin,
    CompilationUnit,
    Dirac,
    LitInt,
    Measure,
    StateBind,
    WhenExpr,
    Var,
)
from ..ir.dag import Dag, lower_source_ast


@dataclass
class EmitResult:
    qasm: str
    notes: list[str]
    ok: bool


def emit_openqasm3(unit: CompilationUnit) -> EmitResult:
    """Best-effort pattern emit; falls back to DAG-commented stub."""
    notes: list[str] = []
    pattern = _try_bell_like(unit)
    if pattern is not None:
        return EmitResult(qasm=pattern, notes=notes, ok=True)

    dag = lower_source_ast(unit)
    notes.append(
        "No coin/when/measure gate pattern matched; emitting DAG-annotated stub."
    )
    return EmitResult(qasm=_dag_stub(dag), notes=notes, ok=True)


def _try_bell_like(unit: CompilationUnit) -> str | None:
    """Recognize: coin → when(ctrl){0→0, else→1} → measure (user ADR example)."""
    if unit.main is None:
        return None
    stmts = unit.main.body.stmts
    binds = [s for s in stmts if isinstance(s, StateBind)]
    measures = [s for s in stmts if isinstance(s, Measure)]
    if len(measures) != 1 or len(binds) < 2:
        return None

    coin_name = None
    for b in binds:
        if isinstance(b.expr, Coin):
            coin_name = b.name
            break
    if coin_name is None:
        return None

    when_name = None
    for b in binds:
        if not isinstance(b.expr, WhenExpr):
            continue
        w = b.expr
        if not isinstance(w.ctrl, Var) or w.ctrl.name != coin_name:
            continue
        if _is_copy_when(w):
            when_name = b.name
            break
    if when_name is None:
        return None

    m = measures[0]
    if not isinstance(m.expr, Var) or m.expr.name != when_name:
        # allow measure of coin or when result
        if not isinstance(m.expr, Var):
            return None

    return _qasm_h_cx_measure()


def _is_copy_when(w: WhenExpr) -> bool:
    """when { 0 -> dirac(0)|0 , else -> dirac(1)|1 }."""
    zero_arm = None
    else_arm = None
    for arm in w.arms:
        if arm.is_else:
            else_arm = arm.body
        elif arm.pat == 0:
            zero_arm = arm.body
    if zero_arm is None or else_arm is None:
        return False
    return _is_dirac_or_lit(zero_arm, 0) and _is_dirac_or_lit(else_arm, 1)


def _is_dirac_or_lit(expr, value: int) -> bool:
    if isinstance(expr, LitInt) and expr.value == value:
        return True
    if isinstance(expr, Dirac):
        return _is_dirac_or_lit(expr.arg, value)
    return False


def _qasm_h_cx_measure() -> str:
    return """OPENQASM 3.0;
include "stdgates.inc";
// QPex codegen (ADR 0036) — coin() → H; when-copy → CX; measure
qubit[2] q;
bit[1] c;
h q[0];
cx q[0], q[1];
c[0] = measure q[1];
"""


def _dag_stub(dag: Dag) -> str:
    lines = [
        "OPENQASM 3.0;",
        'include "stdgates.inc";',
        "// QPex DAG stub — full gate decomposition TBD",
        f"// dag nodes: {dag.summary()['node_count']} kinds={dag.summary()['kinds']}",
        "qubit[1] q;",
        "bit[1] c;",
        "// placeholder identity",
        "c[0] = measure q[0];",
        "",
    ]
    return "\n".join(lines)
