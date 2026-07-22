"""QASM3Emitter — Circuit → OpenQASM 3.0 text."""

from __future__ import annotations

from dataclasses import dataclass

from ...ast_nodes import CompilationUnit
from .circuit import Circuit, Gate
from .lower import lower_unit_to_circuit
from .router import route_circuit
from .topology import Topology, grid, linear


@dataclass
class EmitResult:
    qasm: str
    notes: list[str]
    ok: bool
    circuit: Circuit | None = None


class QASM3Emitter:
    def __init__(
        self,
        *,
        topology: str | Topology = "linear",
        route: bool = True,
        n_physical: int | None = None,
    ) -> None:
        self.topology_spec = topology
        self.route = route
        self.n_physical = n_physical

    def emit_unit(self, unit: CompilationUnit) -> EmitResult:
        logical = lower_unit_to_circuit(unit)
        notes = list(logical.notes)
        circ = logical
        if self.route:
            topo = self._resolve_topo(logical.n_qubits)
            circ = route_circuit(logical, topo)
            notes.extend(circ.notes)
        qasm = self.render(circ)
        return EmitResult(qasm=qasm, notes=notes, ok=True, circuit=circ)

    def _resolve_topo(self, n_logical: int) -> Topology:
        n = self.n_physical or n_logical
        n = max(n, n_logical)
        if isinstance(self.topology_spec, Topology):
            return self.topology_spec
        spec = self.topology_spec.lower()
        if spec.startswith("grid"):
            # grid-2x2 or grid
            if "x" in spec:
                try:
                    _, rc = spec.split("-", 1)
                    r, c = rc.split("x")
                    return grid(int(r), int(c))
                except ValueError:
                    pass
            side = max(2, int(n**0.5) + (0 if int(n**0.5) ** 2 >= n else 1))
            return grid(side, side)
        return linear(n)

    def render(self, circ: Circuit) -> str:
        lines = [
            "OPENQASM 3.0;",
            'include "stdgates.inc";',
            "// QPex QASM3Emitter (Phase 4.1)",
            f"qubit[{circ.n_qubits}] q;",
            f"bit[{max(circ.n_bits, 1)}] c;",
        ]
        for g in circ.gates:
            lines.append(self._fmt_gate(g))
        lines.append("")
        return "\n".join(lines)

    def _fmt_gate(self, g: Gate) -> str:
        cmt = f"  // {g.comment}" if g.comment else ""
        if g.name == "h":
            return f"h q[{g.qubits[0]}];{cmt}"
        if g.name == "x":
            return f"x q[{g.qubits[0]}];{cmt}"
        if g.name == "rz":
            ang = 0.0 if g.angle is None else g.angle
            return f"rz({ang}) q[{g.qubits[0]}];{cmt}"
        if g.name == "cx":
            return f"cx q[{g.qubits[0]}], q[{g.qubits[1]}];{cmt}"
        if g.name == "swap":
            return f"swap q[{g.qubits[0]}], q[{g.qubits[1]}];{cmt}"
        if g.name == "measure":
            b = g.bits[0] if g.bits else 0
            return f"c[{b}] = measure q[{g.qubits[0]}];{cmt}"
        return f"// unknown gate {g.name}"


def emit_openqasm3(
    unit: CompilationUnit,
    *,
    topology: str = "linear",
    route: bool = True,
) -> EmitResult:
    return QASM3Emitter(topology=topology, route=route).emit_unit(unit)
