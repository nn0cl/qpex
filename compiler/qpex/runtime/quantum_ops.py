"""Named qubit Hamiltonians / Paulis for `evolve under H` and `expect` (ADR 0038)."""

from __future__ import annotations

import cmath
import math
from typing import Any


def pauli_u(name: str, t: float) -> tuple[complex, complex, complex, complex]:
    """Return U = e^{-i H t} as flat (u00, u01, u10, u11) for H ∈ {X,Y,Z,I}."""
    n = name.upper()
    if n in {"I", "ID", "IDENTITY"}:
        return (1 + 0j, 0j, 0j, 1 + 0j)
    if n == "Z":
        # e^{-i Z t} = diag(e^{-it}, e^{it})
        return (cmath.exp(-1j * t), 0j, 0j, cmath.exp(1j * t))
    if n == "X":
        # e^{-i X t} = cos(t) I - i sin(t) X
        c, s = math.cos(t), math.sin(t)
        return (c + 0j, -1j * s, -1j * s, c + 0j)
    if n == "Y":
        # e^{-i Y t} = cos(t) I - i sin(t) Y; Y = [[0,-i],[i,0]]
        c, s = math.cos(t), math.sin(t)
        return (c + 0j, -s + 0j, s + 0j, c + 0j)
    raise ValueError(f"unknown Hamiltonian `{name}` (MVP: X, Y, Z, I)")


def apply_u2(
    a0: complex, a1: complex, u: tuple[complex, complex, complex, complex]
) -> tuple[complex, complex]:
    u00, u01, u10, u11 = u
    return (u00 * a0 + u01 * a1, u10 * a0 + u11 * a1)


def expect_pauli(name: str, a0: complex, a1: complex) -> float:
    """⟨ψ|P|ψ⟩ for P ∈ {X,Y,Z,I} on a qubit amp pair."""
    n = name.upper()
    p0 = abs(a0) ** 2
    p1 = abs(a1) ** 2
    if n in {"I", "ID", "IDENTITY"}:
        return float(p0 + p1)
    if n == "Z":
        return float(p0 - p1)
    if n == "X":
        return float(2.0 * (a0.conjugate() * a1).real)
    if n == "Y":
        # ⟨Y⟩ = 2 Im(conj(a0) a1) with Y convention
        return float(2.0 * (a0.conjugate() * a1).imag)
    raise ValueError(f"unknown observable `{name}`")


def z_pm(bit: Any) -> float:
    """Map computational bit {0,1} → Pauli-Z eigenvalue {+1,−1}."""
    if bit in (0, 0.0, False):
        return 1.0
    if bit in (1, 1.0, True):
        return -1.0
    raise ValueError(f"Z eigenvalue expects qubit bit, got {bit!r}")


def expect_zz(worlds: list[Any], ctrl: str, tgt: str) -> float:
    """⟨Z⊗Z⟩ = Σ_w |c_w|² z(ctrl) z(tgt) on computational joint worlds."""
    total = 0.0
    weight = 0.0
    for w in worlds:
        if ctrl not in w.assign or tgt not in w.assign:
            continue
        p = float(abs(w.amp) ** 2)
        if p <= 1e-15:
            continue
        total += p * z_pm(w.assign[ctrl]) * z_pm(w.assign[tgt])
        weight += p
    if weight <= 1e-15:
        return 0.0
    return float(total / weight)


def cnot_bit(ctrl: Any, tgt: Any) -> Any:
    """CNOT on computational bits: |c,t⟩ ↦ |c, t⊕c⟩."""
    c = int(ctrl)
    t = int(tgt)
    if c not in (0, 1) or t not in (0, 1):
        raise ValueError(f"cnot expects qubit bits, got ctrl={ctrl!r} tgt={tgt!r}")
    return t ^ c


def ket_support(label: str) -> list[tuple[Any, complex]]:
    """Expand ket label → (value, amplitude) pairs (unnormalized only for ±)."""
    s = 1.0 / math.sqrt(2.0)
    if label == "0":
        return [(0, 1.0 + 0j)]
    if label == "1":
        return [(1, 1.0 + 0j)]
    if label == "+":
        return [(0, s + 0j), (1, s + 0j)]
    if label == "-":
        return [(0, s + 0j), (1, -s + 0j)]
    if label and all(c in "01" for c in label):
        return [(int(label, 2), 1.0 + 0j)]
    raise ValueError(f"unsupported ket `|{label}>`")
