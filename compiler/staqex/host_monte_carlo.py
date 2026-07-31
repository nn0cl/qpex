"""Host Monte Carlo → finite State inject (ADR 0163 / 0164).

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
from typing import Any, Callable, Mapping, Protocol, Sequence

from .runtime.joint import EPS, Joint, World

APPROX_EQUAL_WIDTH = "EqualWidthHistogram"

LABEL_BIN_INDEX = "bin_index"
LABEL_BIN_MIDPOINT = "bin_midpoint"
LABEL_EXPLICIT = "explicit_labels"
_SUPPORTED_LABEL_MODES = frozenset(
    {LABEL_BIN_INDEX, LABEL_BIN_MIDPOINT, LABEL_EXPLICIT}
)


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
    label_mode: str = LABEL_BIN_INDEX
    bin_labels: Sequence[Any] | None = None


@dataclass(frozen=True)
class FiniteStateInject:
    """Finite-support carrier ready for Kernel Joint construction."""

    coordinate: str
    atoms: tuple[tuple[Any, float], ...]  # (label, mass), masses sum to 1
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
    """``HostMonteCarloPort``: equal-width histogram on a declared interval."""

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
        if spec.label_mode not in _SUPPORTED_LABEL_MODES:
            raise MonteCarloInjectError(
                "MONTE_CARLO_LABEL_MODE_UNSUPPORTED",
                f"unsupported label_mode `{spec.label_mode}`; "
                f"allowed: {sorted(_SUPPORTED_LABEL_MODES)}",
            )
        if spec.label_mode == LABEL_EXPLICIT:
            labels = spec.bin_labels
            if labels is None or len(labels) != spec.n_bins:
                raise MonteCarloInjectError(
                    "MONTE_CARLO_SPEC_INVALID",
                    "explicit_labels requires bin_labels of length n_bins",
                )
            if len(set(labels)) != len(labels):
                raise MonteCarloInjectError(
                    "MONTE_CARLO_SPEC_INVALID",
                    "explicit_labels requires unique bin_labels",
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
            (_atom_label(spec, idx, lo, width), count / n_accepted)
            for idx, count in sorted(counts.items())
        )
        digest = _spec_digest(spec)
        disc = _discretization_block(spec, lo, hi)
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
            "discretization": disc,
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
                assign={inject.coordinate: label},
                amp=cmath.sqrt(float(mass)) + 0.0j,
            )
        )
    if not worlds:
        raise MonteCarloInjectError(
            "MONTE_CARLO_EMPTY_SUPPORT",
            "all atom masses were below epsilon",
        )
    return Joint(worlds=worlds)


def run_host_mc_inject(
    *,
    domain_label: str,
    interval: tuple[float, float],
    n_bins: int,
    n_samples: int,
    coordinate: str,
    continuous_draw: Callable[[HostRngPort], float],
    approximation: str = APPROX_EQUAL_WIDTH,
    seed: int | None = None,
    provenance: Mapping[str, Any] | None = None,
    label_mode: str = LABEL_BIN_INDEX,
    bin_labels: Sequence[Any] | None = None,
    rng: HostRngPort | None = None,
    port: EqualWidthHistogramMonteCarlo | None = None,
) -> tuple[FiniteStateInject, Joint]:
    """Host consumption seam: draw → histogram finiteize → Joint (ADR 0164)."""
    host_rng: HostRngPort = rng if rng is not None else HostRngAdapter(seed=seed)
    mc = port if port is not None else EqualWidthHistogramMonteCarlo()
    spec = MonteCarloSpec(
        domain_label=domain_label,
        interval=interval,
        n_bins=n_bins,
        n_samples=n_samples,
        approximation=approximation,
        coordinate=coordinate,
        provenance=dict(provenance or {}),
        seed=seed,
        label_mode=label_mode,
        bin_labels=bin_labels,
    )
    inject = mc.sample_to_finite(spec, host_rng, continuous_draw=continuous_draw)
    return inject, finite_inject_to_joint(inject)


def _atom_label(
    spec: MonteCarloSpec, idx: int, lo: float, width: float
) -> Any:
    if spec.label_mode == LABEL_BIN_INDEX:
        return int(idx)
    if spec.label_mode == LABEL_BIN_MIDPOINT:
        bin_w = width / spec.n_bins
        return lo + (idx + 0.5) * bin_w
    assert spec.bin_labels is not None
    return spec.bin_labels[idx]


def _discretization_block(
    spec: MonteCarloSpec, lo: float, hi: float
) -> dict[str, Any]:
    error_bound = spec.provenance.get("error_bound", "Unbounded")
    return {
        "domain": spec.domain_label,
        "basis": APPROX_EQUAL_WIDTH,
        "resolution": spec.n_bins,
        "boundary": {
            "interval": [lo, hi],
            "convention": "half_open_right",
        },
        "approximation": spec.approximation,
        "error_bound": error_bound,
        "label_mode": spec.label_mode,
    }


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
        "label_mode": spec.label_mode,
        "bin_labels": list(spec.bin_labels) if spec.bin_labels is not None else None,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


__all__ = [
    "APPROX_EQUAL_WIDTH",
    "LABEL_BIN_INDEX",
    "LABEL_BIN_MIDPOINT",
    "LABEL_EXPLICIT",
    "EqualWidthHistogramMonteCarlo",
    "FiniteStateInject",
    "HostMonteCarloPort",
    "HostRngAdapter",
    "HostRngPort",
    "MonteCarloInjectError",
    "MonteCarloSpec",
    "finite_inject_to_joint",
    "run_host_mc_inject",
]
