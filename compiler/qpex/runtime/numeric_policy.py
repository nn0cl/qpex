"""Dependency-free numeric representation and validation policy."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class NumericPolicy:
    real_representation: str
    complex_representation: str
    pmf_tolerance: float
    physical_tolerance: float


MVP_NUMERIC_POLICY = NumericPolicy(
    real_representation="f64",
    complex_representation="complex-f64",
    pmf_tolerance=1e-9,
    physical_tolerance=1e-12,
)

# Stable field names for consumers that do not need the whole policy object.
REAL_REPRESENTATION = MVP_NUMERIC_POLICY.real_representation
COMPLEX_REPRESENTATION = MVP_NUMERIC_POLICY.complex_representation
PMF_TOLERANCE = MVP_NUMERIC_POLICY.pmf_tolerance
PHYSICAL_TOLERANCE = MVP_NUMERIC_POLICY.physical_tolerance


@dataclass(frozen=True)
class NumericValidationError(ValueError):
    """A numeric contract violation; values are never repaired implicitly."""

    value: float
    expected: float
    tolerance: float
    repaired: bool = False

    def __str__(self) -> str:
        return (
            f"numeric value {self.value!r} differs from expected {self.expected!r} "
            f"beyond tolerance {self.tolerance!r}"
        )


def validate_without_repair(
    value: float,
    *,
    expected: float,
    tolerance: float,
) -> float:
    """Validate a finite value without normalization, clipping, or repair."""
    if not isfinite(value) or abs(value - expected) > tolerance:
        raise NumericValidationError(
            value=value,
            expected=expected,
            tolerance=tolerance,
        )
    return value
