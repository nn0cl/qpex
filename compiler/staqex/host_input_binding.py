"""Host input binding validation (ADR 0194).

Validates a Host-bound matrix value before a Kernel predicate consumes
it -- shape, dtype, and symmetry -- fail-closed. A missing or malformed
binding is always an explicit diagnostic, never a silent pass.
"""

from __future__ import annotations

import math
from typing import Any

HOST_INPUT_BINDING_MISSING = "HOST_INPUT_BINDING_MISSING"
HOST_INPUT_BINDING_VALUE_ERROR = "HOST_INPUT_BINDING_VALUE_ERROR"

Diagnostic = dict[str, Any]


def _diag(code: str, message: str) -> Diagnostic:
    return {"code": code, "message": message}


def validate_matrix_binding(
    name: str,
    value: Any,
    n: int,
    *,
    dtype: type,
    symmetric: bool = True,
) -> list[Diagnostic]:
    """Validate a bound ``n``x``n`` Host input matrix.

    Diagonal entries are never checked -- no consumer reads them.
    """
    if value is None:
        return [_diag(HOST_INPUT_BINDING_MISSING, f"host input `{name}` is not bound")]
    try:
        rows = list(value)
    except TypeError:
        return [
            _diag(
                HOST_INPUT_BINDING_VALUE_ERROR,
                f"host input `{name}` must be a sequence of rows",
            )
        ]
    if len(rows) != n:
        return [
            _diag(
                HOST_INPUT_BINDING_VALUE_ERROR,
                f"host input `{name}` must be {n}x{n}, got {len(rows)} rows",
            )
        ]
    for i, row in enumerate(rows):
        try:
            cells = list(row)
        except TypeError:
            return [
                _diag(
                    HOST_INPUT_BINDING_VALUE_ERROR,
                    f"host input `{name}` row {i} is not a sequence",
                )
            ]
        if len(cells) != n:
            return [
                _diag(
                    HOST_INPUT_BINDING_VALUE_ERROR,
                    f"host input `{name}` row {i} must have {n} columns, "
                    f"got {len(cells)}",
                )
            ]
        rows[i] = cells
        for j, cell in enumerate(cells):
            if dtype is bool:
                if not isinstance(cell, bool):
                    return [
                        _diag(
                            HOST_INPUT_BINDING_VALUE_ERROR,
                            f"host input `{name}`[{i}][{j}] must be Bool",
                        )
                    ]
            else:
                if not isinstance(cell, (int, float)) or isinstance(cell, bool):
                    return [
                        _diag(
                            HOST_INPUT_BINDING_VALUE_ERROR,
                            f"host input `{name}`[{i}][{j}] must be a finite "
                            "non-negative number",
                        )
                    ]
                numeric = float(cell)
                if not math.isfinite(numeric) or numeric < 0:
                    return [
                        _diag(
                            HOST_INPUT_BINDING_VALUE_ERROR,
                            f"host input `{name}`[{i}][{j}] must be a finite "
                            "non-negative number",
                        )
                    ]
    if symmetric:
        for i in range(n):
            for j in range(n):
                if rows[i][j] != rows[j][i]:
                    return [
                        _diag(
                            HOST_INPUT_BINDING_VALUE_ERROR,
                            f"host input `{name}` must be symmetric: "
                            f"[{i}][{j}] != [{j}][{i}]",
                        )
                    ]
    return []


__all__ = [
    "HOST_INPUT_BINDING_MISSING",
    "HOST_INPUT_BINDING_VALUE_ERROR",
    "validate_matrix_binding",
]
