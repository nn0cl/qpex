"""Kernel program source loading port (ADR 0166 / 0172).

Sits below ``load_module_graph``: the linker requests path contents through
this port. Does not replace ADR 0054 import resolution or merge rules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class SourcePort(Protocol):
    """UTF-8 program / module-info source text for a resolved path."""

    def read_text(self, path: str) -> str:
        """Return the full source text for ``path``."""
        ...


class FilesystemSourceAdapter:
    """Default adapter: filesystem UTF-8 read (today's ``Path.read_text``)."""

    def read_text(self, path: str) -> str:
        return Path(path).read_text(encoding="utf-8")


__all__ = ["SourcePort", "FilesystemSourceAdapter"]
