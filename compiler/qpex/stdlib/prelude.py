"""Prelude — names auto-available without import (ADR 0031 / 0034)."""

from __future__ import annotations

# Surface builtins / prep (also Active keywords in lexer).
PRELUDE_PREP = frozenset({"coin", "dirac", "vacuum"})

# Debug / host-boundary helpers always in scope for Kernel scripts.
PRELUDE_DEBUG = frozenset({"inspect", "snapshot", "measure"})

# Combinators (identifiers resolved by Kernel, not hard keywords).
PRELUDE_COMBINATORS = frozenset({"map", "project", "interfer"})

# Qualified Math facade (qpex.math.Math).
PRELUDE_MATH = frozenset({"Math"})

PRELUDE_NAMES = PRELUDE_PREP | PRELUDE_DEBUG | PRELUDE_COMBINATORS | PRELUDE_MATH


def is_prelude(name: str) -> bool:
    return name in PRELUDE_NAMES
