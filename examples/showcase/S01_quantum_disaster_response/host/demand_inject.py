#!/usr/bin/env python3
"""Morning/tonight demand noise → finite inject (ADR 0163/0164)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host_monte_carlo import run_host_mc_inject


def main() -> None:
    inject, joint = run_host_mc_inject(
        domain_label="RescueDemand",
        interval=(0.0, 1.0),
        n_bins=8,
        n_samples=1500,
        coordinate="demand",
        continuous_draw=lambda r: r.random(),
        seed=42,
        label_mode="bin_midpoint",
        provenance={"phase": "tonight_or_morning", "error_bound": "Unbounded"},
    )
    print("discretization:", inject.provenance["discretization"])
    print("atoms:", inject.atoms[:4], "...")
    born = sum(abs(w.amp) ** 2 for w in joint.worlds)
    print("born_sum:", round(born, 6))


if __name__ == "__main__":
    main()
