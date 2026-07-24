"""First-order Pauli Trotter for `evolve … under H for t` → QASM gates (LISS-0008 / ADR 0063).

Kernel evolve semantics stay exact (Taylor / dense). This module only approximates
for gate backends. No vendor SDKs.
"""

from __future__ import annotations

import math
from typing import Sequence

from ...ast_nodes import (
    Attr,
    BinOp,
    Expr,
    LitFloat,
    LitInt,
    OpExpr,
    Var,
    SuzukiPolicy,
)
from ...runtime.sparse_pauli import PauliTerm, SparsePauli, compile_sparse_pauli
from .circuit import Gate

# Reject codes (surfaced via Circuit.reject_code / EmitResult)
REJECT_UNSUPPORTED_H = "QASM_TROTTER_UNSUPPORTED_H"
REJECT_BAD_TIME = "QASM_TROTTER_BAD_TIME"
REJECT_COMPLEX_COEFF = "QASM_TROTTER_COMPLEX_COEFF"

# Cap slices so NISQ emit stays bounded; scale mildly with |t|.
_MAX_STEPS = 64
_MIN_STEPS = 1


class TrotterError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def trotter_step_count(t: float, *, steps: int | None = None) -> int:
    """Fixed-N policy: explicit `steps`, else ceil(|t|*8) clamped to [1, 64]."""
    if steps is not None:
        return max(_MIN_STEPS, min(_MAX_STEPS, int(steps)))
    return max(_MIN_STEPS, min(_MAX_STEPS, math.ceil(abs(float(t)) * 8.0) or 1))


def eval_time_expr(expr: Expr | int | float, scalars: dict[str, float]) -> float:
    """Evaluate `for t` classical duration (literals / prelude / simple arith)."""
    if isinstance(expr, (int, float)) and not isinstance(expr, bool):
        return float(expr)
    v = _eval_float(expr, scalars)  # type: ignore[arg-type]
    if v is None:
        raise TrotterError(REJECT_BAD_TIME, "evolve duration is not a closed classical float")
    return v


def compile_hamiltonian(
    hop: object,
    *,
    env: dict[str, OpExpr],
    scalars: dict[str, float],
    n_qubits: int,
) -> SparsePauli:
    """Resolve Operator AST / name → sparse Pauli; reject Fock / non-Pauli."""
    from ...ast_nodes import (
        OpBin,
        OpHop,
        OpLit,
        OpNumber,
        OpPauli,
        OpPow,
        OpQuadrature,
        OpVar,
    )

    _OP = (OpBin, OpHop, OpLit, OpNumber, OpPauli, OpPow, OpQuadrature, OpVar)
    if isinstance(hop, Var):
        if hop.name not in env:
            raise TrotterError(REJECT_UNSUPPORTED_H, f"unknown Operator `{hop.name}`")
        op: OpExpr = env[hop.name]
    elif isinstance(hop, _OP):
        op = hop  # type: ignore[assignment]
    else:
        raise TrotterError(
            REJECT_UNSUPPORTED_H,
            f"hamiltonian must be Operator name or Pauli AST, got {type(hop).__name__}",
        )
    try:
        return compile_sparse_pauli(op, env=env, scalars=scalars, n_qubits=n_qubits)
    except ValueError as e:
        raise TrotterError(REJECT_UNSUPPORTED_H, str(e)) from e


def trotter_gates(
    terms: Sequence[PauliTerm],
    t: float,
    site_to_qubit: Sequence[int],
    *,
    steps: int | None = None,
) -> list[Gate]:
    """First-order product: (∏_k exp(-i H_k Δt))^N with Δt = t/N."""
    n = trotter_step_count(t, steps=steps)
    dt = float(t) / float(n)
    out: list[Gate] = []
    for step in range(n):
        for term in terms:
            if abs(term.coeff) < 1e-15:
                continue
            if abs(term.coeff.imag) > 1e-9:
                raise TrotterError(
                    REJECT_COMPLEX_COEFF,
                    f"non-Hermitian Pauli coeff {term.coeff}",
                )
            kinds = term.kinds
            if all(k == "I" for k in kinds):
                # Global phase e^{-i c dt} — omit for QASM probability experiments.
                continue
            theta = float(term.coeff.real) * dt
            if abs(theta) < 1e-15:
                continue
            out.extend(
                _pauli_exp_gates(
                    kinds,
                    theta,
                    site_to_qubit,
                    comment=f"trotter step {step + 1}/{n} dt={dt:.6g}",
                )
            )
    if not out:
        # Still record that evolve lowered (idle / pure phase).
        q0 = site_to_qubit[0]
        out.append(
            Gate("rz", (q0,), angle=0.0, comment=f"trotter N={n} idle/global-phase")
        )
    return out


def suzuki_step_count(
    terms: Sequence[PauliTerm],
    t: float,
    *,
    tolerance: float | None = None,
    error_mode: str | None = None,
    steps: int | None = None,
) -> int:
    """Resolve the statically fixed step count for the accepted S2 policy.

    Direct ``steps`` is preserved exactly.  Tolerance mode uses the ADR 0084
    alpha bound/estimate and never silently clamps the resulting value.
    """
    if steps is not None and tolerance is not None:
        raise TrotterError("SUZUKI_POLICY_ERROR", "steps and tolerance are mutually exclusive")
    if steps is not None:
        if int(steps) < 1:
            raise TrotterError("SUZUKI_POLICY_ERROR", "steps must be positive")
        return int(steps)
    if tolerance is None or error_mode not in {"Bound", "EmpiricalEstimate"}:
        raise TrotterError(
            "SUZUKI_POLICY_ERROR",
            "tolerance mode requires error = Bound or EmpiricalEstimate",
        )
    epsilon = float(tolerance)
    if epsilon <= 0.0:
        raise TrotterError("SUZUKI_POLICY_ERROR", "tolerance must be positive")
    alpha = sum(abs(term.coeff) for term in terms)
    denominator = 12.0 if error_mode == "Bound" else 120.0
    estimate = math.sqrt((alpha**3 * abs(float(t)) ** 3) / (denominator * epsilon))
    return max(_MIN_STEPS, math.ceil(estimate))


def resolve_suzuki_steps(policy: SuzukiPolicy, terms: Sequence[PauliTerm], t: float) -> int:
    """Resolve an AST Suzuki policy after its Hamiltonian is compiled."""
    steps = int(policy.steps.value) if isinstance(policy.steps, LitInt) else None
    tolerance = (
        float(policy.tolerance.value)
        if isinstance(policy.tolerance, (LitInt, LitFloat))
        else None
    )
    return suzuki_step_count(
        terms,
        t,
        tolerance=tolerance,
        error_mode=policy.error_mode,
        steps=steps,
    )


def suzuki_gates(
    terms: Sequence[PauliTerm],
    t: float,
    site_to_qubit: Sequence[int],
    *,
    steps: int,
) -> list[Gate]:
    """Emit the symmetric second-order Suzuki product from ADR 0084."""
    if steps < 1:
        raise TrotterError("SUZUKI_POLICY_ERROR", "steps must be positive")
    n = int(steps)
    dt = float(t) / float(n)
    out: list[Gate] = []
    for step in range(n):
        ordered = list(terms[:-1])
        for term in ordered:
            out.extend(_suzuki_term_gates(term, dt / 2.0, site_to_qubit, step, n))
        if terms:
            out.extend(_suzuki_term_gates(terms[-1], dt, site_to_qubit, step, n))
        for term in reversed(ordered):
            out.extend(_suzuki_term_gates(term, dt / 2.0, site_to_qubit, step, n))
    if not out:
        q0 = site_to_qubit[0]
        out.append(Gate("rz", (q0,), angle=0.0, comment=f"suzuki S2 N={n} idle/global-phase"))
    return out


def _suzuki_term_gates(
    term: PauliTerm,
    delta_t: float,
    site_to_qubit: Sequence[int],
    step: int,
    total_steps: int,
) -> list[Gate]:
    if abs(term.coeff) < 1e-15:
        return []
    if abs(term.coeff.imag) > 1e-9:
        raise TrotterError(
            REJECT_COMPLEX_COEFF,
            f"non-Hermitian Pauli coeff {term.coeff}",
        )
    if all(kind == "I" for kind in term.kinds):
        return []
    theta = float(term.coeff.real) * delta_t
    if abs(theta) < 1e-15:
        return []
    return _pauli_exp_gates(
        term.kinds,
        theta,
        site_to_qubit,
        comment=f"suzuki S2 step {step + 1}/{total_steps} dt={delta_t:.6g}",
    )


def _pauli_exp_gates(
    kinds: tuple[str, ...],
    theta: float,
    site_to_qubit: Sequence[int],
    *,
    comment: str = "",
) -> list[Gate]:
    """Emit gates for exp(-i θ P) with P = ⊗ kinds[site].

    Basis change X→H, Y→rx(π/2); CNOT ladder; rz(2θ); undo.
    OpenQASM rz(φ) = exp(-i φ Z / 2) ⇒ exp(-i θ Z) uses φ = 2θ.
    """
    active: list[tuple[int, str]] = []
    for site, kind in enumerate(kinds):
        k = kind.upper()
        if k == "I":
            continue
        if k not in {"X", "Y", "Z"}:
            raise TrotterError(REJECT_UNSUPPORTED_H, f"unsupported Pauli kind `{kind}`")
        if site >= len(site_to_qubit):
            raise TrotterError(
                REJECT_UNSUPPORTED_H,
                f"Pauli site {site} outside evolve wire count {len(site_to_qubit)}",
            )
        active.append((site_to_qubit[site], k))
    if not active:
        return []

    gates: list[Gate] = []
    # Basis change → Z
    for q, k in active:
        if k == "X":
            gates.append(Gate("h", (q,), comment=comment))
        elif k == "Y":
            gates.append(Gate("rx", (q,), angle=math.pi / 2.0, comment=comment))
    # Parity onto last qubit
    for i in range(len(active) - 1):
        c, t = active[i][0], active[i + 1][0]
        gates.append(Gate("cx", (c, t), comment=comment))
    # Diagonal rotation
    target = active[-1][0]
    gates.append(Gate("rz", (target,), angle=2.0 * theta, comment=comment))
    # Undo CNOTs
    for i in range(len(active) - 2, -1, -1):
        c, t = active[i][0], active[i + 1][0]
        gates.append(Gate("cx", (c, t), comment=comment))
    # Undo basis
    for q, k in active:
        if k == "X":
            gates.append(Gate("h", (q,), comment=comment))
        elif k == "Y":
            gates.append(Gate("rx", (q,), angle=-math.pi / 2.0, comment=comment))
    return gates


def _eval_float(expr: Expr, scalars: dict[str, float]) -> float | None:
    if isinstance(expr, LitFloat):
        return float(expr.value)
    if isinstance(expr, LitInt):
        return float(expr.value)
    if isinstance(expr, Var):
        if expr.name in scalars:
            return float(scalars[expr.name])
        from ...stdlib.prelude import PRELUDE_CONSTANTS

        if expr.name in PRELUDE_CONSTANTS:
            return float(PRELUDE_CONSTANTS[expr.name])
        return None
    if isinstance(expr, Attr):
        base = _eval_float(expr.obj, scalars)
        if base is None:
            return None
        unit_scale = {"s": 1.0, "ms": 1e-3, "us": 1e-6, "ns": 1e-9}
        return base * unit_scale[expr.name] if expr.name in unit_scale else None
    if isinstance(expr, BinOp):
        a = _eval_float(expr.lhs, scalars)
        b = _eval_float(expr.rhs, scalars)
        if a is None or b is None:
            return None
        if expr.op == "+":
            return a + b
        if expr.op == "-":
            return a - b
        if expr.op == "*":
            return a * b
        if expr.op == "/":
            if b == 0.0:
                return None
            return a / b
    return None
