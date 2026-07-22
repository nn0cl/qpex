"""qpex.math — State→State pointwise pushforwards (ADR 0031)."""

from __future__ import annotations

import math
from typing import Any, Callable

MATH_OPS: dict[str, Callable[[float], float]] = {
    "sin": math.sin,
    "cos": math.cos,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "abs": abs,
    "log": math.log,
    "tan": math.tan,
}


def apply_math(op: str, value: Any) -> float:
    if op not in MATH_OPS:
        raise KeyError(op)
    return float(MATH_OPS[op](float(value)))


def known_math_op(name: str) -> bool:
    return name in MATH_OPS
