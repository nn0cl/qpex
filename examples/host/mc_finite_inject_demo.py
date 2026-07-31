#!/usr/bin/env python3
"""Host consumption seam demo (ADR 0164 / LISS-0198).

Continuous draws stay on the Host. Only the finite Joint enters Kernel-shaped
Born accounting. No Kernel Continuous syntax.
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host_monte_carlo import run_host_mc_inject


def main() -> None:
    inject, joint = run_host_mc_inject(
        domain_label="Position",
        interval=(0.0, 1.0),
        n_bins=4,
        n_samples=2000,
        coordinate="x",
        continuous_draw=lambda r: r.random(),
        seed=42,
        label_mode="bin_midpoint",
    )
    print("discretization:", inject.provenance["discretization"])
    print("atoms (label, mass):", inject.atoms)
    print("Born masses:")
    for w in joint.worlds:
        print(f"  x={w.assign['x']!r}  |amp|^2={abs(w.amp) ** 2:.6f}")


if __name__ == "__main__":
    main()
