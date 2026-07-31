"""AT-TDD: P1 coverage ledger ↔ Open Topics / CLAUDE honesty consistency."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]


def test_coverage_ledger_consistency_script() -> None:
    script = _REPO / "scripts/check-coverage-ledger-consistency.py"
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=_REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, (
        completed.stdout + "\n" + completed.stderr
    )


if __name__ == "__main__":
    test_coverage_ledger_consistency_script()
    print("OK — coverage ledger consistency red")
