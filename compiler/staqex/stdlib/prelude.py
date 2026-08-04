"""Prelude — names auto-available without import (ADR 0031 / 0034 / 0062)."""

from __future__ import annotations

import math

# Surface builtins / prep (also Active keywords in lexer).
PRELUDE_PREP = frozenset({"coin", "dirac", "vacuum", "empty", "wavepacket"})

# Debug / host-boundary helpers always in scope for Kernel scripts.
PRELUDE_DEBUG = frozenset({"inspect", "snapshot", "measure"})

# Combinators (identifiers resolved by Kernel, not hard keywords).
PRELUDE_COMBINATORS = frozenset(
    {
        "map",
        "project",
        "interfer",
        "phase",
        "cis",
        "grover_diffuse",
        "expect",
        "cnot",
        "trace_out",
        "apply",
        "capply",
        "controlled",
        "ocapply",
        "toffoli",
        "hadamard",
        "walk_shift",
        "tensor",
        # ADR 0185 Lane A: Host MC equal-width finiteize → finite State
        "finiteize",
    }
)

# Qualified Math / Complex facades
PRELUDE_MATH = frozenset({"Math", "Complex"})

# Classical scalar constants (ADR 0062) — Float only; not State carriers.
PRELUDE_CONSTANTS: dict[str, float] = {
    "pi": math.pi,  # ≈ 3.141592653589793
    "sqrt2": math.sqrt(2.0),  # ≈ 1.4142135623730951
    "inv_sqrt2": 1.0 / math.sqrt(2.0),  # ≈ 0.7071067811865476 = 1/√2
}

PRELUDE_NAMES = (
    PRELUDE_PREP
    | PRELUDE_DEBUG
    | PRELUDE_COMBINATORS
    | PRELUDE_MATH
    | frozenset(PRELUDE_CONSTANTS)
)


def is_prelude(name: str) -> bool:
    return name in PRELUDE_NAMES


def is_prelude_constant(name: str) -> bool:
    return name in PRELUDE_CONSTANTS
