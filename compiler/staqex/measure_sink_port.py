"""Kernel measurement / diagnostic sink port (ADR 0166 / 0171).

Wraps today's ``write_sink`` / ``inspect_sink`` TextIO adapters. Host
``JobResult`` / ``MeasurementEnvelope`` remain a separate Host seam.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, TextIO


class MeasureSinkPort(Protocol):
    """Kernel emission for ``measure`` / ``snapshot`` / ``inspect`` text."""

    def write(self, text: str) -> None:
        """Emit ``text`` exactly (callers own newline policy)."""
        ...


class TextIOMeasureSinkAdapter:
    """Adapter that writes to a configured ``TextIO`` (stdout / StringIO)."""

    def __init__(self, stream: TextIO) -> None:
        self._stream = stream

    def write(self, text: str) -> None:
        self._stream.write(text)


class FileMeasureSinkAdapter:
    """Adapter that overwrites a filesystem path (utf-8), matching ``write_sink``."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    def write(self, text: str) -> None:
        self._path.write_text(text, encoding="utf-8")


_STDOUT_ALIASES = frozenset({"stdout", "Stdout", "STDOUT", "Console", "console"})


def resolve_measure_sink(
    sink: str | None,
    *,
    stdout: TextIO | None,
) -> MeasureSinkPort | None:
    """Map a language sink name to a port. ``None`` means no emission."""
    if sink is None or sink in _STDOUT_ALIASES:
        if stdout is None:
            return None
        return TextIOMeasureSinkAdapter(stdout)
    return FileMeasureSinkAdapter(sink)


__all__ = [
    "MeasureSinkPort",
    "TextIOMeasureSinkAdapter",
    "FileMeasureSinkAdapter",
    "resolve_measure_sink",
]
