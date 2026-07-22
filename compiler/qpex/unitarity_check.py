"""Static unitarity / isometry guards (ADR 0045).

MVP catches clear non-unitary remaps on quantum lineages and non-unitary
Operator matrices used with `apply` / `capply`. Full proof of all pushforwards
remains Deferred.
"""

from __future__ import annotations

from typing import Any, Iterator

from .ast_nodes import (
    Attr,
    BinOp,
    Call,
    Coin,
    CompilationUnit,
    Dirac,
    EvolveExpr,
    Expr,
    Inspect,
    KetLit,
    Lambda,
    LitBool,
    LitFloat,
    LitInt,
    LitString,
    Measure,
    Pipe,
    Snapshot,
    StateBind,
    TensorExpr,
    TupleExpr,
    Var,
    WhenExpr,
)
from .runtime.hamiltonian import compile_hamiltonian, op_n_qubits
from .runtime.matrix import mat_dag, mat_mul
from .runtime.unitaries import named_gate_matrix


_EPS = 1e-8

# Ops that mark a coherent quantum lineage (ket / gate / walk)
_QUANTUM_OPS = frozenset(
    {
        "apply",
        "capply",
        "toffoli",
        "hadamard",
        "cnot",
        "phase",
        "diffuse",
        "interfer",
        "shift",
    }
)

# Stricter: non-unitary filters banned only on these (not phase-on-coin pedagogy)
_STRICT_QUANTUM_OPS = frozenset(
    {
        "apply",
        "capply",
        "toffoli",
        "hadamard",
        "cnot",
        "interfer",
        "shift",
    }
)


def check_unitarity(unit: CompilationUnit) -> list[dict[str, Any]]:
    diags: list[dict[str, Any]] = []
    if unit.main is None:
        return diags

    operators: dict[str, Any] = {}
    scalars: dict[str, float] = {}
    quantum: dict[str, bool] = {}  # coherent (incl. phase)
    strict: dict[str, bool] = {}  # ket / gates / interfer — project banned

    for stmt in unit.main.body.stmts:
        if not isinstance(stmt, StateBind):
            if isinstance(stmt, (Measure, Snapshot)):
                _check_expr_unitarity(
                    stmt.expr, quantum, strict, operators, scalars, diags
                )
            continue
        if stmt.ty is not None and stmt.ty.name == "Operator":
            if len(stmt.names) == 1:
                operators[stmt.names[0]] = stmt.expr
            continue
        if (
            stmt.ty is not None
            and stmt.ty.name not in {"State", "Operator", "Delta"}
            and len(stmt.names) == 1
            and _is_numeric_lit(stmt.expr)
        ):
            scalars[stmt.names[0]] = float(_lit_value(stmt.expr))

        q = _expr_is_quantum(stmt.expr, quantum, strict_mode=False)
        s = _expr_is_quantum(stmt.expr, strict, strict_mode=True)
        for n in stmt.names:
            quantum[n] = q
            strict[n] = s

        _check_expr_unitarity(
            stmt.expr, quantum, strict, operators, scalars, diags
        )

    return diags


def _check_expr_unitarity(
    expr: Expr,
    quantum: dict[str, bool],
    strict: dict[str, bool],
    operators: dict[str, Any],
    scalars: dict[str, float],
    diags: list[dict[str, Any]],
) -> None:
    if isinstance(expr, Call):
        op = _op_name(expr)
        if op == "project" and expr.args:
            if _expr_is_quantum(expr.args[0], strict, strict_mode=True):
                diags.append(
                    {
                        "code": "NON_UNITARY_TRANSFORM_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            "`project` on a quantum State is a non-unitary filter. "
                            "Use `measure` only at the end, or keep coherent ops "
                            "(`apply` / `capply` / `phase` / `interfer`)."
                        ),
                    }
                )
        if op == "map" and len(expr.args) >= 2:
            src, fn = expr.args[0], expr.args[1]
            if _expr_is_quantum(src, strict, strict_mode=True) and _lambda_is_constant(
                fn
            ):
                diags.append(
                    {
                        "code": "NON_UNITARY_TRANSFORM_ERROR",
                        "line": expr.span.line,
                        "col": expr.span.col,
                        "message": (
                            "`map` with a constant function on a quantum State "
                            "collapses the support (non-isometric). Use a bijective "
                            "remap or a unitary (`apply`)."
                        ),
                    }
                )
        if op in {"apply", "capply"} and expr.args:
            from .runtime.unitaries import named_gate_matrix

            if op == "apply":
                u_expr = expr.args[0]
                n_wires = len(expr.args) - 1
            else:
                u_idx = None
                for i, a in enumerate(expr.args):
                    if isinstance(a, Var) and (
                        a.name in operators or named_gate_matrix(a.name) is not None
                    ):
                        u_idx = i
                        break
                if u_idx is None or u_idx < 1 or u_idx >= len(expr.args) - 1:
                    u_expr = None
                    n_wires = 0
                else:
                    u_expr = expr.args[u_idx]
                    n_wires = len(expr.args) - u_idx - 1
            if u_expr is not None and n_wires >= 1:
                _check_apply_unitary(u_expr, n_wires, operators, scalars, diags, expr)
        for a in expr.args:
            _check_expr_unitarity(a, quantum, strict, operators, scalars, diags)
        return

    if isinstance(expr, WhenExpr):
        if _expr_is_quantum(expr.ctrl, strict, strict_mode=True) and _when_collapses(
            expr
        ):
            diags.append(
                {
                    "code": "NON_UNITARY_TRANSFORM_ERROR",
                    "line": expr.span.line,
                    "col": expr.span.col,
                    "message": (
                        "`when` on a quantum control maps distinct arms to the same "
                        "value (non-injective / non-unitary). Prefer `apply` / `capply`."
                    ),
                }
            )
        _check_expr_unitarity(expr.ctrl, quantum, strict, operators, scalars, diags)
        for arm in expr.arms:
            _check_expr_unitarity(
                arm.body, quantum, strict, operators, scalars, diags
            )
        return

    if isinstance(expr, EvolveExpr) and expr.hamiltonian is not None:
        hop = expr.hamiltonian
        if isinstance(hop, Var) and hop.name in operators:
            _check_hamiltonian_hermitian(
                hop.name, operators[hop.name], operators, scalars, diags, expr
            )
        for s in expr.seeds:
            _check_expr_unitarity(s, quantum, strict, operators, scalars, diags)
        return

    for child in _children(expr):
        _check_expr_unitarity(child, quantum, strict, operators, scalars, diags)


def _check_apply_unitary(
    u_expr: Expr,
    n_wires: int,
    operators: dict[str, Any],
    scalars: dict[str, float],
    diags: list[dict[str, Any]],
    site: Expr,
) -> None:
    if not isinstance(u_expr, Var):
        return
    name = u_expr.name
    try:
        if name in operators:
            op_ast = operators[name]
            nq = op_n_qubits(op_ast, operators, scalars)
            if nq == 0:
                return
            if nq != n_wires:
                return
            mat = compile_hamiltonian(
                op_ast, env=operators, scalars=scalars, n_qubits=n_wires
            )
        else:
            mat = named_gate_matrix(name)
            if mat is None:
                return
            if n_wires != 1:
                return
        if not _is_unitary(mat):
            diags.append(
                {
                    "code": "NON_UNITARY_TRANSFORM_ERROR",
                    "line": site.span.line,
                    "col": site.span.col,
                    "message": (
                        f"`apply`/`capply` matrix for `{name}` is not unitary "
                        f"(U†U ≉ I). Use a unitary Operator or gate (Hadamard, Pauli)."
                    ),
                }
            )
    except (ValueError, TypeError, KeyError):
        return


def _check_hamiltonian_hermitian(
    name: str,
    op_ast: Any,
    operators: dict[str, Any],
    scalars: dict[str, float],
    diags: list[dict[str, Any]],
    site: Expr,
) -> None:
    try:
        nq = op_n_qubits(op_ast, operators, scalars)
        if nq == 0:
            mat = compile_hamiltonian(
                op_ast, env=operators, scalars=scalars, n_qubits=0, fock_dim=4
            )
        else:
            mat = compile_hamiltonian(
                op_ast, env=operators, scalars=scalars, n_qubits=nq
            )
        if not _is_hermitian(mat):
            diags.append(
                {
                    "code": "NON_UNITARY_TRANSFORM_ERROR",
                    "line": site.span.line,
                    "col": site.span.col,
                    "message": (
                        f"Hamiltonian `{name}` is not Hermitian (H† ≉ H); "
                        f"`evolve under H` would not be unitary."
                    ),
                }
            )
    except (ValueError, TypeError, KeyError):
        return


def _is_unitary(m: list[list[complex]]) -> bool:
    n = len(m)
    prod = mat_mul(mat_dag(m), m)
    for i in range(n):
        for j in range(n):
            target = 1.0 if i == j else 0.0
            if abs(prod[i][j] - target) > _EPS:
                return False
    return True


def _is_hermitian(m: list[list[complex]]) -> bool:
    n = len(m)
    for i in range(n):
        for j in range(n):
            if abs(m[i][j] - m[j][i].conjugate()) > _EPS:
                return False
    return True


def _expr_is_quantum(
    expr: Expr, quantum: dict[str, bool], *, strict_mode: bool
) -> bool:
    ops = _STRICT_QUANTUM_OPS if strict_mode else _QUANTUM_OPS
    if isinstance(expr, KetLit):
        return True
    if isinstance(expr, Coin):
        return False
    if isinstance(expr, Var):
        return quantum.get(expr.name, False)
    if isinstance(expr, Dirac):
        return _expr_is_quantum(expr.arg, quantum, strict_mode=strict_mode)
    if isinstance(expr, Inspect):
        return _expr_is_quantum(expr.expr, quantum, strict_mode=strict_mode)
    if isinstance(expr, Call):
        op = _op_name(expr)
        if op in ops:
            return True
        if op == "expect":
            return False
        # phase/diffuse: coherent but not strict unless already strict parent
        if not strict_mode and op in {"phase", "diffuse"}:
            return True
        return any(
            _expr_is_quantum(a, quantum, strict_mode=strict_mode) for a in expr.args
        )
    if isinstance(expr, WhenExpr):
        return _expr_is_quantum(
            expr.ctrl, quantum, strict_mode=strict_mode
        ) or any(
            _expr_is_quantum(a.body, quantum, strict_mode=strict_mode)
            for a in expr.arms
        )
    if isinstance(expr, BinOp):
        return _expr_is_quantum(
            expr.lhs, quantum, strict_mode=strict_mode
        ) or _expr_is_quantum(expr.rhs, quantum, strict_mode=strict_mode)
    if isinstance(expr, TensorExpr):
        return _expr_is_quantum(
            expr.left, quantum, strict_mode=strict_mode
        ) or _expr_is_quantum(expr.right, quantum, strict_mode=strict_mode)
    if isinstance(expr, EvolveExpr):
        if expr.hamiltonian is not None:
            return True
        return any(
            _expr_is_quantum(s, quantum, strict_mode=strict_mode) for s in expr.seeds
        )
    if isinstance(expr, TupleExpr):
        return any(
            _expr_is_quantum(it, quantum, strict_mode=strict_mode) for it in expr.items
        )
    if isinstance(expr, Pipe):
        return _expr_is_quantum(expr.rhs, quantum, strict_mode=strict_mode)
    if isinstance(expr, Attr):
        return _expr_is_quantum(expr.obj, quantum, strict_mode=strict_mode)
    if isinstance(expr, Lambda):
        return _expr_is_quantum(expr.body, quantum, strict_mode=strict_mode)
    return False


def _lambda_is_constant(fn: Expr) -> bool:
    if not isinstance(fn, Lambda):
        return False
    return not _mentions_name(fn.body, fn.param) and _is_closed_value(fn.body)


def _mentions_name(expr: Expr, name: str) -> bool:
    if isinstance(expr, Var):
        return expr.name == name
    return any(_mentions_name(c, name) for c in _children(expr))


def _is_closed_value(expr: Expr) -> bool:
    return isinstance(expr, (LitInt, LitFloat, LitBool, LitString)) or (
        isinstance(expr, Dirac) and _is_closed_value(expr.arg)
    )


def _when_collapses(expr: WhenExpr) -> bool:
    """True if every arm body is the same closed literal (support collapse)."""
    vals: list[Any] = []
    for arm in expr.arms:
        body = arm.body
        if isinstance(body, Dirac):
            body = body.arg
        if not _is_closed_value(body):
            return False
        vals.append(_lit_value(body))
    return len(vals) >= 2 and len(set(vals)) == 1


def _is_numeric_lit(expr: Expr) -> bool:
    return isinstance(expr, (LitInt, LitFloat))


def _lit_value(expr: Expr) -> Any:
    if isinstance(expr, LitInt):
        return expr.value
    if isinstance(expr, LitFloat):
        return expr.value
    if isinstance(expr, LitBool):
        return expr.value
    if isinstance(expr, LitString):
        return expr.value
    if isinstance(expr, Dirac):
        return _lit_value(expr.arg)
    return None


def _op_name(expr: Call) -> str:
    cal = expr.callee
    if isinstance(cal, Var):
        return cal.name
    if isinstance(cal, Attr):
        return cal.name
    return ""


def _children(expr: Expr) -> Iterator[Expr]:
    if isinstance(expr, BinOp):
        yield expr.lhs
        yield expr.rhs
    elif isinstance(expr, Call):
        yield expr.callee
        yield from expr.args
    elif isinstance(expr, Attr):
        yield expr.obj
    elif isinstance(expr, Dirac):
        yield expr.arg
    elif isinstance(expr, Inspect):
        yield expr.expr
    elif isinstance(expr, Pipe):
        yield expr.lhs
        yield expr.rhs
    elif isinstance(expr, Lambda):
        yield expr.body
    elif isinstance(expr, TupleExpr):
        yield from expr.items
    elif isinstance(expr, TensorExpr):
        yield expr.left
        yield expr.right
    elif isinstance(expr, WhenExpr):
        yield expr.ctrl
        for arm in expr.arms:
            yield arm.body
    elif isinstance(expr, EvolveExpr):
        yield from expr.seeds
        if expr.duration is not None:
            yield expr.duration
        if expr.hamiltonian is not None:
            yield expr.hamiltonian
        if expr.body is not None:
            for lb in expr.body.lets:
                yield lb.expr
            yield expr.body.result
