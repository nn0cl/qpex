"""Logical → physical gate IR for OpenQASM emission."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

GateName = Literal["h", "x", "rz", "cx", "swap", "measure"]


@dataclass
class Gate:
    name: GateName
    qubits: tuple[int, ...]  # logical indices before routing; physical after
    bits: tuple[int, ...] = ()
    angle: float | None = None  # radians for rz
    comment: str = ""


@dataclass
class Circuit:
    n_qubits: int
    n_bits: int
    gates: list[Gate] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def add(self, gate: Gate) -> None:
        self.gates.append(gate)
