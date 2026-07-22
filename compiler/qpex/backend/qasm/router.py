"""Insert SWAP chains so every CX touches a coupled physical edge."""

from __future__ import annotations

from .circuit import Circuit, Gate
from .topology import Topology, linear, shortest_path


def route_circuit(circ: Circuit, topo: Topology | None = None) -> Circuit:
    """Map logical qubits 0..n-1 onto physical 0..n-1 (identity layout) + SWAP route."""
    if topo is None:
        topo = linear(max(circ.n_qubits, 1))
    if topo.n_qubits < circ.n_qubits:
        raise ValueError(
            f"topology {topo.name} has {topo.n_qubits} qubits < circuit {circ.n_qubits}"
        )

    # logical → physical placement (initially identity)
    place = list(range(circ.n_qubits))
    # physical → logical
    inv = {p: l for l, p in enumerate(place)}

    out = Circuit(n_qubits=topo.n_qubits, n_bits=circ.n_bits, notes=list(circ.notes))
    out.notes.append(f"routed on {topo.name}")

    for g in circ.gates:
        if g.name == "cx":
            la, lb = g.qubits
            pa, pb = place[la], place[lb]
            if topo.coupled(pa, pb):
                out.add(Gate("cx", (pa, pb), comment=g.comment))
                continue
            path = shortest_path(topo, pa, pb)
            # SWAP along path until adjacent to target
            for i in range(len(path) - 2):
                u, v = path[i], path[i + 1]
                out.add(Gate("swap", (u, v), comment=f"route {pa}→{pb}"))
                # update placement
                lu, lv = inv[u], inv[v]
                place[lu], place[lv] = v, u
                inv[u], inv[v] = lv, lu
            pa, pb = place[la], place[lb]
            # after swaps, pa should be neighbor of pb
            if not topo.coupled(pa, pb):
                # one more swap if needed
                path2 = shortest_path(topo, pa, pb)
                if len(path2) >= 2:
                    u, v = path2[0], path2[1]
                    out.add(Gate("swap", (u, v), comment="route final"))
                    lu, lv = inv[u], inv[v]
                    place[lu], place[lv] = v, u
                    inv[u], inv[v] = lv, lu
                    pa, pb = place[la], place[lb]
            out.add(Gate("cx", (pa, pb), comment=g.comment))
        elif g.name == "measure":
            (lq,) = g.qubits
            out.add(Gate("measure", (place[lq],), bits=g.bits, comment=g.comment))
        elif g.name == "rz":
            (lq,) = g.qubits
            out.add(Gate("rz", (place[lq],), angle=g.angle, comment=g.comment))
        elif g.name == "cz":
            la, lb = g.qubits
            pa, pb = place[la], place[lb]
            if not topo.coupled(pa, pb):
                # reuse CX routing via temporary CX-shaped path: swap until adjacent
                path = shortest_path(topo, pa, pb)
                for i in range(len(path) - 2):
                    u, v = path[i], path[i + 1]
                    out.add(Gate("swap", (u, v), comment=f"route-cz {pa}→{pb}"))
                    lu, lv = inv[u], inv[v]
                    place[lu], place[lv] = v, u
                    inv[u], inv[v] = lv, lu
                pa, pb = place[la], place[lb]
            out.add(Gate("cz", (pa, pb), comment=g.comment))
        elif g.name in {"h", "x", "y", "z", "swap"}:
            qs = tuple(place[q] for q in g.qubits)
            out.add(Gate(g.name, qs, comment=g.comment))
        else:
            out.add(g)
    return out
