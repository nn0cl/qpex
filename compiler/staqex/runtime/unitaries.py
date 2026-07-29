"""Unitary apply on joint wires (ADR 0042 — apply / DTQW)."""

from __future__ import annotations

import cmath
import math
from collections import defaultdict
from typing import Any, Sequence

from .joint import EPS, Joint, World, _coalesce
from .matrix import Matrix, apply_mat, pauli1


def hadamard() -> Matrix:
    s = 1.0 / math.sqrt(2.0)
    return [[s + 0j, s + 0j], [s + 0j, -s + 0j]]


def named_gate_matrix(name: str) -> Matrix | None:
    """Built-in 1-qubit gates for `apply` (not Schrödinger expm)."""
    n = name.upper()
    if n in {"H", "HAD", "HADAMARD"}:
        return hadamard()
    if n in {"I", "X", "Y", "Z"}:
        return pauli1(n)
    if n == "S":
        # Phase gate diag(1, i)
        return [[1 + 0j, 0j], [0j, 1j]]
    if n == "T":
        # π/8 gate diag(1, e^{iπ/4})
        return [[1 + 0j, 0j], [0j, cmath.exp(1j * math.pi / 4)]]
    return None


def rotation_gate_matrix(axis: str, theta: float) -> Matrix:
    """Rx / Ry / Rz(θ) for QASM-aligned `apply(rx(θ), q)` surface."""
    a = axis.upper()
    half = float(theta) / 2.0
    c = math.cos(half)
    s = math.sin(half)
    if a == "X":
        return [[c + 0j, -1j * s], [-1j * s, c + 0j]]
    if a == "Y":
        return [[c + 0j, -s + 0j], [s + 0j, c + 0j]]
    if a == "Z":
        return [
            [cmath.exp(-1j * half), 0j],
            [0j, cmath.exp(1j * half)],
        ]
    raise ValueError(f"unknown rotation axis `{axis}`")


def apply_unitary_on_wires(
    joint: Joint, wires: Sequence[str], u: Matrix
) -> Joint:
    """Apply dense unitary `u` on `wires` (MSB = wires[0]); tensor I elsewhere."""
    nq = len(wires)
    dim = 2**nq
    if len(u) != dim:
        raise ValueError(
            f"unitary dim {len(u)} does not match {nq} wires (need {dim})"
        )
    if joint.is_vacuum():
        return Joint.empty()

    groups: dict[tuple, list[World]] = defaultdict(list)
    for w in joint.worlds:
        key = tuple(sorted((k, v) for k, v in w.assign.items() if k not in wires))
        groups[key].append(w)

    out_worlds: list[World] = []
    for key, ws in groups.items():
        vec = [0j] * dim
        phases: dict[int, dict[str, complex]] = {}
        for w in ws:
            bits: list[int] = []
            for name in wires:
                if name not in w.assign or w.assign[name] not in (0, 1):
                    raise ValueError(
                        f"apply expects qubit bits {{0,1}} on {list(wires)}"
                    )
                bits.append(int(w.assign[name]))
            idx = 0
            for b in bits:
                idx = (idx << 1) | b
            vec[idx] += w.amp
            phases[idx] = dict(w.coord_phase)
        outv = apply_mat(u, vec)
        base_assign = dict(key)
        for idx, amp in enumerate(outv):
            if abs(amp) ** 2 <= EPS:
                continue
            assign = dict(base_assign)
            x = idx
            bit_list: list[int] = []
            for _ in range(nq):
                bit_list.append(x & 1)
                x >>= 1
            bit_list.reverse()
            for wname, bit in zip(wires, bit_list):
                assign[wname] = bit
            out_worlds.append(
                World(
                    assign=assign,
                    amp=amp,
                    coord_phase=phases.get(idx, {}),
                )
            )
    return Joint(worlds=_coalesce(out_worlds))


def controlled_unitary(u: Matrix) -> Matrix:
    """C(U) = |0⟩⟨0|⊗I + |1⟩⟨1|⊗U  (ctrl is MSB; U acts on remaining qubits)."""
    return multi_controlled_unitary(u, n_controls=1)


def multi_controlled_unitary(
    u: Matrix,
    n_controls: int,
    *,
    active_all_one: bool = True,
    active_mask: int | None = None,
) -> Matrix:
    """Cⁿ(U) on controls-as-MSB.

    active_mask: if set, apply U iff control bits equal this mask
      (bit 0 = LSB = last control; we store MSB-first in wires so
       mask bit (n-1-i) corresponds to controls[i]).
    Else active_all_one=True → all |1⟩; False → all |0⟩ (open).
    """
    from .matrix import zeros

    if n_controls < 1:
        raise ValueError("multi_controlled_unitary needs n_controls ≥ 1")
    dim_tgt = len(u)
    dim = (2**n_controls) * dim_tgt
    out = zeros(dim)
    if active_mask is not None:
        active = active_mask & ((1 << n_controls) - 1)
    else:
        active = (1 << n_controls) - 1 if active_all_one else 0
    for c in range(2**n_controls):
        base = c * dim_tgt
        if c == active:
            for i in range(dim_tgt):
                for j in range(dim_tgt):
                    out[base + i][base + j] = u[i][j]
        else:
            for i in range(dim_tgt):
                out[base + i][base + i] = 1.0 + 0j
    return out

def shift_position(coin: Any, pos: Any) -> Any:
    """DTQW conditional shift: coin 0 → pos−1, coin 1 → pos+1."""
    c = int(coin)
    if c not in (0, 1):
        raise ValueError(f"shift coin expects qubit bit, got {coin!r}")
    p = int(pos) if isinstance(pos, (int, float)) and float(pos) == int(pos) else pos
    if not isinstance(p, int):
        raise ValueError(f"shift position expects Int, got {pos!r}")
    return p - 1 if c == 0 else p + 1
