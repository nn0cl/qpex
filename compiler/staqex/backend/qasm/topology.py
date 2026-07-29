"""Physical topology models for QPU routing (Phase 4.1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Topology:
    """Undirected coupling graph on physical qubits 0..n-1."""

    n_qubits: int
    edges: frozenset[tuple[int, int]]
    name: str = "custom"

    def neighbors(self, q: int) -> set[int]:
        return {b if a == q else a for a, b in self.edges if a == q or b == q}

    def coupled(self, a: int, b: int) -> bool:
        lo, hi = (a, b) if a < b else (b, a)
        return (lo, hi) in self.edges


def linear(n: int) -> Topology:
    edges = frozenset((i, i + 1) for i in range(n - 1))
    return Topology(n_qubits=n, edges=edges, name=f"linear-{n}")


def grid(rows: int, cols: int) -> Topology:
    edges: set[tuple[int, int]] = set()

    def idx(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                a, b = idx(r, c), idx(r, c + 1)
                edges.add((min(a, b), max(a, b)))
            if r + 1 < rows:
                a, b = idx(r, c), idx(r + 1, c)
                edges.add((min(a, b), max(a, b)))
    return Topology(n_qubits=rows * cols, edges=frozenset(edges), name=f"grid-{rows}x{cols}")


def shortest_path(topo: Topology, src: int, dst: int) -> list[int]:
    """BFS path of physical qubit indices inclusive."""
    if src == dst:
        return [src]
    from collections import deque

    q: deque[int] = deque([src])
    prev: dict[int, int | None] = {src: None}
    while q:
        cur = q.popleft()
        for nxt in topo.neighbors(cur):
            if nxt in prev:
                continue
            prev[nxt] = cur
            if nxt == dst:
                path = [dst]
                while path[-1] != src:
                    path.append(prev[path[-1]])  # type: ignore[arg-type]
                path.reverse()
                return path
            q.append(nxt)
    raise ValueError(f"no path {src}→{dst} on {topo.name}")
