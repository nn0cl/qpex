"""Run the Quantum Observatory through the provider-neutral Host Job API."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow the documented repository-root invocation to find the local package.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from compiler.qpex import submit_path


ENTRY = Path(__file__).with_name("main_observatory.qpex")


def main() -> int:
    job = submit_path(
        str(ENTRY),
        settings={"target": "local", "seed": 0},
        stdout=sys.stdout,
    )
    print(f"job={job.id} status={job.status()}")

    result = job.result()
    if result.status != "succeeded":
        for diagnostic in result.diagnostics:
            print(
                f"{diagnostic.get('code')}: {diagnostic.get('message')}",
                file=sys.stderr,
            )
        return 1

    print(f"measurements={len(result.measurements)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
