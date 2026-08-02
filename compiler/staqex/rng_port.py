"""Kernel entropy port for terminal ``measure`` (ADR 0166 / 0170).

Distinct from Host ``HostRngPort`` (Monte Carlo inject). Default adapter wraps
stdlib ``random.Random`` so seeded Kernel outputs stay bit-identical.
"""

from __future__ import annotations

import random
from typing import Protocol


class RngPort(Protocol):
    """Kernel entropy for ``measure`` sampling."""

    def random(self) -> float:
        """Return U ~ Uniform[0, 1)."""
        ...


class StdlibRngAdapter:
    """``random.Random`` adapter implementing ``RngPort``."""

    def __init__(
        self,
        *,
        seed: int | None = None,
        rng: random.Random | None = None,
    ) -> None:
        if rng is not None:
            self._rng = rng
        elif seed is not None:
            self._rng = random.Random(seed)
        else:
            self._rng = random.Random()

    def random(self) -> float:
        return self._rng.random()


__all__ = ["RngPort", "StdlibRngAdapter"]
