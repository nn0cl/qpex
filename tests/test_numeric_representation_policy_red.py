"""AT-TDD Phase 1 Red tests for the numeric representation policy."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from compiler.qpex.runtime.numeric_policy import (  # noqa: E402
    COMPLEX_REPRESENTATION,
    MVP_NUMERIC_POLICY,
    PMF_TOLERANCE,
    PHYSICAL_TOLERANCE,
    REAL_REPRESENTATION,
    NumericValidationError,
    validate_without_repair,
)


def test_mvp_representation_is_dependency_free_floating_point() -> None:
    assert MVP_NUMERIC_POLICY.real_representation == "f64"
    assert MVP_NUMERIC_POLICY.complex_representation == "complex-f64"
    assert REAL_REPRESENTATION == "f64"
    assert COMPLEX_REPRESENTATION == "complex-f64"


def test_contract_tolerances_are_separate() -> None:
    assert PMF_TOLERANCE == 1e-9
    assert PHYSICAL_TOLERANCE == 1e-12
    assert PMF_TOLERANCE != PHYSICAL_TOLERANCE


def test_validation_rejects_without_normalizing_or_clipping() -> None:
    value = 1.0 + 5e-10

    try:
        validate_without_repair(value, expected=1.0, tolerance=PHYSICAL_TOLERANCE)
    except NumericValidationError as exc:
        assert exc.value == value
        assert exc.repaired is False
    else:
        raise AssertionError("physical tolerance violation must be rejected")


if __name__ == "__main__":
    test_mvp_representation_is_dependency_free_floating_point()
    test_contract_tolerances_are_separate()
    test_validation_rejects_without_normalizing_or_clipping()
    print("OK — numeric representation policy Red tests")
