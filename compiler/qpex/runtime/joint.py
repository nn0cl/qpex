"""Discrete joint store — authoritative Kernel state (correlation-preserving)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Hashable, Iterable

EPS = 1e-12


@dataclass
class World:
    assign: dict[str, Any]
    mass: float


@dataclass
class Joint:
    """Finite-support joint over named coordinates."""

    worlds: list[World] = field(default_factory=list)

    @staticmethod
    def empty() -> Joint:
        return Joint(worlds=[])

    @staticmethod
    def unit() -> Joint:
        """Single empty assignment with mass 1 (no coordinates yet)."""
        return Joint(worlds=[World(assign={}, mass=1.0)])

    def norm(self) -> float:
        return float(sum(w.mass for w in self.worlds))

    def is_vacuum(self) -> bool:
        return abs(self.norm()) <= EPS or len(self.worlds) == 0

    def variables(self) -> list[str]:
        keys: set[str] = set()
        for w in self.worlds:
            keys.update(w.assign.keys())
        return sorted(keys)

    def marginal(self, name: str) -> dict[Any, float]:
        acc: dict[Any, float] = defaultdict(float)
        for w in self.worlds:
            if name in w.assign:
                acc[w.assign[name]] += w.mass
        return {k: v for k, v in acc.items() if v > EPS}

    def support_rows(self) -> list[dict[str, Any]]:
        return [{"assignment": dict(w.assign), "mass": w.mass} for w in self.worlds]

    def bind_const(self, name: str, value: Any) -> Joint:
        if self.is_vacuum():
            return Joint.empty()
        return Joint(
            worlds=[
                World(assign={**w.assign, name: value}, mass=w.mass) for w in self.worlds
            ]
        )

    def bind_pushforward(self, name: str, f: Callable[[dict[str, Any]], Any]) -> Joint:
        if self.is_vacuum():
            return Joint.empty()
        return Joint(
            worlds=[
                World(assign={**w.assign, name: f(w.assign)}, mass=w.mass)
                for w in self.worlds
            ]
        )

    def bind_split(
        self, name: str, dist: dict[Any, float] | Callable[[dict[str, Any]], dict[Any, float]]
    ) -> Joint:
        """Extend each world by an independent (or world-dependent) discrete draw."""
        if self.is_vacuum():
            return Joint.empty()
        out: list[World] = []
        for w in self.worlds:
            local = dist(w.assign) if callable(dist) else dist
            for val, p in local.items():
                if p > EPS and w.mass * p > EPS:
                    out.append(World(assign={**w.assign, name: val}, mass=w.mass * p))
        return Joint(worlds=_coalesce(out))

    def project_coord(self, name: str, pred: Callable[[Any], bool]) -> Joint:
        """Keep worlds where pred(world[name]) holds; all rejected → vacuum."""
        kept = [
            World(assign=dict(w.assign), mass=w.mass)
            for w in self.worlds
            if name in w.assign and pred(w.assign[name])
        ]
        if not kept:
            return Joint.empty()
        return Joint(worlds=kept)

    def project_world(self, pred: Callable[[dict[str, Any]], bool]) -> Joint:
        kept = [
            World(assign=dict(w.assign), mass=w.mass)
            for w in self.worlds
            if pred(w.assign)
        ]
        if not kept:
            return Joint.empty()
        return Joint(worlds=kept)

    def map_coord(self, src: str, dest: str, f: Callable[[Any], Any]) -> Joint:
        if self.is_vacuum():
            return Joint.empty()
        return Joint(
            worlds=[
                World(
                    assign={**w.assign, dest: f(w.assign[src])},
                    mass=w.mass,
                )
                for w in self.worlds
                if src in w.assign
            ]
        )

    def replace_coord(self, name: str, f: Callable[[Any], Any]) -> Joint:
        return self.map_coord(name, name, f)


def _coalesce(worlds: Iterable[World]) -> list[World]:
    acc: dict[tuple[tuple[str, Any], ...], float] = defaultdict(float)
    for w in worlds:
        key = tuple(sorted(w.assign.items()))
        acc[key] += w.mass
    return [
        World(assign=dict(k), mass=m) for k, m in acc.items() if m > EPS
    ]


def marginal_to_state_dict(marginal: dict[Any, float]) -> dict[Any, float]:
    return dict(marginal)


def sample_from_marginal(
    marginal: dict[Any, float],
    rng: Any,
) -> Any | None:
    """Draw one atom; vacuum → None. Uses rng.random() in [0,1)."""
    items = [(v, m) for v, m in marginal.items() if m > EPS]
    if not items:
        return None
    total = sum(m for _, m in items)
    if total <= EPS:
        return None
    u = rng.random() * total
    acc = 0.0
    for v, m in items:
        acc += m
        if u <= acc:
            return v
    return items[-1][0]
