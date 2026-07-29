"""Acceptance tests for the scalar Host contract in LISS-0045."""

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))


def _api():
    from compiler.staqex.scientific_input import (  # noqa: F401
        InputProvenance,
        ParameterBinding,
        ParameterSweep,
        ScientificInput,
        ScientificInputValidationError,
    )

    return (
        InputProvenance,
        ParameterBinding,
        ParameterSweep,
        ScientificInput,
        ScientificInputValidationError,
    )


def test_scalar_input_requires_provenance_and_preserves_binding_identity():
    InputProvenance, ParameterBinding, _, ScientificInput, _ = _api()

    provenance = InputProvenance(
        source_formula="rabi(theta)",
        input_id="experiment-001",
    )
    binding = ParameterBinding(name="theta", value=0.25, unit="rad")
    scientific_input = ScientificInput(
        declared_parameters=("theta",),
        bindings=(binding,),
        provenance=provenance,
    )

    assert scientific_input.bindings == (binding,)
    assert scientific_input.provenance.input_id == "experiment-001"


def test_unknown_parameter_name_is_a_hard_validation_error():
    _, ParameterBinding, _, ScientificInput, ScientificInputValidationError = _api()

    try:
        ScientificInput(
            declared_parameters=("theta",),
            bindings=(ParameterBinding(name="phi", value=0.25, unit="rad"),),
            provenance={"source_formula": "rabi(theta)", "input_id": "x"},
        )
    except ScientificInputValidationError as error:
        assert error.code == "SCIENTIFIC_INPUT_UNKNOWN_PARAMETER"
    else:
        raise AssertionError("unknown parameter binding must be rejected")


def test_parameter_sweep_is_non_empty_and_immutable():
    InputProvenance, ParameterBinding, ParameterSweep, _, _ = _api()

    sweep = ParameterSweep(
        bindings=(
            (ParameterBinding(name="theta", value=0.0, unit="rad"),),
            (ParameterBinding(name="theta", value=1.0, unit="rad"),),
        ),
        provenance=InputProvenance(source_formula="rabi(theta)", input_id="x"),
    )

    assert len(sweep.bindings) == 2
    assert isinstance(sweep.bindings, tuple)


def test_incompatible_unit_dimension_is_not_silently_coerced():
    InputProvenance, ParameterBinding, _, ScientificInput, ScientificInputValidationError = _api()

    try:
        ScientificInput(
            declared_parameters={"theta": "Angle"},
            bindings=(ParameterBinding(name="theta", value=2.0, unit="m"),),
            provenance=InputProvenance(source_formula="rabi(theta)", input_id="x"),
        )
    except ScientificInputValidationError as error:
        assert error.code == "SCIENTIFIC_INPUT_DIMENSION_ERROR"
    else:
        raise AssertionError("incompatible units must be rejected")


def test_empty_sweep_is_rejected_with_a_stable_diagnostic():
    InputProvenance, _, ParameterSweep, _, ScientificInputValidationError = _api()

    try:
        ParameterSweep(
            bindings=(),
            provenance=InputProvenance(source_formula="rabi(theta)", input_id="x"),
        )
    except ScientificInputValidationError as error:
        assert error.code == "SCIENTIFIC_INPUT_EMPTY_SWEEP"
    else:
        raise AssertionError("an empty parameter sweep must be rejected")


if __name__ == "__main__":
    tests = [
        test_scalar_input_requires_provenance_and_preserves_binding_identity,
        test_unknown_parameter_name_is_a_hard_validation_error,
        test_parameter_sweep_is_non_empty_and_immutable,
        test_incompatible_unit_dimension_is_not_silently_coerced,
        test_empty_sweep_is_rejected_with_a_stable_diagnostic,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as error:  # Phase 1 Red intentionally reports failures.
            failures += 1
            print(f"FAIL {test.__name__}: {type(error).__name__}: {error}")
    print(f"Scientific input contract: {len(tests) - failures} passed, {failures} failed")
    raise SystemExit(1 if failures else 0)
