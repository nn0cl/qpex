#!/usr/bin/env python3
"""Export S01 tonight JobResult as TonightTicket JSON (LISS-0243 A→B→C)."""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[4]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

_HOST = Path(__file__).resolve().parent
if str(_HOST) not in sys.path:
    sys.path.insert(0, str(_HOST))

from compiler.staqex.host import JobResult, run_path  # noqa: E402

from ticket_dto import IncompleteMeasurementError, build_tonight_ticket  # noqa: E402

_DEFAULT_ENTRY = (
    Path(__file__).resolve().parents[1] / "main_disaster_response.sqx"
)


def export_tonight_ticket_from_result(
    result: JobResult,
    *,
    entry: str,
    seed: int,
    out_path: Path,
    target: str = "local",
) -> int:
    """Map JobResult → TonightTicket JSON. Return process exit code."""

    if result.status != "succeeded":
        print(
            f"export_tonight_ticket: job status={result.status!r}; refusing ticket",
            file=sys.stderr,
        )
        return 1
    try:
        ticket = build_tonight_ticket(
            result,
            entry=entry,
            seed=seed,
            target=target,
        )
    except IncompleteMeasurementError as exc:
        print(f"export_tonight_ticket: incomplete measurement: {exc}", file=sys.stderr)
        return 2
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(ticket, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


def export_tonight_ticket(
    *,
    entry: str,
    seed: int,
    out_path: Path,
    target: str = "local",
) -> int:
    """Run the S01 spine via Host run_path and write TonightTicket JSON."""

    result = run_path(
        entry,
        settings={"target": target, "seed": seed},
        stdout=io.StringIO(),
    )
    return export_tonight_ticket_from_result(
        result,
        entry=entry,
        seed=seed,
        out_path=out_path,
        target=target,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export S01 tonight JobResult as TonightTicket JSON (sim-only)."
    )
    parser.add_argument(
        "--entry",
        default=str(_DEFAULT_ENTRY),
        help="Path to main_disaster_response.sqx",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output TonightTicket JSON path",
    )
    parser.add_argument("--target", default="local")
    args = parser.parse_args(argv)
    return export_tonight_ticket(
        entry=args.entry,
        seed=args.seed,
        out_path=args.out,
        target=args.target,
    )


if __name__ == "__main__":
    raise SystemExit(main())
