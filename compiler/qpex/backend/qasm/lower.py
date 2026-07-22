"""DAG / AST → logical Circuit (Phase 4.1)."""

from __future__ import annotations

from ...ast_nodes import (
    Call,
    Coin,
    CompilationUnit,
    Dirac,
    KetLit,
    LitInt,
    Measure,
    StateBind,
    Var,
    WhenExpr,
)
from ...ir.dag import Dag, lower_source_ast
from .circuit import Circuit, Gate


def lower_unit_to_circuit(unit: CompilationUnit) -> Circuit:
    """Prefer structural AST patterns; else DAG-driven heuristic."""
    circ = _from_ast_patterns(unit)
    if circ is not None:
        return circ
    dag = lower_source_ast(unit)
    return _from_dag(dag)


def _from_ast_patterns(unit: CompilationUnit) -> Circuit | None:
    if unit.main is None:
        return None
    stmts = unit.main.body.stmts
    binds = [s for s in stmts if isinstance(s, StateBind)]
    measures = [s for s in stmts if isinstance(s, Measure)]
    if not measures:
        return None

    # Map state names → logical qubit ids as we allocate
    qubit_of: dict[str, int] = {}
    gates: list[Gate] = []
    next_q = 0
    notes: list[str] = []

    def alloc(name: str) -> int:
        nonlocal next_q
        if name not in qubit_of:
            qubit_of[name] = next_q
            next_q += 1
        return qubit_of[name]

    for b in binds:
        if isinstance(b.expr, Coin):
            q = alloc(b.name)
            gates.append(Gate("h", (q,), comment=f"coin() → |+⟩ on {b.name}"))
            continue
        if isinstance(b.expr, KetLit):
            q = alloc(b.name)
            lab = b.expr.label
            if lab == "+":
                gates.append(Gate("h", (q,), comment=f"|+⟩ on {b.name}"))
            elif lab == "1":
                gates.append(Gate("x", (q,), comment=f"|1⟩ on {b.name}"))
            elif lab == "-":
                gates.append(Gate("x", (q,), comment=f"|-⟩ prep X"))
                gates.append(Gate("h", (q,), comment=f"|-⟩ prep H"))
            else:
                notes.append(f"|{lab}⟩ on {b.name} ≈ |0⟩ idle / multi-qubit later")
            continue
        if isinstance(b.expr, Call) and isinstance(b.expr.callee, Var) and b.expr.callee.name == "cnot":
            if len(b.expr.args) == 2 and all(isinstance(a, Var) for a in b.expr.args):
                ctrl_n = b.expr.args[0].name
                tgt_n = b.expr.args[1].name
                if ctrl_n not in qubit_of:
                    notes.append(f"cnot ctrl `{ctrl_n}` unbound")
                    continue
                ctrl = qubit_of[ctrl_n]
                if tgt_n in qubit_of:
                    tgt = qubit_of[tgt_n]
                else:
                    tgt = alloc(tgt_n)
                qubit_of[b.name] = tgt
                gates.append(Gate("cx", (ctrl, tgt), comment=f"cnot {ctrl_n}→{tgt_n}"))
                continue
        if isinstance(b.expr, Call) and isinstance(b.expr.callee, Var) and b.expr.callee.name == "apply":
            gate_nm = _unitary_gate_name(b.expr.args[0]) if b.expr.args else None
            if (
                gate_nm in {"x", "y", "z", "h"}
                and len(b.expr.args) == 2
                and isinstance(b.expr.args[1], Var)
            ):
                src = b.expr.args[1].name
                if src not in qubit_of:
                    notes.append(f"apply target `{src}` unbound")
                    continue
                q = qubit_of[src]
                qubit_of[b.name] = q
                gates.append(
                    Gate(gate_nm, (q,), comment=f"apply({gate_nm.upper()}, {src})")  # type: ignore[arg-type]
                )
                continue
        if isinstance(b.expr, Call) and isinstance(b.expr.callee, Var) and b.expr.callee.name == "capply":
            # capply(ctrl, U, tgt) with single control
            if len(b.expr.args) == 3 and isinstance(b.expr.args[0], Var) and isinstance(
                b.expr.args[2], Var
            ):
                u = _unitary_gate_name(b.expr.args[1])
                ctrl_n = b.expr.args[0].name
                tgt_n = b.expr.args[2].name
                if ctrl_n not in qubit_of or tgt_n not in qubit_of:
                    notes.append(f"capply unbound wires `{ctrl_n}`/`{tgt_n}`")
                    continue
                ctrl, tgt = qubit_of[ctrl_n], qubit_of[tgt_n]
                qubit_of[b.name] = tgt
                if u == "x":
                    gates.append(Gate("cx", (ctrl, tgt), comment=f"capply X {ctrl_n}→{tgt_n}"))
                elif u == "z":
                    gates.append(Gate("cz", (ctrl, tgt), comment=f"capply Z {ctrl_n}→{tgt_n}"))
                else:
                    notes.append(f"capply({u}) not mapped to QASM yet")
                continue
        if isinstance(b.expr, Call) and isinstance(b.expr.callee, Var) and b.expr.callee.name == "expect":
            notes.append(f"expect(...) on `{b.name}` is classical — skipped in QASM")
            continue
        if isinstance(b.expr, WhenExpr) and isinstance(b.expr.ctrl, Var):
            ctrl_name = b.expr.ctrl.name
            if ctrl_name not in qubit_of:
                notes.append(f"when ctrl `{ctrl_name}` unbound; skip CX pattern")
                continue
            if _is_copy_when(b.expr):
                tgt = alloc(b.name)
                ctrl = qubit_of[ctrl_name]
                gates.append(Gate("cx", (ctrl, tgt), comment=f"when-copy {ctrl_name}→{b.name}"))
                continue
            # generic when: RZ annotation + note (amplitude IR later)
            tgt = alloc(b.name)
            gates.append(Gate("h", (tgt,), comment=f"when-mixture prep {b.name}"))
            gates.append(Gate("rz", (tgt,), angle=0.0, comment="when phase placeholder"))
            notes.append(f"generic when on `{b.name}` lowered to H+RZ(0) placeholder")
            continue
        if isinstance(b.expr, Dirac) or isinstance(b.expr, LitInt):
            q = alloc(b.name)
            val = _dirac_bit(b.expr)
            if val == 1:
                gates.append(Gate("x", (q,), comment=f"dirac(1) {b.name}"))
            else:
                notes.append(f"dirac(0) on {b.name} = |0⟩ (idle)")
            continue

    # interfer nodes: RZ on involved qubits (phase kick heuristic)
    # handled via DAG path primarily

    m = measures[0]
    if isinstance(m.expr, Var) and m.expr.name in qubit_of:
        q = qubit_of[m.expr.name]
    elif qubit_of:
        q = next(reversed(list(qubit_of.values())))
        notes.append("measure fallback: last allocated qubit")
    else:
        q = alloc("_m")
        gates.append(Gate("h", (q,), comment="empty program fallback"))

    gates.append(Gate("measure", (q,), bits=(0,), comment="terminal measure"))
    n_q = max(next_q, 1)
    return Circuit(n_qubits=n_q, n_bits=1, gates=gates, notes=notes)


def _from_dag(dag: Dag) -> Circuit:
    gates: list[Gate] = []
    notes = ["DAG heuristic lowering (no AST coin/when pattern)"]
    qmap: dict[int, int] = {}
    next_q = 0

    def q_for(nid: int) -> int:
        nonlocal next_q
        if nid not in qmap:
            qmap[nid] = next_q
            next_q += 1
        return qmap[nid]

    for n in dag.nodes:
        if n.kind == "coin":
            q = q_for(n.id)
            gates.append(Gate("h", (q,), comment=f"dag coin n{n.id}"))
        elif n.kind == "when":
            # CX if has ≥2 inputs (ctrl + body)
            if len(n.inputs) >= 2:
                c, t = q_for(n.inputs[0]), q_for(n.id)
                if c == t:
                    t = q_for(n.id + 10_000)  # force distinct
                gates.append(Gate("cx", (c, t), comment=f"dag when n{n.id}"))
            else:
                q = q_for(n.id)
                gates.append(Gate("rz", (q,), angle=0.0, comment=f"dag when rz n{n.id}"))
        elif n.kind == "interfer":
            for inp in n.inputs:
                q = q_for(inp)
                gates.append(Gate("rz", (q,), angle=0.0, comment=f"dag interfer phase n{n.id}"))
            q = q_for(n.id)
            gates.append(Gate("h", (q,), comment=f"dag interfer mix n{n.id}"))
        elif n.kind == "measure":
            src = n.inputs[0] if n.inputs else n.id
            q = q_for(src)
            gates.append(Gate("measure", (q,), bits=(0,), comment=f"dag measure n{n.id}"))

    if not any(g.name == "measure" for g in gates):
        q = 0 if next_q == 0 else next_q - 1
        if next_q == 0:
            next_q = 1
            gates.append(Gate("h", (0,), comment="dag empty"))
        gates.append(Gate("measure", (q,), bits=(0,)))

    return Circuit(n_qubits=max(next_q, 1), n_bits=1, gates=gates, notes=notes)


def _is_copy_when(w: WhenExpr) -> bool:
    zero_arm = else_arm = None
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


def _dirac_bit(expr) -> int:
    if isinstance(expr, LitInt):
        return int(expr.value)
    if isinstance(expr, Dirac):
        return _dirac_bit(expr.arg)
    return 0


def _unitary_gate_name(expr) -> str | None:
    """Map QPex unitary token (Var `X`/`H`/…) to lowercase OpenQASM gate id."""
    if isinstance(expr, Var):
        n = expr.name
        if n in {"X", "Y", "Z", "H"}:
            return n.lower()
        if n in {"x", "y", "z", "h"}:
            return n
    return None
