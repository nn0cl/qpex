"""Runtime uncompute witness helpers (LISS-0114 Slice F / R7·R9)."""

from __future__ import annotations

from .joint import Joint
from .numeric_policy import PHYSICAL_TOLERANCE

# Align with ADR 0076 physical-tolerance class / ADR 0107 candidate.
LINEAR_UNCOMPUTE_AMPLITUDE_TOL = PHYSICAL_TOLERANCE


def is_computational_basis_zero(
    joint: Joint,
    name: str,
    *,
    tol: float = LINEAR_UNCOMPUTE_AMPLITUDE_TOL,
) -> bool:
    """True when Born mass of ``name`` is concentrated on computational ``0``.

    Compares ``Σ_{v≠0} P(name=v)`` against ``tol`` relative to joint norm.
    Empty / vacuum joints are treated as zero (no residual ancilla mass).
    """
    total = joint.norm()
    if total <= tol or joint.is_vacuum():
        return True
    marg = joint.marginal(name)
    if not marg:
        return False
    p0 = float(marg.get(0, 0.0))
    return (total - p0) <= tol


def require_computational_basis_zero(
    joint: Joint,
    name: str,
    *,
    tol: float = LINEAR_UNCOMPUTE_AMPLITUDE_TOL,
) -> None:
    """Raise ``ValueError`` with ``UNCOMPUTE_RUNTIME_MISMATCH`` when not ≈ |0⟩."""
    if is_computational_basis_zero(joint, name, tol=tol):
        return
    raise ValueError(
        f"UNCOMPUTE_RUNTIME_MISMATCH: `{name}` is not within {tol} of "
        f"computational |0> (simulator-equivalence uncompute witness)"
    )
