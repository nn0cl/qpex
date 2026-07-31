"""Host Monte Carlo → finite State inject (ADR 0163 / LISS-0195).

Continuous sampling stays on the Host. The Kernel receives only a finite-support
Joint via ``finite_inject_to_joint``. No Kernel ``Continuous`` type.
"""

from __future__ import annotations

import cmath
import hashlib
import json
import random
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol

from .runtime.joint import EPS, Joint, World

APPROX_EQUAL_WIDTH = "EqualWidthHistogram"


class HostRngPort(Protocol):
    """Host entropy for continuous sampling (≠ Kernel terminal measure RNG)."""

    def random(self) -> float:
        """Return U ~ Uniform[0, 1)."""
        ...


class HostRngAdapter:
    """``random.Random`` adapter implementing ``HostRngPort``."""

    def __init__(self, seed: int | None = None) -> None:
        self._rng = random.Random(seed)

    def random(self) -> float:
        return self._rng.random()


@dataclass(frozen=True)
class MonteCarloSpec:
    """Explicit finiteization contract for equal-width histogram inject."""

    domain_label: str
    interval: tuple[float, float]
    n_bins: int
    n_samples: int
    approximation: str
    coordinate: str
    provenance: Mapping[str, Any] = field(default_factory=dict)
    seed: int | None = None


@dataclass(frozen=True)
class FiniteStateInject:
    """Finite-support carrier ready for Kernel Joint construction."""

    coordinate: str
    atoms: tuple[tuple[int, float], ...]  # (bin_index, mass), masses sum to 1
    provenance: Mapping[str, Any]


class MonteCarloInjectError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


class HostMonteCarloPort(Protocol):
    def sample_to_finite(
        self,
        spec: MonteCarloSpec,
        rng: HostRngPort,
        *,
        continuous_draw: Callable[[HostRngPort], float],
    ) -> FiniteStateInject:
        ...


class EqualWidthHistogramMonteCarlo:
    """MVP ``HostMonteCarloPort``: equal-width histogram on a declared interval."""

    def sample_to_finite(
        self,
        spec: MonteCarloSpec,
        rng: HostRngPort,
        *,
        continuous_draw: Callable[[HostRngPort], float],
    ) -> FiniteStateInject:
        _validate_spec(spec)
        if spec.approximation != APPROX_EQUAL_WIDTH:
            raise MonteCarloInjectError(
                "MONTE_CARLO_APPROXIMATION_UNSUPPORTED",
                f"unsupported approximation `{spec.approximation}`; "
                f"MVP allows only `{APPROX_EQUAL_WIDTH}`",
            )

        lo, hi = spec.interval
        width = hi - lo
        counts: Counter[int] = Counter()
        n_rejected = 0
        for _ in range(spec.n_samples):
            x = float(continuous_draw(rng))
            if not (lo <= x < hi):
                n_rejected += 1
                continue
            # Equal-width bin index in [0, n_bins-1].
            idx = int((x - lo) / width * spec.n_bins)
            if idx < 0:
                idx = 0
            elif idx >= spec.n_bins:
                idx = spec.n_bins - 1
            counts[idx] += 1

        n_accepted = sum(counts.values())
        if n_accepted == 0:
            raise MonteCarloInjectError(
                "MONTE_CARLO_EMPTY_SUPPORT",
                "no samples fell inside the declared interval; refuse empty inject",
            )

        atoms = tuple(
            (int(label), count / n_accepted)
            for label, count in sorted(counts.items())
        )
        digest = _spec_digest(spec)
        provenance: dict[str, Any] = {
            **dict(spec.provenance),
            "domain_label": spec.domain_label,
            "interval": [lo, hi],
            "n_bins": spec.n_bins,
            "n_samples": spec.n_samples,
            "approximation": spec.approximation,
            "seed": spec.seed,
            "n_accepted": n_accepted,
            "n_rejected": n_rejected,
            "spec_digest": digest,
            "finite_approximation": True,
            "note": "finite histogram support; not the continuous PDF",
        }
        return FiniteStateInject(
            coordinate=spec.coordinate,
            atoms=atoms,
            provenance=provenance,
        )


def finite_inject_to_joint(inject: FiniteStateInject) -> Joint:
    """Map normalized masses to Joint worlds with amp = √mass (ADR 0163)."""
    if not inject.atoms:
        raise MonteCarloInjectError(
            "MONTE_CARLO_EMPTY_SUPPORT",
            "cannot build Joint from empty FiniteStateInject",
        )
    worlds: list[World] = []
    for label, mass in inject.atoms:
        if mass <= EPS:
            continue
        worlds.append(
            World(
                assign={inject.coordinate: int(label)},
                amp=cmath.sqrt(float(mass)) + 0.0j,
            )
        )
    if not worlds:
        raise MonteCarloInjectError(
            "MONTE_CARLO_EMPTY_SUPPORT",
            "all atom masses were below epsilon",
        )
    return Joint(worlds=worlds)


def _validate_spec(spec: MonteCarloSpec) -> None:
    lo, hi = spec.interval
    if not (
        spec.domain_label
        and spec.coordinate
        and spec.n_bins >= 1
        and spec.n_samples >= 1
        and hi > lo
        and spec.approximation
    ):
        raise MonteCarloInjectError(
            "MONTE_CARLO_SPEC_INVALID",
            "MonteCarloSpec requires domain_label, coordinate, n_bins≥1, "
            "n_samples≥1, approximation, and interval with hi > lo",
        )


def _spec_digest(spec: MonteCarloSpec) -> str:
    payload = {
        "domain_label": spec.domain_label,
        "interval": list(spec.interval),
        "n_bins": spec.n_bins,
        "n_samples": spec.n_samples,
        "approximation": spec.approximation,
        "coordinate": spec.coordinate,
        "seed": spec.seed,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


__all__ = [
    "APPROX_EQUAL_WIDTH",
    "EqualWidthHistogramMonteCarlo",
    "FiniteStateInject",
    "HostMonteCarloPort",
    "HostRngAdapter",
    "HostRngPort",
    "MonteCarloInjectError",
    "MonteCarloSpec",
    "finite_inject_to_joint",
]
