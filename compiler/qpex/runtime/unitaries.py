"""Unitary apply on joint wires (ADR 0042 — apply / DTQW)."""

from __future__ import annotations

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
    return None


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


def shift_position(coin: Any, pos: Any) -> Any:
    """DTQW conditional shift: coin 0 → pos−1, coin 1 → pos+1."""
    c = int(coin)
    if c not in (0, 1):
        raise ValueError(f"shift coin expects qubit bit, got {coin!r}")
    p = int(pos) if isinstance(pos, (int, float)) and float(pos) == int(pos) else pos
    if not isinstance(p, int):
        raise ValueError(f"shift position expects Int, got {pos!r}")
    return p - 1 if c == 0 else p + 1
