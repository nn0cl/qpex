"""Canonical source formatting for LISS-0072 Slice B."""

from __future__ import annotations

from .migrate_unicode_math import migrate_unicode_math_source


def format_source(source: str) -> str:
    """Return the current canonical source spelling for formatter-owned slices.

    Slice B keeps formatting intentionally small: preserve the existing source
    layout and comments while canonicalizing the approved Unicode math spellings
    from LISS-0069.
    """

    return migrate_unicode_math_source(source)
