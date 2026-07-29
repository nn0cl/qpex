"""staqex.io — host boundary sinks for snapshot / measure (ADR 0029)."""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any, TextIO


def format_marginal_table(marginal: dict[Any, float], *, label: str | None = None) -> str:
    lines: list[str] = []
    if label:
        lines.append(f"# inspect {label}")
    lines.append("value\tmass")
    for v, m in sorted(marginal.items(), key=lambda kv: str(kv[0])):
        lines.append(f"{v}\t{m}")
    return "\n".join(lines) + ("\n" if lines else "")


def format_snapshot_csv(marginal: dict[Any, float]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["value", "mass"])
    for v, m in sorted(marginal.items(), key=lambda kv: str(kv[0])):
        w.writerow([v, m])
    return buf.getvalue()


def write_sink(sink: str, text: str, *, stdout: TextIO | None = None) -> None:
    """Write host text to stdout or a file path named by sink."""
    if sink in {"stdout", "Stdout", "STDOUT", "Console", "console"}:
        if stdout is not None:
            stdout.write(text)
            if text and not text.endswith("\n"):
                stdout.write("\n")
        return
    path = Path(sink)
    # allow File("x") style stripped to x by caller; here sink is bare path/ident
    path.write_text(text, encoding="utf-8")
