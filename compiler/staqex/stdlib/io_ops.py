"""staqex.io — host boundary sinks for snapshot / measure (ADR 0029 / 0171)."""

from __future__ import annotations

import csv
import io
from typing import Any, TextIO

from ..measure_sink_port import _STDOUT_ALIASES, resolve_measure_sink


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
    """Write host text to stdout or a file path named by sink (via MeasureSinkPort)."""
    if sink in _STDOUT_ALIASES:
        if stdout is None:
            return
        if text and not text.endswith("\n"):
            text = text + "\n"
    port = resolve_measure_sink(sink, stdout=stdout)
    if port is None:
        return
    port.write(text)
