#!/usr/bin/env python3
"""Rolling replan Host job + optional data-parallel workers (ADR 0159)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.staqex.host import run_path


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    entry = root / "main_disaster_response.sqx"
    workers = int(os.environ.get("STAQEX_DATA_PARALLEL_WORKERS", "1"))
    # Resource-profile narrative: Abort-style refusal if budget flag set.
    if os.environ.get("STAQEX_S01_ABORT_BUDGET") == "1":
        print("resource_profile: Abort — replan budget exceeded; shrink model")
        return
    result = run_path(
        str(entry),
        settings={
            "target": "local",
            "seed": 0,
            "data_parallel_workers": workers,
        },
    )
    print("rolling_replan_status:", result.status)
    print("data_parallel_workers:", workers)
    if result.diagnostics:
        print("diagnostics:", [d.get("code") for d in result.diagnostics[:5]])


if __name__ == "__main__":
    main()
